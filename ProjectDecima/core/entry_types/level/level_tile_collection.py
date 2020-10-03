from typing import List

from .. import CoreDummy
from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class StreamingStrategyResource(Resource):
    magic = 0xE64B4D3F10A16A96

    def __init__(self):
        super().__init__()
        self.blacklisted_types = []
        self.whitelisted_types = []
        self.whitelisted_objects = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            string = reader.read_hashed_string()
            self.blacklisted_types.append(string)
        for _ in range(reader.read_uint32()):
            string = reader.read_hashed_string()
            self.whitelisted_types.append(string)
            self.blacklisted_types.append(string)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.whitelisted_objects.append(ref)


EntryTypeManager.register_handler(StreamingStrategyResource)


class TileBasedStreamingStrategyResource(CoreDummy):
    magic = 0x3c0d150db02d8c80

    def __init__(self):
        super().__init__()
        self.hint_all_tiles = 0
        self.tile_border = 0
        self.grid_size = []
        self.tiles: List[EntryReference] = []
        self.high_lod_diameter = 0
        self.low_lod_diameter = 0
        self.superlow_lod_diameter = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.hint_all_tiles = reader.read_uint8()
        self.tile_border = reader.read_uint32()
        self.grid_size = reader.read_fmt('2i')
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.tiles.append(ref)
        self.high_lod_diameter, self.low_lod_diameter, self.superlow_lod_diameter = reader.read_fmt('3i')


EntryTypeManager.register_handler(TileBasedStreamingStrategyResource)
