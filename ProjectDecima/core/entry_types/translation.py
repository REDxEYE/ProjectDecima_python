import json
import os
from pathlib import Path
from typing import List, Dict
from uuid import UUID

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ..pod.strings import HashedString
from ..stream_reference import StreamReference
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


class SpeakerInfo(CoreDummy):
    magic = 0xE676A549155DA53B

    def __init__(self):
        super().__init__()
        self.name = HashedString()
        self.localized_name = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.name = reader.read_hashed_string()
        reader.skip(5)
        self.localized_name.parse(reader, core_file)


EntryTypeManager.register_handler(SpeakerInfo)


class VoiceRef(CoreDummy):
    magic = 0xAD7F486B5DD745A4
    exportable = True

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.voice_lines_localized_ref = EntryReference()
        self.ref_1 = EntryReference()
        self.text_lines_localized_ref = EntryReference()
        self.speaker_name_localized_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        reader.skip(2)
        self.voice_lines_localized_ref.parse(reader, core_file)
        self.ref_1.parse(reader, core_file)
        self.text_lines_localized_ref.parse(reader, core_file)
        # reader.skip(18)
        self.speaker_name_localized_ref.parse(reader, core_file)

    def dump(self, output_path: Path):
        text: Translation = self.text_lines_localized_ref.ref
        voice: VoiceTranslation = self.voice_lines_localized_ref.ref
        speaker: SpeakerInfo = self.speaker_name_localized_ref.ref
        if not all([text, speaker]):
            return
        speaker_translation: Translation = speaker.localized_name.ref
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


EntryTypeManager.register_handler(VoiceRef)


class VoiceTranslation(CoreDummy):
    magic = 0xC726DF870437D774

    def __init__(self):
        super().__init__()
        self.sentence_id = HashedString()
        self.sound_group_settings_ref = EntryReference()
        self.wwise_localized_sound_presets_ref = EntryReference()
        self.voices: Dict[str, StreamReference] = {}

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.sentence_id = reader.read_hashed_string()
        self.sound_group_settings_ref.parse(reader, core_file)
        reader.skip(138)
        self.wwise_localized_sound_presets_ref.parse(reader, core_file)
        unk_count = reader.read_uint32()
        reader.skip(240)
        while reader:
            stream_ref = StreamReference()
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


EntryTypeManager.register_handler(VoiceTranslation)


class Translation(CoreDummy):
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

        def dump(self):
            return {'string': self.string, 'comment': self.comment, 'flag': self.flag}

        def __repr__(self):
            return f'<Localized string: "{self.string}" : {self.comment}>'

    def __init__(self):
        super().__init__()
        self.translations: Dict[str, Translation.Language] = {}

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()

        for lang in language_list:
            self.translations[lang] = self.Language().parse(reader)


EntryTypeManager.register_handler(Translation)


class UnkData(CoreDummy):
    magic = 0x257040983B11DA11

    def __init__(self):
        super().__init__()
        self.unk_0 = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.unk_0 = reader.read_fmt('BBI')
        self.guid = reader.read_guid()


EntryTypeManager.register_handler(UnkData)


class UnkData0(CoreDummy):
    magic = 0x1D68E0C914AB952E

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.unk_1_count = 0
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        self.unk_1_count = reader.read_uint32()
        for _ in range(self.unk_1_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)


EntryTypeManager.register_handler(UnkData0)


class UnkData1(CoreDummy):
    magic = 0x39A4A2EC923B67E8

    def __init__(self):
        super().__init__()
        self.skeleton_ref = EntryReference()
        self.data_size = 0
        self.data = []
        self.unk_0 = []
        self.unk_1 = 0
        self.unk_2 = []
        self.unk_3 = 0.0
        self.unk_4 = []
        self.unk_5 = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.skeleton_ref.parse(reader, core_file)
        self.data_size = reader.read_uint32()
        self.unk_0 = reader.read_fmt('2f')
        self.unk_1 = reader.read_uint32()
        self.unk_2 = reader.read_fmt('3I')
        self.unk_3 = reader.read_float()
        self.unk_4 = reader.read_fmt('4I')
        self.unk_4 = reader.read_uint8()


EntryTypeManager.register_handler(UnkData1)
