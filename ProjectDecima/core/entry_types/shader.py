from . import CoreDummy
from ...utils.byte_io_ds import ByteIODS


class CoreShader(CoreDummy):

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, None)
