from pathlib import Path
from uuid import UUID

from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io_ds import ByteIODS
from ...core.pod.core_header import CoreHeader


class CoreDummy:
    magic = 0xFFFF_FFFF_FFFF_FFFF
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


EntryTypeManager.set_default(CoreDummy)


class CoreDummy_60(CoreDummy):
    magic = 0x2F8D786D07E19A72

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(60)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 16)


EntryTypeManager.register_handler(CoreDummy_60, CoreDummy_60.magic)


class CoreDummy_4(CoreDummy):
    magic = 0x3650BFD5E3DDF318

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(4)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 20)


EntryTypeManager.register_handler(CoreDummy_4, CoreDummy_4.magic)
EntryTypeManager.register_handler(CoreDummy_4, 0xE59AB7DFD80B9421)
EntryTypeManager.register_handler(CoreDummy_4, 0x8FAA995D50547F10)
EntryTypeManager.register_handler(CoreDummy_4, 0xFF5B35CA05453AC)
