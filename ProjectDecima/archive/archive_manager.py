import json
from pathlib import Path
from typing import List, Union, Dict, Set

from .archive import Archive
from ..core.entry_reference import EntryReference
from ..core.stream_reference import StreamingDataSource
from ..utils.decryption import hash_string


class ArchiveManager:
    __core_file_cache: Dict[int, 'CoreFile'] = {}

    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.archives: List[Archive] = []
        self.hash_to_archive: Dict[int, Archive] = {}
        self._invalid_cache = False
        self._cache = {}
        self._exclude_archive = []

    def cache_all(self):
        if self._invalid_cache:
            for archive in self.archives:
                self._cache['archive_info'][archive.filepath.stem] = archive.to_cache()
            cache_path = Path('./cache.json')
            with cache_path.open('w') as f:
                json.dump(self._cache, f)

    def load_cache(self):
        cache_path = Path('./cache.json')
        if cache_path.exists():
            with cache_path.open('r') as f:
                self._cache = json.load(f)
                self._invalid_cache = False
        else:
            self._invalid_cache = True
            self._cache['check'] = {}
            self._cache['archive_info'] = {}

    def check_crc(self, all_files: List[Path]):
        for n, file in enumerate(all_files):
            stat = file.stat()
            print(f'Checking {file.stem} archive [{n + 1}/{len(all_files)}]')
            if self._invalid_cache:
                self._cache['check'][file.stem] = stat.st_ctime_ns
            else:
                prev_ctime = self._cache['check'].get(file.stem, -1)
                if stat.st_ctime_ns != prev_ctime:
                    self._cache['check'][file.stem] = stat.st_ctime_ns
                else:
                    self._cache['check'][file.stem] = stat.st_ctime_ns
                    self._exclude_archive.append(file.stem)

        pass

    def parse_all(self):
        StreamingDataSource.set_archive_manager(self)
        EntryReference.set_archive_manager(self)
        all_files = list(self.work_dir.rglob('*.bin'))
        self.load_cache()
        self.check_crc(all_files)
        for n, file in enumerate(all_files):
            print(f'Reading {file.stem} archive [{n + 1}/{len(all_files)}]')

            archive = Archive(file)
            if file.stem in self._exclude_archive:
                archive.from_cache(self._cache['archive_info'][file.stem])
            else:
                archive.parse()
            self.archives.append(archive)
            self.hash_to_archive.update({k: archive for k in archive.hash_to_entry.keys()})
        self.cache_all()
        self._cache = {}

    def queue_file(self, file_id: Union[str, int], is_core_file=True):
        if isinstance(file_id, str):
            if file_id.rfind('.') == -1:
                file_id += '.core' if is_core_file else '.core.stream'
        core_file = self.__core_file_cache.get(file_id, None)
        if core_file:
            return core_file
        archive = self.hash_to_archive.get(hash_string(file_id), None)
        if archive:
            core_file = archive.queue_file(file_id, is_core_file)
            self.__core_file_cache[file_id] = core_file
            return core_file
