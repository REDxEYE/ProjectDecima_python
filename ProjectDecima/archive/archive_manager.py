from functools import lru_cache
from pathlib import Path
from typing import List, Union, Dict

from .archive import Archive
from ..utils.decryption import hash_string


class ArchiveManager:
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.archives: List[Archive] = []
        self.hash_to_archive: Dict[int, Archive] = {}

    def parse_all(self):
        all_files = list(self.work_dir.rglob('*.bin'))
        for n, file in enumerate(all_files):
            print(f'Reading {file.stem} archive [{n + 1}/{len(all_files)}]')
            archive = Archive(file)
            archive.parse()
            self.archives.append(archive)
            self.hash_to_archive.update({k: archive for k in archive.hash_to_entry.keys()})

    @lru_cache(16)
    def queue_file(self, file_id: Union[str, int]):
        archive = self.hash_to_archive.get(hash_string(file_id), None)
        if archive:
            core_file = archive.queue_file(file_id)
            return core_file
