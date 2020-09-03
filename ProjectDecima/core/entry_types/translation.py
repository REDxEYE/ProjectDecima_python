from typing import List, Dict
from uuid import UUID

from . import CoreDummy
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


class VoiceRef(CoreDummy):

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.voice_lines_localized_ref = EntryReference()
        self.ref_1 = EntryReference()
        self.text_lines_localized_ref = EntryReference()
        self.speaker_name_localized_ref = EntryReference()  # not sure

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


class VoiceTranslation(CoreDummy):

    def __init__(self):
        super().__init__()
        self.sentence_id = HashedString()
        self.sound_group_settings_ref = EntryReference()
        self.wwise_localized_sound_presets_ref = EntryReference()
        self.voices = []

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
            self.voices.append(stream_ref)
            reader.skip(1)


class Translation(CoreDummy):
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
        self.translations: Dict[str, Translation.Language] = {}

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()

        for lang in language_list:
            self.translations[lang] = self.Language().parse(reader)
