import os
from pathlib import Path
from typing import List

from ProjectDecima import ArchiveManager, CoreFile, Archive
from ProjectDecima.core.entry_reference import EntryReference, LoadMethod
from ProjectDecima.core.stream_reference import StreamReference

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
            if isinstance(v, EntryReference):
                v: EntryReference
                if v._core_file is not None and v.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
                    dump_core_file(dump_dir, v._core_file)
            elif isinstance(v, StreamReference):
                v: StreamReference
                if v.mempool_tag.int==0:
                    continue
                os.makedirs((dump_path / str(v.stream_path)).parent, exist_ok=True)
                print(f"Writing {dump_path / str(v.stream_path)}.core.stream stream")
                if v in dumped_files:
                    continue
                else:
                    dumped_files.append(v)
                    with (dump_path / (str(v.stream_path)+'.core.stream')).open('wb') as f:
                        v.stream_reader.seek(0)
                        f.write(v.stream_reader.read_bytes(-1))
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], EntryReference):
                v: List[EntryReference]
                for ref in v:
                    if ref._core_file is not None and ref.load_method in [LoadMethod.ImmediateCoreFile,
                                                                          LoadMethod.CoreFile]:
                        dump_core_file(dump_dir, ref._core_file)


if __name__ == '__main__':
    archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
    print(f'Loading archives from "{archive_dir}"')
    dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    print(f'Dumping files to "{archive_dir}"')
    ar_set = ArchiveManager(archive_dir)
    ar_set.parse_all()

    while 1:
        core_file_path = input('Core file path: ')
        core_file_path = core_file_path.replace('\\','/')
        if not core_file_path:
            break
        file = ar_set.queue_file(core_file_path)
        dump_core_file(dump_dir, file)
