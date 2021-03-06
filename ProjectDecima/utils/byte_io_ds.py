from .byte_io import ByteIO
from uuid import UUID

from ..core.pod.strings import HashedString, UnHashedString


class ByteIODS(ByteIO):

    def read(self, t):
        return super().read('<' + t)

    def read_guid(self):
        return UUID(bytes_le=self.read_bytes(16))

    def read_hashed_string(self):
        size = self.read_uint32()
        if size:
            hs = self.read_uint32()
            return HashedString(self.read_bytes(size).decode('utf'), hs)
        return HashedString('', 0)

    def read_unhashed_string(self):
        size = self.read_uint32()
        if size:
            return UnHashedString(self.read_bytes(size).decode('utf'))
        return UnHashedString('')

    def read_ref(self, core_file):
        from ..core.entry_reference import EntryReference
        ref = EntryReference()
        ref.parse(self, core_file)
        return ref

    def range32(self):
        return range(self.read_uint32())
