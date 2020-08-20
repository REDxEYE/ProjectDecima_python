from ...utils.byte_io_ds import ByteIODS
from ...core.pod.core_header import CoreHeader


class CoreDummy:
    def __init__(self,):
        self.header = CoreHeader()

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        reader.skip(self.header.size - 16)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.header.guid}>'
