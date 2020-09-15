import os
from pathlib import Path

from ProjectDecima import ArchiveManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.stream_reference import StreamReference


def main():
    archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
    print(f'Loading archives from "{archive_dir}"')
    dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    print(f'Dumping files to "{archive_dir}"')
    ar_set = ArchiveManager(archive_dir)
    ar_set.parse_all()
    while 1:
        core_file_path = input(
            'Core file path: ') or "localized/sentences/ds_lines_common/lines_1p5_dsp_global/sentences.core"
        if not core_file_path:
            break
        file = ar_set.queue_file(core_file_path, True)
        os.makedirs((dump_dir / Path(core_file_path).with_suffix('')), exist_ok=True)
        file_dump_path = dump_dir / Path(core_file_path).with_suffix('')
        for entry in file.entries:
            if not entry.exportable:
                continue
            entry_dump_path = file_dump_path
            os.makedirs(entry_dump_path, exist_ok=True)
            entry.dump(entry_dump_path)


if __name__ == '__main__':
    main()
