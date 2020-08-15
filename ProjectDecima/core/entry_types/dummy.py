from ...byte_io_ds import ByteIODS
from ProjectDecima.core.core import CoreHeader


class CoreDummy:
    def __init__(self, core_file):
        from ...core_file import CoreFile
        self._core_file: CoreFile = core_file
        self.header = CoreHeader()

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        reader.skip(self.header.size - 16)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.header.guid}>'
