from enum import IntEnum
from typing import List

from ..dummy import CoreDummy
from ..resource import Resource, ResourceWithNameHash
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
        self.bone_bbox = [reader.read_fmt('6f') for _ in reader.range32()]
        self.indices = [reader.read_uint16() for _ in reader.range32()]
        self.uses_indices = reader.read_uint8()
        self.initialized = reader.read_uint8()



EntryTypeManager.register_handler(SkinnedMeshBoneBoundingBoxes)





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
        self.part_motion_type = EPhysicsMotionType(reader.read_uint32())
        self.helper_node = reader.read_hashed_string()
        self.render_effect_allocation_mode = ERenderEffectAllocationMode(reader.read_uint8())




EntryTypeManager.register_handler(ModelPartResource)



