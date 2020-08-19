from enum import IntEnum
from pathlib import Path
from typing import List
from uuid import UUID

from . import CoreDummy
from ..pod.strings import HashedString
from ...byte_io_ds import ByteIODS


class Bone:
    def __init__(self):
        self.name = HashedString()
        self.parent = 0

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()
        self.parent = reader.read_int16()

    def __repr__(self):
        return f'<Bone "{self.name}" prnt:{self.parent}>'


class UnkData0:
    def __init__(self):
        self.name = HashedString()
        self.bone_id = 0
        self.unk_1 = 0

    def parse(self, reader: ByteIODS):
        self.name = reader.read_hashed_string()
        self.bone_id, self.unk_1 = reader.read_fmt('2I')


class UnkData1:
    def __init__(self):
        self.unk_0 = 0
        self.unk_1 = 0

    def parse(self, reader: ByteIODS):
        self.unk_0, self.unk_1 = reader.read_fmt('QI')


class Armature(CoreDummy):

    def __init__(self):
        super().__init__()
        self.bones: List[Bone] = []
        self.unk_0 = 0
        self.unk_data_0: List[UnkData0] = []
        self.unk_data_1: List[UnkData1] = []
        self.unks_1 = []
        self.unks_2 = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        bone_count = reader.read_uint32()
        for _ in range(bone_count):
            bone = Bone()
            bone.parse(reader)
            self.bones.append(bone)
        unk_0_count = reader.read_uint32()
        self.unk_0 = reader.read_uint32()
        for _ in range(unk_0_count):
            unk = UnkData0()
            unk.parse(reader)
            self.unk_data_0.append(unk)
        for _ in range(unk_0_count):
            unk = UnkData1()
            unk.parse(reader)
            self.unk_data_1.append(unk)
        self.unks_2 = reader.read_fmt('20I')
        unks_2_count = reader.read_uint32()
        self.unks_2 = reader.read_fmt(f'{unks_2_count}H')
