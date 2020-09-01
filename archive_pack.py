import math
import os
import struct
from pathlib import Path
from struct import pack
from typing import List, Tuple

from ProjectDecima import ArchiveSet, Archive
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

        self._raw_chunk_buffer_path = self.arc_dir / 'RAW_BUFFER.tmp'
        self._compressed_chunk_buffer_path = self.arc_dir / 'CMP_BUFFER.tmp'

    def collect_files(self):
        print('Collecting bin files')
        for file in self.arc_dir.rglob('*.bin'):
            self.files.append((file, file.stat().st_size))
        self.files.sort(key=lambda a: a[1], reverse=True)
        print(f'Collected {len(self.files)}')

    def create_entries(self):
        print('Creating file entries')
        for file, file_size in self.files:
            entry = ArchiveEntry()
            entry.entry_id, entry.hash = [int(v) for v in file.stem.split('-')]
            entry.size = file_size
            entry.key_0 = ((entry.entry_id * entry.hash) ^ 0xFEEEDECE) & 0xFFFFFFFF
            entry.key_1 = ((entry.entry_id * entry.hash) ^ 0xAEBECEDE) & 0xFFFFFFFF
            self.entries.append((entry, file))
            pass
        print(f'Created {len(self.entries)} file entries')

    def dump_to_temp_file(self):
        print('Creating temporary buffer')
        entry_count = len(self.entries)
        with self._raw_chunk_buffer_path.open('wb') as raw_buffer:
            for i, (entry, file) in enumerate(self.entries):
                print(f'\rDumping {i + 1}/{entry_count} files', end='')
                with file.open('rb') as f:
                    entry.offset = raw_buffer.tell()
                    raw_buffer.write(f.read(-1))
            print('\n')
        print(f'Created temporary buffer')

    def create_chunks(self):
        print('Creating chunks')
        total_data_size = sum([v[1] for v in self.files])
        estimated_chunk_count = math.ceil(total_data_size / self._chunk_max_size)
        chunk_data_start_offset = len(self.entries) * 32 + estimated_chunk_count * 32 + 32+8
        with self._compressed_chunk_buffer_path.open('wb') as compressed_buffer:
            with self._raw_chunk_buffer_path.open('rb') as raw_buffer:
                for i in range(estimated_chunk_count):
                    print(f'\rCompressing {i + 1}/{estimated_chunk_count} chunk', end='')
                    chunk = ArchiveChunk()
                    chunk.uncompressed_offset = raw_buffer.tell()
                    raw_data = raw_buffer.read(self._chunk_max_size)
                    chunk.uncompressed_size = len(raw_data)

                    compressed_data = Oodle.compress(raw_data)
                    chunk.compressed_size = len(compressed_data)
                    chunk.compressed_offset = chunk_data_start_offset+compressed_buffer.tell()

                    chunk.key_0 = (chunk.uncompressed_size ^ chunk.uncompressed_offset) & 0xFFFFFFFF
                    chunk.key_1 = (chunk.compressed_size ^ chunk.compressed_offset) & 0xFFFFFFFF

                    if self._encrypt:
                        compressed_data = self._encrypt_chunk(chunk, compressed_data)
                    compressed_buffer.write(compressed_data)

                    self.chunks.append(chunk)
                print('\n')
        print(f'Created {estimated_chunk_count} chunks')

    def _encrypt_chunk(self, chunk: ArchiveChunk, chunk_data: bytes):
        key = pack('Q2I', chunk.uncompressed_offset, chunk.uncompressed_size, chunk.key_0)
        chunk_data = decrypt_chunk_data(chunk_data, key)
        return chunk_data

    def write_archive(self):
        header = ArchiveHeader()
        header.version = ArchiveVersion.encrypted_version if self._encrypt else ArchiveVersion.default_version
        header.key = 0xCAFEBABE
        header.data_size = sum([v[1] for v in self.files])
        header.file_size = self._compressed_chunk_buffer_path.stat().st_size + len(self.entries) * 32 + len(
            self.chunks) * 32 + 36
        header.max_chunk_size = self._chunk_max_size
        header.chunk_table_size = len(self.chunks)
        header.content_table_size = len(self.entries)
        with open(self.arc_dir / f'{self.name}.bin.repack', 'wb') as arc:
            header.dump(arc, self._encrypt)
            for entry, _ in self.entries:
                entry.dump(arc, self._encrypt)
            for chunk in self.chunks:
                chunk.dump(arc, self._encrypt)
            with self._compressed_chunk_buffer_path.open('rb') as f:
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    arc.write(data)

    def finish(self):
        if self._compressed_chunk_buffer_path.exists():
            os.remove(self._compressed_chunk_buffer_path)
        if self._raw_chunk_buffer_path.exists():
            os.remove(self._raw_chunk_buffer_path)


if __name__ == '__main__':
    a = ArchivePacker(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\477e458b2c825633499874678a2b9ea5',
                      '477e458b2c825633499874678a2b9ea5', False)
    a.collect_files()
    a.create_entries()
    a.dump_to_temp_file()
    a.create_chunks()
    a.write_archive()
    a.finish()
    pass
