import os
from pathlib import Path
from typing import List

from ProjectDecima import ArchiveManager, CoreFile
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.pod.entry_reference import RTTIRef, LoadMethod
from ProjectDecima.core.pod.stream_reference import StreamingDataSource

dumped_files = []


def dump_file(dump_path: Path, core_file: CoreFile):
    if (dump_path / core_file.filepath).exists():
        return
    reader = core_file.reader
    reader.seek(0)
    os.makedirs((dump_path / core_file.filepath).parent, exist_ok=True)
    print(f"Writing {dump_path / core_file.filepath} core file")
    with (dump_path / core_file.filepath).open('wb') as f:
        f.write(reader.read_bytes(-1))


def dump_core_file(dump_path: Path, core_file: CoreFile):
    print(f"Dumping {core_file.filepath} file")
    if core_file in dumped_files:
        return
    else:
        dumped_files.append(core_file)
    dump_file(dump_path, core_file)
    for entry in file.entries:
        for k, v in entry.__dict__.items():
            if isinstance(v, RTTIRef):
                v: RTTIRef
                if v._core_file is not None and v.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
                    dump_core_file(dump_dir, v._core_file)
            elif isinstance(v, StreamingDataSource):
                v: StreamingDataSource
                if v.mempool_tag.int == 0:
                    continue
                os.makedirs((dump_path / str(v.stream_path)).parent, exist_ok=True)
                print(f"Writing {dump_path / str(v.stream_path)}.core.stream stream")
                if v in dumped_files:
                    continue
                else:
                    dumped_files.append(v)
                    with (dump_path / (str(v.stream_path) + '.core.stream')).open('wb') as f:
                        v.stream_reader.seek(0)
                        f.write(v.stream_reader.read_bytes(-1))
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], RTTIRef):
                v: List[RTTIRef]
                for ref in v:
                    if ref._core_file is not None and ref.load_method in [LoadMethod.ImmediateCoreFile,
                                                                          LoadMethod.CoreFile]:
                        dump_core_file(dump_dir, ref._core_file)


if __name__ == '__main__':
    EntryTypeManager.load_handlers('./ProjectDecima/core/entry_types/')
    archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
    print(f'Loading archives from "{archive_dir}"')
    dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    print(f'Dumping files to "{archive_dir}"')
    ar_set = ArchiveManager(archive_dir)
    ar_set.parse_all()

    while 1:
        core_file_path = input('Core file path: ')
        core_file_path = core_file_path.replace('\\', '/')

        if not core_file_path:
            break
        file = ar_set.queue_file(core_file_path)
        dump_core_file(dump_dir, file)
