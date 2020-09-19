from typing import List, Dict, Tuple

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ..pod.strings import HashedString
from ...utils.byte_io_ds import ByteIODS


class Joint:
    def __init__(self):
        self.name = HashedString()
        self.parent = 0

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()
        self.parent = reader.read_int16()

    def __repr__(self):
        return f'<Bone "{self.name}" prnt:{self.parent}>'


class SkeletonAnimChannel:
    def __init__(self):
        self.name = HashedString()

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()

    def __repr__(self):
        return f'<AnimChannel "{self.name}">'


class Skeleton(CoreDummy):
    magic = 0x11E1D1A40B933E66

    def __init__(self):
        super().__init__()
        self.joints: List[Joint] = []
        self.joint_name_to_index: Dict[str, Tuple[HashedString, int]] = {}
        self.joint_name_hash_to_index: Dict[int, Tuple[int, int]] = {}
        self.animation_channels: List[SkeletonAnimChannel] = []
        self.anim_channel_name_to_handle: Dict[str, Tuple[HashedString, int]] = {}
        self.skeleton_layout_hash = 0
        self.skeleton_channel_layout_hash = 0
        self.edge_anim_skeleton:List[int] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        array_size = reader.read_uint32()
        for _ in range(array_size):
            joint = Joint()
            joint.parse(reader)
            self.joints.append(joint)
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            key = reader.read_uint32()
            self.joint_name_to_index[key] = (reader.read_hashed_string(), reader.read_int32())
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            key = reader.read_uint32()
            self.joint_name_hash_to_index[key] = (reader.read_uint32(), reader.read_int32())
        animation_channels_count = reader.read_uint32()
        for _ in range(animation_channels_count):
            anim_channel = SkeletonAnimChannel()
            anim_channel.parse(reader)
            self.animation_channels.append(anim_channel)
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            key = reader.read_uint32()
            self.anim_channel_name_to_handle[key] = (reader.read_hashed_string(), reader.read_int32())
        self.skeleton_layout_hash = reader.read_uint32()
        self.skeleton_channel_layout_hash = reader.read_uint32()
        array_size = reader.read_uint32()
        self.edge_anim_skeleton = list(reader.read_fmt(f'{array_size}B'))

EntryTypeManager.register_handler(Skeleton)


class ArmatureReference(CoreDummy):
    magic = 0xb1d37c8f8304785b

    def __init__(self):
        super().__init__()
        self.unk_entry_ref = EntryReference()
        self.armature_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_entry_ref.parse(reader, core_file)
        self.armature_ref.parse(reader, core_file)


EntryTypeManager.register_handler(ArmatureReference)
