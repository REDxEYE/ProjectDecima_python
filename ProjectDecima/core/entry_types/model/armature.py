from typing import List, Dict, Tuple

from ProjectDecima.core.entry_types import CoreDummy
from ProjectDecima.core.entry_types.resource import Resource
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.utils.byte_io_ds import ByteIODS


class Joint:
    def __init__(self):
        self.name = HashedString()
        self.parent = 0

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()
        self.parent = reader.read_int16()

    def dump(self):
        return {
            'name': self.name,
            'parent': self.parent,
        }

    def __repr__(self):
        return f'<Bone "{self.name}" prnt:{self.parent}>'


class SkeletonAnimChannel:
    def __init__(self):
        self.name = HashedString()

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()

    def dump(self):
        return {
            'name': self.name,
        }

    def __repr__(self):
        return f'<AnimChannel "{self.name}">'


class Skeleton(Resource):
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
        self.edge_anim_skeleton: List[int] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            joint = Joint()
            joint.parse(reader)
            self.joints.append(joint)
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            reader.read_uint32()
            key = reader.read_hashed_string()
            self.joint_name_to_index[key] = reader.read_int32()
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            reader.read_uint32()
            key = reader.read_uint32()
            self.joint_name_hash_to_index[key] = reader.read_int32()
        animation_channels_count = reader.read_uint32()
        for _ in range(animation_channels_count):
            anim_channel = SkeletonAnimChannel()
            anim_channel.parse(reader)
            self.animation_channels.append(anim_channel)
        hash_map_len = reader.read_uint32()
        for _ in range(hash_map_len):
            reader.read_uint32()
            key = reader.read_hashed_string()
            self.anim_channel_name_to_handle[key] = reader.read_int32()
        self.skeleton_layout_hash = reader.read_uint32()
        self.skeleton_channel_layout_hash = reader.read_uint32()
        array_size = reader.read_uint32()
        self.edge_anim_skeleton = list(reader.read_fmt(f'{array_size}B'))

    def dump(self):
        return {
            'joints': [joint.dump() for joint in self.joints],
            'joint_name_to_index': self.joint_name_to_index,
            'joint_name_hash_to_index': self.joint_name_hash_to_index,
            'animation_channels': [ac.dump() for ac in self.animation_channels],
            'anim_channel_name_to_handle': self.anim_channel_name_to_handle,
            'skeleton_layout_hash': self.skeleton_layout_hash,
            'skeleton_channel_layout_hash': self.skeleton_channel_layout_hash,
            'edge_anim_skeleton': self.edge_anim_skeleton,
        }


EntryTypeManager.register_handler(Skeleton)


class DSCoverModelPreComputedResource(Resource):
    magic = 0xb1d37c8f8304785b

    def __init__(self):
        super().__init__()
        self.bbox = EntryReference()
        self.repr_skeleton = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.bbox.parse(reader, core_file)
        self.repr_skeleton.parse(reader, core_file)

    def dump(self) -> dict:
        return {
            'bbox': self.bbox.dump(),
            'repr_skeleton': self.repr_skeleton.dump(),
        }


EntryTypeManager.register_handler(DSCoverModelPreComputedResource)
