from enum import IntEnum
from typing import List

from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class ETerrainMaterialLODType(IntEnum):
    HighQuality = 0
    Flattened = 1
    LowLOD = 2


class TerrainTileMaterialData:
    def __init__(self):
        self.lookup_data_path = HashedString()
        self.lookup_data_block_size = 0
        self.lookup_value_buffer = EntryReference()
        self.lookup_data_offsets = []
        self.lookup_data_buffer = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.lookup_data_path = reader.read_hashed_string()
        self.lookup_data_block_size = reader.read_uint32()
        self.lookup_value_buffer.parse(reader, core_file)
        self.lookup_data_offsets = reader.read_fmt('4f')
        self.lookup_data_buffer.parse(reader, core_file)



class TerrainTileData(Resource):
    magic = 0x3C31E4C959F31FB4

    def __init__(self):
        super().__init__()
        self.grid_pos = []
        self.minimum_node_size = 0
        self.material_lod_type = ETerrainMaterialLODType.HighQuality
        self.material_lod_count = 0
        self.terrain_material_data = TerrainTileMaterialData()
        self.material_weight_map = EntryReference()
        self.ecotope_count_per_terrain_material = []
        self.ecotope_indices_per_terrain_material = []
        self.hole_bboxes = []
        self.hole_data_buffer = EntryReference()
        self.mapped_height_range = []
        self.tile_data_nodes = []
        self.bbox = []
        self.streaming_hint_data = EntryReference()
        self.original_mask_render_effects: List[EntryReference] = []
        self.baked_mask_render_effects: List[EntryReference] = []
        self.runtime_merged_mask_render_effects: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.grid_pos = reader.read_fmt('2i')
        self.minimum_node_size = reader.read_uint32()
        self.material_lod_type = ETerrainMaterialLODType(reader.read_uint32())
        self.material_lod_count = reader.read_uint32()
        self.terrain_material_data.parse(reader, core_file)
        self.material_weight_map.parse(reader, core_file)
        self.ecotope_count_per_terrain_material = reader.read_fmt('4i')
        self.ecotope_indices_per_terrain_material = reader.read_fmt(f'{reader.read_uint32()}B')
        self.hole_bboxes = [reader.read_fmt('4f') for _ in reader.range32()]
        self.hole_data_buffer.parse(reader, core_file)
        self.mapped_height_range = reader.read_fmt('2f')
        self.tile_data_nodes = [reader.read_fmt('3H') for _ in reader.range32()]
        self.bbox = reader.read_fmt('6f')
        self.streaming_hint_data.parse(reader, core_file)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.original_mask_render_effects.append(ref)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.baked_mask_render_effects.append(ref)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.runtime_merged_mask_render_effects.append(ref)
        pass


EntryTypeManager.register_handler(TerrainTileData)
