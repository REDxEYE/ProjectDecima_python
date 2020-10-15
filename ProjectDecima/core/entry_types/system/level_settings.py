from enum import IntEnum
from typing import List

from ..resource import Resource
from ..rtti_object import RTTIObject, RTTIRefObject
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class PlayerCharacterEntry:
    def __init__(self):
        self.id = HashedString()
        self.character = EntryReference()
        self.condition = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.id = reader.read_hashed_string()
        self.character.parse(reader, core_file)
        self.condition.parse(reader, core_file)


class LevelSettings(Resource):
    magic = 0xB8B2B3402EEA751B

    def __init__(self):
        super().__init__()
        self.ds_player_entity_resource = EntryReference()
        self.player_characters: List[EntryReference] = []
        self.ai_manager = EntryReference()
        self.collectable_manager = EntryReference()
        self.fast_travel_system = EntryReference()
        self.loading_hint_system = EntryReference()
        self.session_image = EntryReference()
        self.weather_system = EntryReference()
        self.crowd_manager = EntryReference()
        self.dynamic_spawner_manager = EntryReference()
        self.heading = 0.0
        self.pre_mission_delay = 0.0
        self.post_mission_delay = 0.0
        self.settings = EntryReference()
        self.ambience_manager = EntryReference()
        self.health_screen_effect_resource = EntryReference()
        self.fade_out_screen_effect_resource = EntryReference()
        self.fade_in_screen_effect_resource = EntryReference()
        self.fell_through_worlds_effect_resource = EntryReference()
        self.loading_fade_in_effect_resource = EntryReference()
        self.impact_effect_resource_collection = EntryReference()
        self.aurora_settings = EntryReference()
        self.splitscreen_lod_mult_override = 0.0
        self.fog_height_map = EntryReference()
        self.fog_height_map_bounds = []
        self.spring_settings = EntryReference()
        self.forcefield_manager_settings = EntryReference()
        self.initial_time_of_day = 0.0
        self.duration_of_one_day_in_seconds = 0.0
        self.initial_enable_day_night_cycle = 0
        self.randomize_time_of_day = 0
        self.environment_interaction_manager = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.ds_player_entity_resource.parse(reader, core_file)
        for _ in reader.range32():
            entry = PlayerCharacterEntry()
            entry.parse(reader,core_file)
            self.player_characters.append(entry)
        self.ai_manager.parse(reader, core_file)
        self.collectable_manager.parse(reader, core_file)
        self.fast_travel_system.parse(reader, core_file)
        self.loading_hint_system.parse(reader, core_file)
        self.session_image.parse(reader, core_file)
        self.weather_system.parse(reader, core_file)
        self.crowd_manager.parse(reader, core_file)
        self.dynamic_spawner_manager.parse(reader, core_file)
        self.heading = reader.read_float()
        self.pre_mission_delay = reader.read_float()
        self.post_mission_delay = reader.read_float()
        self.settings.parse(reader, core_file)
        self.ambience_manager.parse(reader, core_file)
        self.health_screen_effect_resource.parse(reader, core_file)
        self.fade_out_screen_effect_resource.parse(reader, core_file)
        self.fade_in_screen_effect_resource.parse(reader, core_file)
        self.fell_through_worlds_effect_resource.parse(reader, core_file)
        self.loading_fade_in_effect_resource.parse(reader, core_file)
        self.impact_effect_resource_collection.parse(reader, core_file)
        self.aurora_settings.parse(reader, core_file)
        self.splitscreen_lod_mult_override = reader.read_float()
        self.fog_height_map.parse(reader, core_file)
        self.fog_height_map_bounds = reader.read_fmt('3f')
        self.spring_settings.parse(reader, core_file)
        self.forcefield_manager_settings.parse(reader, core_file)
        self.initial_time_of_day = reader.read_float()
        self.duration_of_one_day_in_seconds = reader.read_float()
        self.initial_enable_day_night_cycle = reader.read_uint8()
        self.randomize_time_of_day = reader.read_uint8()
        self.environment_interaction_manager.parse(reader, core_file)


EntryTypeManager.register_handler(LevelSettings)
