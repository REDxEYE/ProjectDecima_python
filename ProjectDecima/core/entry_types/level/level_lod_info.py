from enum import IntEnum
from typing import List

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class StreamingTileStateResource(CoreObject):
    magic = 0x8C348AF2D505E5BC

    def __init__(self):
        super().__init__()
        self.lods: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)

        lod_count = reader.read_uint32()
        for _ in range(lod_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.lods.append(ref)


EntryTypeManager.register_handler(StreamingTileStateResource)


class LodLevel(IntEnum):
    SuperLow = 0
    Low = 1
    Medium = 2
    High = 3


class StreamingTileLODResource(CoreObject):
    magic = 0x25591EC41134AEA2

    def __init__(self):
        super().__init__()
        self.lod_level = LodLevel.SuperLow
        self.objects = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.lod_level = LodLevel(reader.read_uint8())
        self.objects.parse(reader, core_file)


EntryTypeManager.register_handler(StreamingTileLODResource)


class StreamingTileResource(CoreObject):
    magic = 0x81879C362F35924C

    def __init__(self):
        super().__init__()
        self.pos = []
        self.states: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.pos = reader.read_fmt('2i')
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.states.append(ref)


EntryTypeManager.register_handler(StreamingTileResource)
