import mmap
import os
from pathlib import Path
from struct import pack

import tqdm

from ProjectDecima import ArchiveManager, Archive
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
    total = len(archive.entries)
    for n, entry in tqdm.tqdm(enumerate(archive.entries), desc='Unpacking files', unit_scale=1, unit=' files',
                              total=total):
        data = archive.get_file_data(entry)
        with open(archive_dump_path / f'{entry.hash}.bin', 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    dump_path = Path(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    archive_path = r"F:\SteamLibrary\steamapps\common\Death Stranding\data\7017f9bb9d52fc1c4433599203cc51b1.bin"
    dump_archive(archive_path, dump_path)
