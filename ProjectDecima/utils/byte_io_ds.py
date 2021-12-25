from .byte_io import ByteIO


class ByteIODS(ByteIO):

    def read(self, t):
        return super().read('<' + t)

    def range32(self):
        return range(self.read_uint32())
