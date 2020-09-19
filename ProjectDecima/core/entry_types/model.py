from enum import IntEnum
from typing import List

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ...core.stream_reference import StreamingDataSource
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class ESkinningDeformerType(IntEnum):
    DeformPosAndNormals = 0
    DeformPosAndComputeNormals = 1


class MeshHierarchyInfo:
    def __init__(self):
        self.mit_node_size = 0
        self.primitive_count = 0
        self.mesh_count = 0
        self.static_mesh_count = 0
        self.lod_mesh_count = 0
        self.packed_data = 0

    def parse(self, reader: ByteIODS):
        (self.mit_node_size,
         self.primitive_count,
         self.mesh_count,
         self.static_mesh_count,
         self.lod_mesh_count,
         self.packed_data) = reader.read_fmt('2I4H')


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
        self.static_data_block_size = reader.read_uint32()
        self.bbox = (reader.read_fmt('3f'), reader.read_fmt('3f'))
        self.cull_info = reader.read_uint32()
        self.mesh_hierarchy_info.parse(reader)
        self.skeleton.parse(reader, core_file)
        self.orientation_helpers.parse(reader, core_file)
        reader.skip(7)
        self.deformer_type = ESkinningDeformerType(reader.read_uint8())
        self.skinned_mesh_joints_bindings.parse(reader, core_file)
        self.skinned_mesh_bone_bboxes.parse(reader, core_file)

        self.position_bounds_scale = reader.read_fmt('3f')
        self.position_bounds_offset = reader.read_fmt('3f')
        self.skin_info.parse(reader, core_file)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.primitives.append(ref)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.shading_groups.append(ref)
        self.render_effect_swapper.parse(reader, core_file)
        self.mesh_stream.parse(reader)


EntryTypeManager.register_handler(CoreModel)
