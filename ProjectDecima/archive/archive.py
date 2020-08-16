from pathlib import Path
from enum import IntEnum
from struct import pack, unpack
from typing import List, Dict

import numpy as np

from ..byte_io_ds import ByteIODS
from ..constants import encryption_key_1, encryption_key_2, seed
from ..utils.decryption import dectypt


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
        input_key = [pack('4I', *[self.key, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]]),
                     pack('4I', *[self.key + 1, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]])]
        data = np.array(data, dtype=np.uint32)
        dectypt(input_key, data)

        (self.file_size, self.data_size, self.content_table_size,
         self.chunk_table_size,
         self.max_chunk_size) = unpack('3Q2I', pack('8I', *data))


class ArchiveChunk:
    encrypted = False

    @classmethod
    def set_enctypted_flag(cls, flag):
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
        key_1 = data[7]
        input_key = [pack('4I', *[key_0, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]]),
                     pack('4I', *[key_1, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]])]
        data = np.array(data, dtype=np.uint32)
        dectypt(input_key, data)

        (self.uncompressed_offset, self.uncompressed_size, self.key_0, self.compressed_offset, self.compressed_size,
         self.key_1) = unpack('Q2IQ2I', pack('8I', *data))
        self.key_0 = key_0


class ArchiveEntry:
    encrypted = False

    @classmethod
    def set_enctypted_flag(cls, flag):
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
        key_0 = data[1]
        key_1 = data[7]
        input_key = [pack('4I', *[key_0, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]]),
                     pack('4I', *[key_1, encryption_key_1[1], encryption_key_1[2], encryption_key_1[3]])]
        data = np.array(data, dtype=np.uint32)
        dectypt(input_key, data)

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
        ArchiveEntry.set_enctypted_flag(self.is_encrypted)
        for _ in range(self.header.content_table_size):
            entry = ArchiveEntry()
            entry.parse(reader)
            self.hash_to_entry[entry.hash] = entry
        ArchiveChunk.set_enctypted_flag(self.is_encrypted)
        for _ in range(self.header.chunk_table_size):
            chunk = ArchiveChunk()
            chunk.parse(reader)
            self.chunks.append(chunk)
