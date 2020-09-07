from .byte_io import ByteIO
from uuid import UUID
from ..core.pod.strings import HashedString, UnHashedString


class ByteIODS(ByteIO):

    def read_guid(self):
        return UUID(bytes=self.read_bytes(16))

    def read_hashed_string(self):
        size, hs = self.read_fmt('2I')
        return HashedString(self.read_bytes(size).decode('utf'), hs)

    def read_unhashed_string(self):
        size = self.read_uint32()
        return UnHashedString(self.read_bytes(size).decode('utf'))
