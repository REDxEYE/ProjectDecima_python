from enum import IntEnum
from pathlib import Path
from typing import List, Dict, Type

from .dummy import CoreDummy
from .resource import ResourceWithName
from ..core_entry_handler_manager import EntryTypeManager
from ..core_object import CoreObject
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class ESoundShape(IntEnum):
    Sphere = 0,
    Box = 1,
    Cone = 2,
    Capsule = 3,


class ESoundInstanceLimitMode(IntEnum):
    Off = 0
    StopOldest = 1
    StopSoftest = 2
    RejectNew = 3


class SoundResource(ResourceWithName):
    magic = 0x686C8BDBEC28F192

    def __init__(self):
        super().__init__()
        self.group = EntryReference()
        self.volume = 0.0
        self.lfe_volume = 0.0
        self.angle = 0.0
        self.freq_factor = 0.0
        self.shape = ESoundShape.Sphere
        self.wet_level = 0
        self.min_dist = 0.0
        self.pressure_level = 0.0
        self.attenuation_linearity = 0.0
        self.attenuation_slope = 0.0
        self.looping = 0
        self.uses_hdr_system = 0
        self.uses_raycast = 0
        self.affected_by_timescale = 0
        self.instance_limit_mode = ESoundInstanceLimitMode.Off
        self.instance_limit = 0
        self.bit_field = 0
        self.initial_rms = 0.0
        self.wet_min_range = 0.0
        self.wet_max_range = 0.0
        self.wet_level_bias = 0.0
        self.pan_mod_distance = 0.0
        self.occlusion_factor = 0.0
        self.obstruction_factor = 0.0
        self.cancel_sound_zone_occlusion_and_obstruction = 0
        self.dopper_factor = 0.0
        self.max_azimut_delta = 0.0
        self.max_dist = 0.0
        self.stop_on_skip = 0
        self.source_position_expansion_factor = 0.0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.group.parse(reader, core_file)
        self.volume = reader.read_float()
        self.lfe_volume = reader.read_float()
        self.angle = reader.read_float()
        self.freq_factor = reader.read_float()
        self.shape = ESoundShape(reader.read_uint8())
        self.wet_level = reader.read_float()
        self.min_dist = reader.read_float()
        self.pressure_level = reader.read_float()
        self.attenuation_linearity = reader.read_float()
        self.attenuation_slope = reader.read_float()
        self.looping = reader.read_uint8()
        self.uses_hdr_system = reader.read_uint8()
        self.uses_raycast = reader.read_uint8()
        self.affected_by_timescale = reader.read_uint8()
        self.instance_limit_mode = ESoundInstanceLimitMode(reader.read_uint8())
        self.instance_limit = reader.read_uint8()
        self.bit_field = reader.read_uint8()
        self.initial_rms = reader.read_float()
        self.wet_min_range = reader.read_float()
        self.wet_max_range = reader.read_float()
        self.wet_level_bias = reader.read_float()
        self.pan_mod_distance = reader.read_float()
        self.occlusion_factor = reader.read_float()
        self.obstruction_factor = reader.read_float()
        self.cancel_sound_zone_occlusion_and_obstruction = reader.read_uint8()
        self.dopper_factor = reader.read_float()
        self.max_azimut_delta = reader.read_float()
        self.max_dist = reader.read_float()
        self.stop_on_skip = reader.read_uint8()
        self.source_position_expansion_factor = reader.read_float()


EntryTypeManager.register_handler(SoundResource)


class WwiseSimpleSoundResource(SoundResource):
    magic = 0x831CF8CE2070CA1F

    def __init__(self):
        super().__init__()
        self.external_source_cookie = 0
        self.flags = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.external_source_cookie = reader.read_uint32()
        self.flags = reader.read_uint8()


class DSMusicPlayerSystemResource(CoreDummy):
    magic = 0x256E8E4E5646F75A

    def __init__(self):
        super().__init__()
        self.all_albums: List[EntryReference] = []
        self.all_musics: List[EntryReference] = []
        self.music_player = EntryReference()
        self.music_player_control = EntryReference()
        self.stop_enum = EntryReference()
        self.pause_enum = EntryReference()
        self.resume_enum = EntryReference()
        self.resume_by_another_track = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.all_albums.append(ref)
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.all_musics.append(ref)
        self.music_player.parse(reader, core_file)
        self.music_player_control.parse(reader, core_file)
        self.stop_enum.parse(reader, core_file)
        self.pause_enum.parse(reader, core_file)
        self.resume_enum.parse(reader, core_file)
        self.resume_by_another_track.parse(reader, core_file)


EntryTypeManager.register_handler(DSMusicPlayerSystemResource)


class DSMusicPlayerAlbumResource(CoreDummy):
    magic = 0xDAFEAE13C7269562

    def __init__(self):
        super().__init__()
        self.menu_display_priority = 0
        self.title_text = EntryReference()
        self.artist_name = EntryReference()
        self.credits = EntryReference()
        self.artist_name_telop = EntryReference()
        self.credits_telop = EntryReference()
        self.artist_resource = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.menu_display_priority = reader.read_uint16()
        self.title_text.parse(reader, core_file)
        self.artist_name.parse(reader, core_file)
        self.credits.parse(reader, core_file)
        self.artist_name_telop.parse(reader, core_file)
        self.credits_telop.parse(reader, core_file)
        self.artist_resource.parse(reader, core_file)


EntryTypeManager.register_handler(DSMusicPlayerAlbumResource)


class DSMusicPlayerArtistResource(CoreDummy):
    magic = 0x17FF4558067CC876

    def __init__(self):
        super().__init__()
        self.artist_id = 0
        self.menu_display_priority = 0
        self.artist_name = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.artist_id = reader.read_uint32()
        self.menu_display_priority = reader.read_uint16()
        self.artist_name.parse(reader, core_file)


EntryTypeManager.register_handler(DSMusicPlayerArtistResource)


class DSMusicPlayerTrackResource(CoreDummy):
    magic = 0x1749BDEE3A132B09

    def __init__(self):
        super().__init__()
        self.id = 0
        self.seconds = 0
        self.menu_display_priority = 0
        self.album = EntryReference()
        self.title = EntryReference()
        self.track_enum = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.id = reader.read_uint32()
        self.seconds = reader.read_uint8()
        self.menu_display_priority = reader.read_uint32()
        self.album.parse(reader, core_file)
        self.title.parse(reader, core_file)
        self.track_enum.parse(reader, core_file)


EntryTypeManager.register_handler(DSMusicPlayerTrackResource)


class SoundGroupList(CoreObject):
    magic = 0x5C2B37CF67300726

    def __init__(self):
        super().__init__()
        self.groups: List[EntryReference] = []
        self.parent_group = EntryReference()
        self.default_player_dialogue_group = EntryReference()
        self.default_npc_dialogue_group = EntryReference()
        self.default_music_group = EntryReference()
        self.metronome_group = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.groups.append(ref)
        self.parent_group.parse(reader, core_file)
        self.default_player_dialogue_group.parse(reader, core_file)
        self.default_npc_dialogue_group.parse(reader, core_file)
        self.default_music_group.parse(reader, core_file)
        self.metronome_group.parse(reader, core_file)


EntryTypeManager.register_handler(SoundGroupList)
