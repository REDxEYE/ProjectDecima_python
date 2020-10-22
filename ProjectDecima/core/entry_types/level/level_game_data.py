from enum import IntEnum
from typing import List

from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class LevelData(CoreObject):
    magic = 0x36274D2289724B1A

    def __init__(self):
        super().__init__()
        self.initial_area = EntryReference()
        self.hd_area = EntryReference()
        self.strategy_resources: List[EntryReference] = []
        self.global_streaming_strategy_bl_types: List[HashedString] = []
        self.global_streaming_strategy_wl_types: List[HashedString] = []
        self.fog_height_map = EntryReference()
        self.fog_height_bounds = []
        self.env_interaction_manager = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader,core_file)
        self.initial_area.parse(reader, core_file)
        self.hd_area.parse(reader, core_file)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.strategy_resources.append(ref)
        for _ in reader.range32():
            self.global_streaming_strategy_bl_types.append(reader.read_hashed_string())
        for _ in reader.range32():
            self.global_streaming_strategy_wl_types.append(reader.read_hashed_string())
        self.fog_height_map.parse(reader, core_file)
        self.fog_height_bounds = reader.read_fmt('6f')
        self.env_interaction_manager.parse(reader, core_file)


EntryTypeManager.register_handler(LevelData)


class LevelDataGame(LevelData):
    magic = 0xDBDC689E46C7F160
    exportable = True

    def __init__(self):
        super().__init__()
        self.level_settings = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.level_settings.parse(reader, core_file)


EntryTypeManager.register_handler(LevelDataGame)
