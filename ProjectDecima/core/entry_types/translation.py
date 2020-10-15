import json
import os
from enum import IntEnum
from pathlib import Path
from typing import List, Dict
from uuid import UUID

from .dummy import CoreDummy
from .resource import ResourceWithName, Resource
from .rtti_object import RTTIRefObject
from .sound import WwiseSimpleSoundResource
from ..core_entry_handler_manager import EntryTypeManager
from ..core_object import CoreObject
from ..entry_reference import EntryReference
from ..pod.strings import HashedString
from ..stream_reference import StreamingDataSource
from ...utils.byte_io_ds import ByteIODS

language_list = ["English",
                 "French",
                 "Spanish",
                 "German",
                 "Italian",
                 "Dutch",
                 "Portuguese",
                 "Chinese (Traditional)",
                 "Korean",
                 "Russian",
                 "Polish",
                 "Norwegian",
                 "Finnish",
                 "Swedish",
                 "Danish",
                 "Japanese",
                 "Spanish (Mexico)",
                 "Portuguese (Brazil)",
                 "Turkish",
                 "Arabic",
                 "Chinese (Simplified)",
                 "Unknown",
                 "Greek",
                 "Czech",
                 "Hungarian"]


class EGender(IntEnum):
    Male = 1
    Female = 2


class VoiceResource(ResourceWithName):
    magic = 0xE676A549155DA53B

    def __init__(self):
        super().__init__()
        self.voice_id = 0
        self.gender = EGender.Male
        self.localized_name = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.voice_id = reader.read_uint32()
        self.gender = EGender(reader.read_uint8())
        self.localized_name.parse(reader, core_file)


EntryTypeManager.register_handler(VoiceResource)


class ESentenceDelivery(IntEnum):
    on_actor = 1
    radio = 2


