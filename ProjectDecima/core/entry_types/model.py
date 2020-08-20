from typing import List

from . import CoreDummy
from ...core.stream_reference import StreamReference
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class CoreModel(CoreDummy):

    def __init__(self):
        super().__init__()

        self.unk: List[int] = []
        self.unk1 = 0
        self.armature_reference = EntryReference()
        self.bone_data_ref = EntryReference()
        self.unk_entry_ref = EntryReference()
        self.floats = []
        self.vertex_data_info_ref = EntryReference()
        self.mesh_info_ref = []
        self.materials = []
        self.mesh_stream = StreamReference()

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
            ref = EntryReference()
            ref.parse(reader)
            self.mesh_info_ref.append(ref)
        unk_guid_count = reader.read_uint32()
        for _ in range(unk_guid_count):
            ref = EntryReference()
            ref.parse(reader)
            self.materials.append(ref)
        reader.skip(1)
        self.mesh_stream.parse(reader)
