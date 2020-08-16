from pathlib import Path
from enum import IntEnum
from struct import pack, unpack
from typing import List, Dict, Union

import numpy as np

from ..byte_io_ds import ByteIODS
from ..constants import encryption_key_1
from ..core_file import CoreFile
from ..utils.chunk_utils import calculate_first_containing_chunk, calculate_last_containing_chunk
from ..utils.decryption import decrypt, hash_string, decrypt_chunk_data
from ..utils.oodle_wrapper import Oodle


class ArchiveVersion(IntEnum):
    unknown = 0
    default_version = 0x20304050
    encrypted_version = 0x21304050


class ArchiveHeader:
    def __init__(self):
        self.version = ArchiveVersion(0)
        self.key = 0
        self.file_size = 0
        self.data_size = 0
        self.content_table_size = 0
        self.chunk_table_size = 0
        self.max_chunk_size = 0

    def parse(self, reader: ByteIODS):
        self.version = ArchiveVersion(reader.read_uint32())
        self.key = reader.read_uint32()
        if self.version == ArchiveVersion.encrypted_version:
            self.decrypt(reader.read_fmt('8I'))
        else:
            self.file_size = reader.read_uint64()
            self.data_size = reader.read_uint64()
            self.content_table_size = reader.read_uint64()
            self.chunk_table_size = reader.read_uint32()
            self.max_chunk_size = reader.read_uint32()

    def decrypt(self, data):
        input_key = [pack('4I', self.key, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]),
                     pack('4I', self.key + 1, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3])]
        data = np.array(data, dtype=np.uint32)
        data = decrypt(input_key, data)

        (self.file_size, self.data_size, self.content_table_size,
         self.chunk_table_size,
         self.max_chunk_size) = unpack('3Q2I', pack('8I', *data))


class ArchiveChunk:
    encrypted = False

    @classmethod
    def set_encrypted_flag(cls, flag):
        cls.encrypted = flag

    def __init__(self):
        self.uncompressed_offset = 0
        self.uncompressed_size = 0
        self.key_0 = 0
        self.compressed_offset = 0
        self.compressed_size = 0
        self.key_1 = 0

    def parse(self, reader: ByteIODS):
        if self.encrypted:
            self.decrypt(reader.read_fmt('8I'))
        else:
            (self.uncompressed_offset, self.uncompressed_size, self.key_0, self.compressed_offset, self.compressed_size,
             self.key_1) = reader.read_fmt('Q2IQ2I')

    def decrypt(self, data):
        key_0 = data[3]
        input_key = [pack('4I', data[3], encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]),
                     pack('4I', data[7], encryption_key_1[1], encryption_key_1[2], encryption_key_1[3])]
        data = np.array(data, dtype=np.uint32)
        data = decrypt(input_key, data)

        (self.uncompressed_offset, self.uncompressed_size, self.key_0, self.compressed_offset, self.compressed_size,
         self.key_1) = unpack('Q2IQ2I', pack('8I', *data))
        self.key_0 = key_0


class ArchiveEntry:
    encrypted = False

    @classmethod
    def set_encrypted_flag(cls, flag):
        cls.encrypted = flag

    def __init__(self):
        self.entry_num = 0
        self.key_0 = 0
        self.hash = 0
        self.offset = 0
        self.size = 0
        self.key_1 = 0

    def parse(self, reader: ByteIODS):
        if self.encrypted:
            self.decrypt(reader.read_fmt('8I'))
        else:
            (self.entry_num, self.key_0, self.hash, self.offset, self.size, self.key_1) = reader.read_fmt('2I2Q2I')

    def decrypt(self, data):
        input_key = [pack('4I', data[1], encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]),
                     pack('4I', data[7], encryption_key_1[1], encryption_key_1[2], encryption_key_1[3])]
        data = np.array(data, dtype=np.uint32)
        data = decrypt(input_key, data)

        (self.entry_num, self.key_0, self.hash, self.offset, self.size, self.key_1) = unpack('2I2Q2I',
                                                                                             pack('8I', *data))


class Archive:

    def __init__(self, filepath):
        self.header = ArchiveHeader()
        self.filepath = Path(filepath)
        self.reader = ByteIODS(filepath)
        self.chunks: List[ArchiveChunk] = []
        self.hash_to_entry: Dict[int, ArchiveEntry] = {}

    @property
    def is_encrypted(self):
        return self.header.version == ArchiveVersion.encrypted_version

    def parse(self):
        reader = self.reader
        self.header.parse(reader)
        ArchiveEntry.set_encrypted_flag(self.is_encrypted)
        for _ in range(self.header.content_table_size):
            entry = ArchiveEntry()
            entry.parse(reader)
            self.hash_to_entry[entry.hash] = entry
        ArchiveChunk.set_encrypted_flag(self.is_encrypted)
        for _ in range(self.header.chunk_table_size):
            chunk = ArchiveChunk()
            chunk.parse(reader)
            self.chunks.append(chunk)

    def get_chunk_boundaries(self, file_id: int):
        if file_id == -1:
            return -1, -1

        file_entry = self.hash_to_entry.get(file_id)

        file_offset = file_entry.offset
        file_size = file_entry.size

        first_chunk = calculate_first_containing_chunk(file_offset, self.header.max_chunk_size)
        last_chunk = calculate_last_containing_chunk(file_offset, file_size, self.header.max_chunk_size)

        first_chunk_row = self.chunk_id_by_offset(first_chunk)
        last_chunk_row = self.chunk_id_by_offset(last_chunk)
        return first_chunk_row, last_chunk_row

    def chunk_id_by_offset(self, offset):
        for i, chunk in enumerate(self.chunks):
            if chunk.uncompressed_offset == offset:
                return i

        return -1

    def get_file_data(self, entry: ArchiveEntry):
        first_chunk, last_chunk = self.get_chunk_boundaries(entry.hash)
        total_data = bytearray()
        output_size = 0
        input_size = 0
        for i in range(first_chunk, last_chunk + 1):
            chunk = self.chunks[i]
            self.reader.seek(chunk.compressed_offset)
            chunk_data = self.reader.read_bytes(chunk.compressed_size)
            if self.is_encrypted:
                key = pack('Q2I', chunk.uncompressed_offset, chunk.uncompressed_size, chunk.key_0)
                chunk_data = decrypt_chunk_data(chunk_data, key)
            total_data.extend(chunk_data)
            output_size += chunk.uncompressed_size
            input_size += chunk.compressed_size
        file_position = entry.offset % self.header.max_chunk_size
        decompressed_data = Oodle.decompress(total_data, output_size)

        return decompressed_data[file_position:file_position + entry.size]

    def queue_file(self, file_id: Union[str, int], is_core_file=True):
        if isinstance(file_id, str):
            file_name = file_id
            file_id = hash_string(file_id)
        else:
            file_name = str(file_id)
        file_entry = self.hash_to_entry.get(file_id, None)
        if file_entry:
            if is_core_file:
                core_file = CoreFile(self.get_file_data(file_entry), file_name)
                core_file.parse()
                return core_file
            else:
                return self.get_file_data(file_entry)

        return None
