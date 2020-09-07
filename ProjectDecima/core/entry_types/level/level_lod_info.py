from enum import IntEnum
from typing import List

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS
from ...pod.core_header import CoreHeader


class LevelTileLodInfo(CoreDummy):
    magic = 0x8C348AF2D505E5BC

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


EntryTypeManager.register_handler(LevelTileLodInfo)


class LodLevel(IntEnum):
    DefaultRes = 3
    MiddleRes = 2
    LowRes = 1
    NoLod = 0


class LevelTileLod(CoreDummy):
    magic = 0x25591EC41134AEA2

    def __init__(self):
        super().__init__()
        self.lod_level = LodLevel(0)
        self.lod_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.lod_level = LodLevel(reader.read_uint8())
        self.lod_ref.parse(reader, core_file)


EntryTypeManager.register_handler(LevelTileLod)


class LevelLodUnk(CoreDummy):
    magic = 0x81879C362F35924C

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


EntryTypeManager.register_handler(LevelLodUnk)
