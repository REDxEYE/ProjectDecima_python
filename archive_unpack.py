import os
from pathlib import Path
from struct import pack

from ProjectDecima import ArchiveSet, Archive
from ProjectDecima.utils.decryption import hash_string, decrypt_chunk_data
from ProjectDecima.archive.archive import ArchiveEntry, ArchiveChunk
from ProjectDecima.utils.oodle_wrapper import Oodle


def dump_archive(archive_path: str, dump_path: str):
    dump_path = Path(dump_path)
    archive_path = Path(archive_path)
    archive_dump_path = dump_path / archive_path.stem
    archive = Archive(archive_path)
    archive.parse()
    os.makedirs(archive_dump_path, exist_ok=True)
    for entry in archive.entries:
        print(f"Writing {entry.entry_id}-{entry.hash}.bin file")
        data = archive.get_file_data(entry)
        with open(archive_dump_path / f'{entry.entry_id}-{entry.hash}.bin', 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    dump_path = Path(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    archive_path = r"F:\SteamLibrary\steamapps\common\Death Stranding\data\477e458b2c825633499874678a2b9ea5.bin"
    dump_archive(archive_path, dump_path)
