from typing import List
from uuid import UUID

from . import CoreDummy
from ..pod.strings import HashedString
from ..entry_reference import EntryReference
from ...byte_io_ds import ByteIODS


class CoreModel(CoreDummy):

    def __init__(self, core_file):
        super().__init__(core_file)

        self.unk: List[int] = []
        self.unk1 = 0
        self.armature_reference = EntryReference(core_file)
        self.bone_data_ref = EntryReference(core_file)
        self.unk_entry_ref = EntryReference(core_file)
        self.floats = []
        self.vertex_data_info_ref = EntryReference(core_file)
        self.guids_1 = []
        self.materials = []
        self.mesh_stream = HashedString(0, '')
        self.self_guid = UUID(int=0)
        self.unks2 = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.unk = reader.read_fmt('12I')
        self.armature_reference.parse(reader)
        reader.skip(9)
        self.bone_data_ref.parse(reader)
        self.unk_entry_ref.parse(reader)
        self.floats = reader.read_fmt('6f')
        self.vertex_data_info_ref.parse(reader)
        unk_guid_count = reader.read_uint32()
        for _ in range(unk_guid_count):
            ref = EntryReference(self._core_file)
            ref.parse(reader)
            self.guids_1.append(ref)
        unk_guid_count = reader.read_uint32()
        for _ in range(unk_guid_count):
            ref = EntryReference(self._core_file)
            ref.parse(reader)
            self.materials.append(ref)
        reader.skip(1)
        self.mesh_stream = reader.read_unhashed_string()
        self.self_guid = reader.read_guid()
        self.unks2 = reader.read_fmt('3I')
