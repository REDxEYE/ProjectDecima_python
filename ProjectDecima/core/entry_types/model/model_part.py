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


class ArtPartsSubModelResource(ModelPartResource):
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


EntryTypeManager.register_handler(ArtPartsSubModelResource)
