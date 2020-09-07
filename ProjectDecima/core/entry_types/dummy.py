from pathlib import Path
from uuid import UUID

from ...utils.byte_io_ds import ByteIODS
from ...core.pod.core_header import CoreHeader


class CoreDummy:
    exportable = False

    def __init__(self, ):
        self.header = CoreHeader()
        self.guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 16)

    def dump(self, output_path: Path):
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.guid}>'


class CoreDummy_60(CoreDummy):

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(60)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 16)


class CoreDummy_4(CoreDummy):

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(4)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 20)
