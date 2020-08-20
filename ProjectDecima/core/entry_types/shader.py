from . import CoreDummy
from ...utils.byte_io_ds import ByteIODS


class CoreShader(CoreDummy):

    def parse(self, reader: ByteIODS):
        super().parse(reader)
