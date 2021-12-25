from abc import ABC

from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.core.pod.base_type import RTTIType


class RTTIString(RTTIType, str):
    pass


class HashedString(RTTIString):

    def __new__(cls, string='', string_hash=0, *args, **kwargs):
        new_str = super(HashedString, cls).__new__(cls, string)
        new_str.hash = string_hash
        return new_str

    def __init__(self, string='', string_hash=0):
        self.hash = string_hash

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        size = buffer.read_uint32()
        if size:
            hs = buffer.read_uint32()
            return cls(buffer.read_bytes(size).decode('utf'), hs)

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(len(self))
        if self:
            buffer.write_uint32(self.hash)
            buffer.write_bytes(self.encode('utf8'))

    def __repr__(self):
        return f'HashedString({str(self)!r},{self.hash}'


class UnHashedString(RTTIString):

    def __new__(cls, string='', *args, **kwargs):
        return super(UnHashedString, cls).__new__(cls, string)

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        size = buffer.read_uint32()
        if size:
            return cls(buffer.read_bytes(size).decode('utf'))

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(len(self))
        if self:
            buffer.write_bytes(self.encode('utf8'))


class WUnHashedString(RTTIString):

    def __new__(cls, string='', *args, **kwargs):
        return super(WUnHashedString, cls).__new__(cls, string)

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        size = buffer.read_uint32() * 2
        if size:
            return cls(buffer.read_bytes(size).decode('utf-16'))

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(len(self))
        if self:
            buffer.write_bytes(self.encode('utf-16'))
