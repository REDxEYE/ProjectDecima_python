from typing import List

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ...core.stream_reference import StreamReference
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class CoreModel(CoreDummy):
    magic = 0xE2A812418ABC2172

    def __init__(self):
        super().__init__()

        self.static_data_block_size = 0
        self.bbox = []
        self.cull_info = 0
        self.mesh_hierarchy_info = MeshHierarchyInfo()
        self.skeleton = EntryReference()
        self.orientation_helpers = EntryReference()
        self.deformer_type = ESkinningDeformerType.DeformPosAndNormals
        self.skinned_mesh_joints_bindings = EntryReference()
        self.skinned_mesh_bone_bboxes = EntryReference()
        self.position_bounds_scale = []
        self.position_bounds_offset = []
        self.skin_info = EntryReference()
        self.primitives = []
        self.shading_groups = []
        self.render_effect_swapper = EntryReference()
        self.mesh_stream = StreamingDataSource()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk = reader.read_fmt('12I')
        self.armature_reference.parse(reader, core_file)
        reader.skip(9)
        self.bone_data_ref.parse(reader, core_file)
        self.unk_entry_ref.parse(reader, core_file)
        self.floats = reader.read_fmt('6f')
        self.vertex_data_info_ref.parse(reader, core_file)
        unk_guid_count = reader.read_uint32()
        for _ in range(unk_guid_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.mesh_info_ref.append(ref)
        unk_guid_count = reader.read_uint32()
        for _ in range(unk_guid_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.materials.append(ref)
        reader.skip(1)
        self.mesh_stream.parse(reader)


EntryTypeManager.register_handler(CoreModel)
