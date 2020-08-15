from . import CoreDummy
from ...byte_io_ds import ByteIODS


class CoreShader(CoreDummy):

    def parse(self, reader: ByteIODS):
        super().parse(reader)
