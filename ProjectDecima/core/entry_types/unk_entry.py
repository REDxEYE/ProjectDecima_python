from typing import List

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class BoneRelatedEntry(CoreDummy):
    magic = 0x118378C2F191097A

    def __init__(self):
        super().__init__()
        self.unk_0_count = 0
        self.unk_0_floats = []
        self.unk_1_count = 0
        self.bone_remap = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0_count = reader.read_uint32()
        self.unk_0_floats = [reader.read_fmt('6f') for _ in range(self.unk_0_count)]
        self.unk_1_count = reader.read_uint32()
        self.bone_remap = reader.read_fmt(f'{self.unk_1_count}H')


EntryTypeManager.register_handler(BoneRelatedEntry)


class UnkEntry(CoreDummy):
    magic = 0x5D1FB9F0D8EA70F4

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.ref_count = 0
        self.refs: List[EntryReference] = []
        self.ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0, self.ref_count = reader.read_fmt('2I')
        for _ in range(self.ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)
        self.ref.parse(reader, core_file)


EntryTypeManager.register_handler(UnkEntry)


class UnkEntry2(CoreDummy):
    magic = 0x2ED3FA0EE459E5AC

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.part_mesh_ref = EntryReference()
        self.ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        no_second_guid = False
        if reader.peek_int16() == 0:
            no_second_guid = True
            reader.skip(2)
        self.part_mesh_ref.parse(reader, core_file)
        if not no_second_guid:
            self.ref.parse(reader, core_file)
        reader.skip(82 + int(not no_second_guid))


EntryTypeManager.register_handler(UnkEntry2)

