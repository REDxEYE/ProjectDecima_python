from enum import IntEnum
from typing import List

from ProjectDecima.core.entry_types import CoreDummy
from ProjectDecima.core.entry_types.resource import Resource, ResourceWithNameHash
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.core.entry_reference import EntryReference


class SkinnedMeshBoneBoundingBoxes(Resource):
    magic = 0x118378C2F191097A

    def __init__(self):
        super().__init__()
        self.bone_bbox = []
        self.indices = []
        self.uses_indices = 0
        self.initialized = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.bone_bbox = [reader.read_fmt('6f') for _ in range(reader.read_uint32())]
        self.indices = [reader.read_uint16() for _ in range(reader.read_uint32())]
        self.uses_indices = reader.read_uint8()
        self.initialized = reader.read_uint8()

    def dump(self):
        return {
            'class': self.class_name,
            'bone_bbox': self.bone_bbox,
            'indices': self.indices,
            'uses_indices': self.uses_indices,
            'initialized': self.initialized,
        }


EntryTypeManager.register_handler(SkinnedMeshBoneBoundingBoxes)


class ArtPartsSubModelWithChildrenResource(ResourceWithNameHash):
    magic = 0x5D1FB9F0D8EA70F4

    def __init__(self):
        super().__init__()
        self.children: List[EntryReference] = []
        self.art_parts_sub_model_part_resource = EntryReference()
        self.hidden = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.children.append(ref)
        self.art_parts_sub_model_part_resource.parse(reader, core_file)
        self.hidden = reader.read_uint8()

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'children': [ch.dump() for ch in self.children],
            'art_parts_sub_model_part_resource': self.art_parts_sub_model_part_resource.dump(),
            'hidden': self.hidden
        })
        return out


EntryTypeManager.register_handler(ArtPartsSubModelWithChildrenResource)


class EPhysicsMotionType(IntEnum):
    Dynamic = 1
    Keyframed = 2
    Static = 3


class ERenderEffectAllocationMode(IntEnum):
    Private = 0
    Cached = 1


class ModelPartResource(ResourceWithNameHash):
    magic = 0xCDBCD0D1DCA09A23

    def __init__(self):
        super().__init__()
        self.mesh_resource = EntryReference()
        self.bone_bounding_boxes = EntryReference()
        self.physics_resource = EntryReference()
        self.part_motion_type = EPhysicsMotionType.Dynamic
        self.helper_node = HashedString()
        self.render_effect_allocation_mode = ERenderEffectAllocationMode.Private

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.mesh_resource.parse(reader, core_file)
        self.bone_bounding_boxes.parse(reader, core_file)
        self.physics_resource.parse(reader, core_file)
        self.helper_node = reader.read_hashed_string()
        self.render_effect_allocation_mode = ERenderEffectAllocationMode(reader.read_uint32())

    def dump(self) -> dict:
        out = super().dump()
        out.update({
            'class': self.class_name,
            'mesh_resource': self.mesh_resource.dump(),
            'bone_bounding_boxes': self.bone_bounding_boxes.dump(),
            'physics_resource': self.physics_resource.dump(),
            'part_motion_type': self.part_motion_type.value,
            'helper_node': self.helper_node,
            'render_effect_allocation_mode': self.render_effect_allocation_mode.value,
        })
        return out


class EArtPartsSubModelKind(IntEnum):
    NONE = 0
    Cover = 1
    CoverAndAnim = 2


class ArtPartsSubModelResource(ModelPartResource):
    magic = 0x2ED3FA0EE459E5AC

    def __init__(self):
        super().__init__()
        self.helper_resource = EntryReference()
        self.skinned_model_pose_deformer_resource = EntryReference()
        self.skeleton = EntryReference()
        self.local_offset_matrix = []
        self.extra_resource = EntryReference()
        self.model_kind = EArtPartsSubModelKind.NONE
        self.is_hide_default = False

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.helper_resource.parse(reader, core_file)
        self.skinned_model_pose_deformer_resource.parse(reader, core_file)
        self.skeleton.parse(reader, core_file)
        self.local_offset_matrix = reader.read_fmt('16f')
        self.extra_resource.parse(reader, core_file)
        self.model_kind = EArtPartsSubModelKind(reader.read_uint32())
        self.is_hide_default = reader.read_uint8()

    def dump(self) -> dict:
        out = super().dump()
        out.update({
            'class': self.class_name,
            'helper_resource': self.helper_resource.dump(),
            'skinned_model_pose_deformer_resource': self.skinned_model_pose_deformer_resource.dump(),
            'local_offset_matrix': self.local_offset_matrix,
            'skeleton': self.extra_resource.dump(),
            'extra_resource': self.extra_resource.dump(),
            'model_kind': self.model_kind.value,
            'is_hide_default': self.is_hide_default,
        })
        return out


EntryTypeManager.register_handler(ArtPartsSubModelResource)