class SentenceResource(Resource):
    magic = 0xAD7F486B5DD745A4
    exportable = True

    def __init__(self):
        super().__init__()
        self.delivery = ESentenceDelivery.on_actor
        self.post_delay = 0.0
        self.show_subs = 0
        self.sound = EntryReference()
        self.animation = EntryReference()
        self.text = EntryReference()
        self.voice = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.delivery = reader.read_uint8()
        self.post_delay = reader.read_float()
        self.show_subs = reader.read_uint8()
        self.sound.parse(reader, core_file)
        self.animation.parse(reader, core_file)
        self.text.parse(reader, core_file)
        self.voice.parse(reader, core_file)

    def export(self, output_path: Path):
        text: LocalizedTextResource = self.text.ref
        voice: LocalizedSimpleSoundResource = self.sound.ref
        speaker: VoiceResource = self.voice.ref
        if not all([text, speaker]):
            return
        speaker_translation: LocalizedTextResource = speaker.localized_name.ref
        if not speaker_translation:
            return

        output_json = {}
        lang_output_path = output_path / speaker.name
        os.makedirs(lang_output_path, exist_ok=True)
        print(f'Exporting translation {speaker.name} to {lang_output_path}')

        for lang in language_list:
            localized_speaker = speaker_translation.translations[lang]
            localized_text = text.translations[lang]
            localized_voice = voice.voices.get(lang, None) if voice else None
            output_json[lang] = {'speaker_name': localized_speaker.dump(),
                                 'text_line': localized_text.dump(),
                                 'voice_line_name': f'{lang}_{Path(localized_voice.stream_path).stem}' if localized_voice else "<empty>"}
            if localized_voice:
                localized_voice.stream_reader.seek(0)
                with (lang_output_path / f'{lang}_{Path(localized_voice.stream_path).stem}').open('wb') as f:
                    f.write(localized_voice.stream_reader.read_bytes(-1))
        with (lang_output_path / f'translation_info_{self.guid}.json').open('w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4)

            pass


EntryTypeManager.register_handler(SentenceResource)


class LocalizedSimpleSoundResource(WwiseSimpleSoundResource):
    magic = 0xC726DF870437D774

    def __init__(self):
        super().__init__()
        self.sound_mix_state = EntryReference()
        self.preset = EntryReference()
        self.lengths: List[float] = []
        self.wem_ids: List[int] = []
        self.voices: Dict[str, StreamingDataSource] = {}

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        reader.skip(10 * 4 + 2)
        self.sound_mix_state.parse(reader, core_file)
        self.preset.parse(reader, core_file)
        array_size = reader.peek_uint32()
        self.lengths = reader.read_fmt(f'{array_size}f')
        reader.skip(4)
        array_size = reader.peek_uint32()
        self.wem_ids = reader.read_fmt(f'{array_size}I')
        reader.skip(8 * 4)
        while reader:
            stream_ref = StreamingDataSource()
            stream_ref.parse(reader)
            lang = stream_ref.stream_path.split('.')[-1].capitalize()
            if lang == 'Chinese':
                lang = 'Chinese (Simplified)'
            if lang == 'Latampor':
                lang = 'Portuguese (Brazil)'
            if lang == 'Latamsp':
                lang = 'Spanish (Mexico)'
            self.voices[lang] = stream_ref
            reader.skip(1)


EntryTypeManager.register_handler(LocalizedSimpleSoundResource)


class LocalizedTextResource(Resource):
    magic = 0x31be502435317445

    class Language:
        def __init__(self):
            self.string = ''
            self.comment = ''
            self.flag = 0

        def parse(self, reader: ByteIODS):
            self.string = reader.read_ascii_string(reader.read_uint16())
            self.comment = reader.read_ascii_string(reader.read_uint16())
            self.flag = reader.read_uint8()
            return self



        def __repr__(self):
            return f'<Localized string: "{self.string}" : {self.comment}>'

    def __init__(self):
        super().__init__()
        self.translations: Dict[str, LocalizedTextResource.Language] = {}

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for lang in language_list:
            self.translations[lang] = self.Language().parse(reader)


EntryTypeManager.register_handler(LocalizedTextResource)


class EWaveDataEncodingQuality(IntEnum):
    UncompressedPCM = 0
    LossyLowest = 1
    LossyLow = 2
    LossyMedium = 3
    LossyHigh = 4
    LossyHighest = 5


class EWaveDataEncodingHint(IntEnum):
    ATRAC9 = 3
    MP3 = 4
    AAC = 6
    AutoSelect = 7


class WaveResource(Resource):
    magic = 0x257040983B11DA11

    def __init__(self):
        super().__init__()
        self.is_streaming = 0
        self.use_vbr = 0
        self.encoding_quality = EWaveDataEncodingQuality.UncompressedPCM
        self.wave_data = []
        self.wave_data_size = 0
        self.sample_rate = 0
        self.channel_count = 0
        self.encoding = EWaveDataEncodingHint.ATRAC9
        self.bits_per_sample = 0
        self.bits_per_second = 0
        self.block_alignment = 0
        self.format_tag = 0
        self.frame_size = 0
        self.sample_count = 0

    def parse(self, reader: ByteIODS, core_file):
        super(RTTIRefObject, self).parse(reader, core_file)
        self.is_streaming, self.use_vbr = reader.read_fmt('BB')
        self.encoding_quality = EWaveDataEncodingQuality(reader.read_uint32())
        self.guid = reader.read_guid()
        self.wave_data = reader.read_bytes(reader.read_uint32())
        self.wave_data_size = reader.read_uint32()
        self.sample_rate = reader.read_uint32()
        self.channel_count = reader.read_uint8()
        self.encoding = EWaveDataEncodingHint(reader.read_uint32())
        self.bits_per_sample = reader.read_uint16()
        self.bits_per_second = reader.read_uint32()
        self.block_alignment = reader.read_uint16()
        self.format_tag = reader.read_uint16()
        self.frame_size = reader.read_uint16()
        self.sample_count = reader.read_uint32()


EntryTypeManager.register_handler(WaveResource)


class ELanguage(IntEnum):
    English = 1
    Unknown = 0
    Dutch = 6
    German = 4
    French = 2
    Spanish = 3
    Italian = 5
    Portuguese = 7
    Japanese = 16
    Chinese_Traditional = 8
    Korean = 9
    Russian = 10
    Polish = 11
    Danish = 12
    Finnish = 13
    Norwegian = 14
    Swedish = 15
    LATAMSP = 17
    LATAMPOR = 18
    Turkish = 19
    Arabic = 20
    Chinese_Simplified = 21
    English_UK = 22
    Greek = 23
    Czech = 24
    Hungarian = 25


class AnimationResourceTranslation:
    def __init__(self):
        self.language = ELanguage.Unknown
        self.animation = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.language = ELanguage(reader.read_uint32())
        self.animation.parse(reader, core_file)


class LocalizedAnimationResource(Resource):
    magic = 0x1D68E0C914AB952E

    def __init__(self):
        super().__init__()
        self.animations: List[AnimationResourceTranslation] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in reader.range32():
            anim = AnimationResourceTranslation()
            anim.parse(reader, core_file)
            self.animations.append(anim)


EntryTypeManager.register_handler(LocalizedAnimationResource)


class ELoopMode(IntEnum):
    Off = 0
    On = 1
    Hold = 2
    PingPong = 3


class SkeletonAnimationResource(Resource):
    magic = 0x39A4A2EC923B67E8

    def __init__(self):
        super().__init__()
        self.skeleton = EntryReference()
        self.edge_anim_animations = []
        self.data = []
        self.sample_rate = 0.0
        self.duration = 0.0
        self.loop_mode = ELoopMode.Off
        self.locomotion_delta_rotation = []
        self.locomotion_delta_translation = []
        self.events = EntryReference()
        self.anim_event = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.skeleton.parse(reader, core_file)
        self.edge_anim_animations = reader.read_bytes(reader.read_uint32())
        self.sample_rate = reader.read_float()
        self.duration = reader.read_float()
        self.loop_mode = ELoopMode(reader.read_uint16())
        self.locomotion_delta_rotation = reader.read_fmt('4f')
        self.locomotion_delta_translation = reader.read_fmt('3f')
        self.events.parse(reader, core_file)
        for _ in reader.range32():
            self.anim_event.append(reader.read_uint32())


EntryTypeManager.register_handler(SkeletonAnimationResource)


class LocalizedSoundPreset(CoreObject):
    magic = 0xA2FE933E7E76C534

    def __init__(self):
        super().__init__()
        self.def_volume = 0.0
        self.def_lfe__volume = 0.0
        self.wet_level = 0.0
        self.max_dst = 0.0
        self.min_dst = 0.0
        self.subtitle_max_dst = 0.0
        self.pressure_level = 0.0
        self.attenuation_linearity = 0.0
        self.attenuation_slope = 0.0
        self.group = EntryReference()
        self.uses_hdr_system = 0
        self.affected_by_time_scale = 0
        self.initial_rms = 0.0
        self.wet_min_range = 0.0
        self.wet_max_range = 0.0
        self.wet_level_bias = 0.0
        self.pan_modification_distance = 0.0
        self.occlusion_factor = 0.0
        self.obstruction_factor = 0.0
        self.doppler_factor = 0.0
        self.max_azimuth_delta = 0.0
        self.proximity_radio = 0
        self.should_also_pan_to_center = 0
        self.sound_mix_state = EntryReference()
        self.desired_encoding = EWaveDataEncodingHint.ATRAC9
        self.encoding_quality = EWaveDataEncodingQuality.LossyHigh
        self.obstruction_radius = 0.0
        self.external_source_cookie = 0
        self.flags = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.def_volume = reader.read_float()
        self.def_lfe__volume = reader.read_float()
        self.wet_level = reader.read_float()
        self.min_dst = reader.read_float()
        self.max_dst = reader.read_float()
        self.subtitle_max_dst = reader.read_float()
        self.pressure_level = reader.read_float()
        self.attenuation_linearity = reader.read_float()
        self.attenuation_slope = reader.read_float()
        self.group.parse(reader, core_file)
        self.uses_hdr_system = reader.read_uint8()
        self.affected_by_time_scale = reader.read_uint8()
        self.initial_rms = reader.read_float()
        self.wet_min_range = reader.read_float()
        self.wet_max_range = reader.read_float()
        self.wet_level_bias = reader.read_float()
        self.pan_modification_distance = reader.read_float()
        self.occlusion_factor = reader.read_float()
        self.obstruction_factor = reader.read_float()
        self.doppler_factor = reader.read_float()
        self.max_azimuth_delta = reader.read_float()
        self.proximity_radio = reader.read_uint8()
        self.should_also_pan_to_center = reader.read_uint8()
        self.sound_mix_state.parse(reader, core_file)
        self.desired_encoding = EWaveDataEncodingHint(reader.read_uint32())
        self.encoding_quality = EWaveDataEncodingQuality(reader.read_uint32())
        self.obstruction_radius = reader.read_float()
        self.external_source_cookie = reader.read_uint32()
        self.flags = reader.read_uint8()


EntryTypeManager.register_handler(LocalizedSoundPreset)


class ESentenceGroupType(IntEnum):
    Normal = 0
    OneOfRandom = 1
    OneOfInOrder = 2


class SentenceGroupResource(Resource):
    def __init__(self):
        super().__init__()
        self.type = ESentenceGroupType.Normal
        self.sentences: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.type = ESentenceGroupType(reader.read_uint32())
        self.sentences = [reader.read_ref(core_file) for _ in reader.range32()]
