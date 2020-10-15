import math
import os
import struct
from pathlib import Path
from struct import pack
from typing import List, Tuple

import tqdm

from ProjectDecima import ArchiveManager, Archive
from ProjectDecima.utils.decryption import hash_string, decrypt_chunk_data
from ProjectDecima.archive.archive import ArchiveEntry, ArchiveChunk, ArchiveVersion, ArchiveHeader
from ProjectDecima.utils.oodle_wrapper import Oodle


class ArchivePacker:
    _chunk_max_size = 262144

    def __init__(self, arc_dir: str, output_name: str, encrypt: bool = False):
        self._encrypt = encrypt
        self.arc_dir = Path(arc_dir)
        self.files: List[Tuple[Path, int]] = []
        self.entries: List[Tuple[ArchiveEntry, Path]] = []
        self.chunks: List[ArchiveChunk] = []
        self.name = output_name

        self._output_archive = Path(self.arc_dir / f'{self.name}.bin.repack')
        self._output_handle = self._output_archive.open('wb')

    def collect_files(self):
        print('Collecting bin files')
        for file in self.arc_dir.rglob('*.bin'):
            self.files.append((file, file.stat().st_size))

    def create_entries(self):
        print('Creating file entries')
        for entry_id, (file, file_size) in tqdm.tqdm(enumerate(self.files), desc='Creating file entries',
                                                     total=len(self.files), unit=' entry', unit_scale=1):
            entry = ArchiveEntry()
            entry.entry_id = entry_id
            entry.hash = int(file.stem)
            entry.size = file_size
            entry.key_0 = ((entry.entry_id * entry.hash) ^ 0xFEEEDECE) & 0xFFFFFFFF
            entry.key_1 = ((entry.entry_id * entry.hash) ^ 0xAEBECEDE) & 0xFFFFFFFF
            self.entries.append((entry, file))
        self.entries.sort(key=lambda a: a[0].hash, reverse=False)

    def create_chunks(self):
        print('Creating chunks')
        total_data_size = sum([v[1] for v in self.files])
        estimated_chunk_count = math.ceil(total_data_size / self._chunk_max_size)
        chunk_data_start_offset = len(self.entries) * 32 + estimated_chunk_count * 32 + 40
        chunk_buffer = bytes()
        uncompressed_offset = 0
        accumulative_offset = 0

        def create_chunk(data, output_file):
            nonlocal uncompressed_offset
            chunk = ArchiveChunk()
            chunk.uncompressed_offset = uncompressed_offset
            chunk.uncompressed_size = len(data)
            uncompressed_offset += chunk.uncompressed_size

            compressed_data = Oodle.compress(data)
            chunk.compressed_size = len(compressed_data)
            chunk.compressed_offset = output_file.tell()

            chunk.key_0 = (chunk.uncompressed_size ^ chunk.uncompressed_offset) & 0xFFFFFFFF
            chunk.key_1 = (chunk.compressed_size ^ chunk.compressed_offset) & 0xFFFFFFFF
            if self._encrypt:
                compressed_data = self._encrypt_chunk(chunk, compressed_data)

            output_file.write(compressed_data)
            self.chunks.append(chunk)

        self._output_handle.write(b'\x00' * chunk_data_start_offset)

        for i, ((file, size), (entry, _)) in tqdm.tqdm(enumerate(zip(self.files, self.entries)),
                                                       desc='Compressing files', total=len(self.entries),
                                                       unit=' files', unit_scale=1):
            entry.offset = accumulative_offset
            accumulative_offset += size
            with file.open('rb') as f:
                chunk_buffer += f.read()
            while len(chunk_buffer) >= self._chunk_max_size:
                chunk_data = chunk_buffer[:self._chunk_max_size]
                chunk_buffer = chunk_buffer[self._chunk_max_size:]
                create_chunk(chunk_data, self._output_handle)
        create_chunk(chunk_buffer, self._output_handle)

    @staticmethod
    def _encrypt_chunk(chunk: ArchiveChunk, chunk_data: bytes):
        key = pack('Q2I', chunk.uncompressed_offset, chunk.uncompressed_size, chunk.key_0)
        chunk_data = decrypt_chunk_data(chunk_data, key)
        return chunk_data

    def write_archive(self):
        header = ArchiveHeader()
        header.version = ArchiveVersion.encrypted_version if self._encrypt else ArchiveVersion.default_version
        header.key = 0xCAFEBABE
        header.data_size = sum([v[1] for v in self.files])
        header.file_size = self._output_archive.stat().st_size + len(self.entries) * 32 + len(self.chunks) * 32 + 40
        header.max_chunk_size = self._chunk_max_size
        header.chunk_table_size = len(self.chunks)
        header.content_table_size = len(self.entries)
        self._output_handle.seek(0)
        header.dump(self._output_handle, self._encrypt)
        for entry, _ in self.entries:
            entry.dump(self._output_handle, self._encrypt)
        for chunk in self.chunks:
            chunk.dump(self._output_handle, self._encrypt)

    def finish(self):
        self._output_handle.close()
        print('Done packing archive')

if __name__ == '__main__':
    a = ArchivePacker(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\7017f9bb9d52fc1c4433599203cc51b1',
                      '7017f9bb9d52fc1c4433599203cc51b1', False)
    a.collect_files()
    a.create_entries()
    a.create_chunks()
    a.write_archive()
    a.finish()
    pass
