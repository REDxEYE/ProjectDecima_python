from typing import List

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class UnkModelEntry(CoreDummy):
    magic = 0x9FC36C15337A680A

    def __init__(self):
        super().__init__()
        self.unk1 = 0
        self.model_refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        reader.skip(28)
        self.unk1 = reader.read_uint32()
        reader.skip(16)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            reader.skip(60)
            self.model_refs.append(ref)


EntryTypeManager.register_handler(UnkModelEntry)


class UnkModelEntry2(UnkModelEntry):
    magic = 0x36B88667B0A33134

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        reader.skip(28)
        self.unk1 = reader.read_uint32()
        reader.skip(20)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            reader.skip(4)
            self.model_refs.append(ref)


EntryTypeManager.register_handler(UnkModelEntry2)
