import os
from pathlib import Path

from ProjectDecima import ArchiveManager


def main():
    archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
    print(f'Loading archives from "{archive_dir}"')
    dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    print(f'Dumping files to "{archive_dir}"')
    ar_set = ArchiveManager(archive_dir)
    ar_set.parse_all()
    while 1:
        core_file_path = input('Core file path: ')
        if not core_file_path:
            break
        file = ar_set.queue_file(core_file_path, False)
        if file:
            os.makedirs((dump_dir / core_file_path).parent, exist_ok=True)
            with (dump_dir / core_file_path).open('wb') as f:
                f.write(file)
            print(f'Written to {dump_dir / core_file_path}')
        else:
            print(f'File {core_file_path} not found.')


if __name__ == '__main__':
    main()
