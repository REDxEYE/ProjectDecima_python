from typing import List
from uuid import UUID

from . import CoreDummy
from ...core.stream_reference import StreamReference
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class EntityModelInfo(CoreDummy):

    def __init__(self):
        super().__init__()
        self.ref_0 = EntryReference()
        self.ref_1 = EntryReference()
        self.refs_2: List[EntryReference] = []
        self.ref_3 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.ref_0.parse(reader, core_file)
        self.ref_1.parse(reader, core_file)
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs_2.append(ref)
        self.ref_3.parse(reader, core_file)


class EntityMeshInfo(CoreDummy):
    def __init__(self):
        super().__init__()
        self.part_ref = EntryReference()
        self.armature_ref = EntryReference()
        self.unk_ref = EntryReference()
        self.armature_ref_1 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        assert reader.read_uint32() == 0, 'Non zero INT32!'
        self.part_ref.parse(reader, core_file)
        assert reader.read_uint32() == 1
        assert sum(reader.read_fmt('12B')) == 0
        self.armature_ref.parse(reader, core_file)
        assert sum(reader.read_fmt('5B')) == 0
        self.unk_ref.parse(reader, core_file)
        self.armature_ref_1.parse(reader, core_file)
        assert sum(reader.read_fmt('10B')) == 0

