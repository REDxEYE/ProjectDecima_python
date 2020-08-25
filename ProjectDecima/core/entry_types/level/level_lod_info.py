from enum import IntEnum
from typing import List

from .. import CoreDummy
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS
from ...pod.core_header import CoreHeader


class LevelTileLodInfo(CoreDummy):
    def __init__(self):
        super().__init__()
        self.lod_refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader, None)
        self.guid = reader.read_guid()

        lod_count = reader.read_uint32()
        for _ in range(lod_count):
            ref = EntryReference()
            ref.parse(reader, None)
            self.lod_refs.append(ref)


class LodLevel(IntEnum):
    DefaultRes = 3
    MiddleRes = 2
    LowRes = 1
    NoLod = 0


class LevelTileLod(CoreDummy):
    def __init__(self):
        super().__init__()
        self.lod_level = LodLevel(0)
        self.lod_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.lod_level = LodLevel(reader.read_uint8())
        self.lod_ref.parse(reader, core_file)


class LevelLodUnk(CoreDummy):
    def __init__(self):
        super().__init__()
        self.unks_0 = []
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unks_0 = reader.read_fmt('2i')
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)
