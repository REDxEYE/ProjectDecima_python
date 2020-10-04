from enum import IntEnum
from typing import List

from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.entry_types.resource import Resource
from ProjectDecima.core.entry_types.rtti_object import EntityComponentResource
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.core.stream_reference import StreamingDataSource
from ProjectDecima.utils.byte_io_ds import ByteIODS


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

    def dump(self):
        return {
            'class': self.__class__.__name__,
            'mit_node_size': self.mit_node_size,
            'primitive_count': self.primitive_count,
            'mesh_count': self.mesh_count,
            'static_mesh_count': self.static_mesh_count,
            'lod_mesh_count': self.lod_mesh_count,
            'packed_data': self.packed_data,
        }


class MeshResourceBase(Resource):
    magic = 0x2879C7EF5EAF5865

    def __init__(self):
        super().__init__()
        self.static_data_block_size = 0
        self.bounding_box = []
        self.cull_info = 0
        self.mesh_hierarchy_info = MeshHierarchyInfo()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.static_data_block_size = reader.read_uint32()
        self.bounding_box = (reader.read_fmt('3f'), reader.read_fmt('3f'))
        self.cull_info = reader.read_uint32()
        self.mesh_hierarchy_info.parse(reader)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'static_data_block_size': self.static_data_block_size,
            'bounding_box': self.bounding_box,
            'cull_info': self.cull_info,
            'mesh_hierarchy_info': self.mesh_hierarchy_info.dump(),
        })
        return out


EntryTypeManager.register_handler(MeshResourceBase)


class EViewLayer(IntEnum):
    Background = 0
    Default = 1
    FirstPerson = 2
    Overlay = 3


class EActiveView(IntEnum):
    NONE = -1
    Default = 0
    ThirdPerson = 1
    FirstPerson = 2


class ModelResource(EntityComponentResource):
    magic = 0x885C3466410310D9

    def __init__(self):
        super().__init__()
        self.model_part_resources: List[EntryReference] = []
        self.art_parts_resources = EntryReference()
        self.view_layer = EViewLayer.Background
        self.active_view = EActiveView.NONE
        self.helpers: List[EntryReference] = []
        self.helper_name = HashedString()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.model_part_resources.append(ref)
        self.art_parts_resources.parse(reader, core_file)
        self.view_layer = EViewLayer(reader.read_uint32())
        self.active_view = EActiveView(reader.read_int32())
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.helpers.append(ref)
        self.helper_name = reader.read_hashed_string()

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'model_part_resources': [part.dump() for part in self.model_part_resources],
            'art_parts_resources': self.art_parts_resources.dump(),
            'view_layer': self.view_layer.value,
            'active_view': self.active_view.value,
            'helpers': [helper.dump() for helper in self.helpers],
            'helper_name': self.helper_name,
        })
        return out


class SkinnedModelResource(ModelResource):
    magic = 0xBC79DACC10E13CB7

    def __init__(self):
        super().__init__()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)


EntryTypeManager.register_handler(SkinnedModelResource)


class ESkinningDeformerType(IntEnum):
    DeformPosAndNormals = 0
    DeformPosAndComputeNormals = 1


class SkinnedMeshResource(MeshResourceBase):
    magic = 0xC8D223289354D443

    def __init__(self):
        super().__init__()
        self.skeleton = EntryReference()
        self.orientation_helpers = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.skeleton.parse(reader, core_file)
        self.orientation_helpers.parse(reader, core_file)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'skeleton': self.skeleton.dump(),
            'orientation_helpers': self.orientation_helpers.dump(),
        })
        return out


EntryTypeManager.register_handler(SkinnedMeshResource)


class RegularSkinnedMeshResourceBase(SkinnedMeshResource):
    magic = 0xD40C19AE1D16D98E

    def __init__(self):
        super().__init__()
        self.draw_flags = 0
        self.deformer_type = ESkinningDeformerType.DeformPosAndNormals
        self.skinned_mesh_joints_bindings = EntryReference()
        self.skinned_mesh_bone_bboxes = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.draw_flags = reader.read_uint32()
        self.deformer_type = ESkinningDeformerType(reader.read_uint32())
        self.skinned_mesh_joints_bindings.parse(reader, core_file)
        self.skinned_mesh_bone_bboxes.parse(reader, core_file)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'draw_flags': self.draw_flags,
            'deformer_type': self.deformer_type.value,
            'skinned_mesh_joints_bindings': self.skinned_mesh_joints_bindings.dump(),
            'skinned_mesh_bone_bboxes': self.skinned_mesh_bone_bboxes.dump(),
        })
        return out


EntryTypeManager.register_handler(RegularSkinnedMeshResourceBase)


class RegularSkinnedMeshResource(RegularSkinnedMeshResourceBase):
    magic = 0xE2A812418ABC2172

    def __init__(self):
        super().__init__()

        self.position_bounds_scale = []
        self.position_bounds_offset = []
        self.skin_info = EntryReference()
        self.primitives: List[EntryReference] = []
        self.shading_groups: List[EntryReference] = []
        self.render_effect_swapper = EntryReference()
        self.mesh_stream = StreamingDataSource()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.position_bounds_scale = reader.read_fmt('3f')
        self.position_bounds_offset = reader.read_fmt('3f')
        self.skin_info.parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.primitives.append(ref)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.shading_groups.append(ref)
        self.render_effect_swapper.parse(reader, core_file)
        self.mesh_stream.parse(reader)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'position_bounds_scale': self.position_bounds_scale,
            'position_bounds_offset': self.position_bounds_offset,
            'mesh_stream': self.mesh_stream.dump(),
            'primitives': [prim.dump() for prim in self.primitives],
            'materials': [shd.dump() for shd in self.shading_groups],
        })
        return out


EntryTypeManager.register_handler(RegularSkinnedMeshResource)
