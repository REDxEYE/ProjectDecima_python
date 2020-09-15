from pathlib import Path
from typing import List, Dict, Type

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class UnkSongBlock(CoreDummy):
    magic = 0x256E8E4E5646F75A

    def __init__(self):
        super().__init__()
        self.song_list: List[EntryReference] = []
        self.song_info_unk: List[EntryReference] = []
        self.ref_0 = EntryReference()
        self.ref_1 = EntryReference()
        self.ref_2 = EntryReference()
        self.ref_3 = EntryReference()
        self.ref_4 = EntryReference()
        self.ref_5 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.song_list.append(ref)
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.song_info_unk.append(ref)
        self.ref_0.parse(reader, core_file)
        self.ref_1.parse(reader, core_file)
        self.ref_2.parse(reader, core_file)
        self.ref_3.parse(reader, core_file)
        self.ref_4.parse(reader, core_file)
        self.ref_5.parse(reader, core_file)


EntryTypeManager.register_handler(UnkSongBlock)


class SongInfo(CoreDummy):
    magic = 0xDAFEAE13C7269562

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.artist_name_2 = EntryReference()
        self.artist_name = EntryReference()
        self.copyrights = EntryReference()
        self.additional_info = EntryReference()
        self.ref_4 = EntryReference()
        self.ref_5 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint16()
        self.artist_name_2.parse(reader, core_file)
        self.artist_name.parse(reader, core_file)
        self.copyrights.parse(reader, core_file)
        self.additional_info.parse(reader, core_file)
        self.ref_4.parse(reader, core_file)
        self.ref_5.parse(reader, core_file)


EntryTypeManager.register_handler(SongInfo)


class UnkBlock(CoreDummy):
    magic = 0x17FF4558067CC876

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.unk_1 = 0
        self.artist_name = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        self.unk_1 = reader.read_uint16()
        self.artist_name.parse(reader, core_file)


EntryTypeManager.register_handler(UnkBlock)


class UnkBlock2(CoreDummy):
    magic = 0x1749BDEE3A132B09

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.unk_1 = 0
        self.unk_2 = 0
        self.song_info = EntryReference()
        self.song_name = EntryReference()
        self.control_object = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        self.unk_1 = reader.read_uint8()
        self.unk_2 = reader.read_uint32()
        self.song_info.parse(reader, core_file)
        self.song_name.parse(reader, core_file)
        self.control_object.parse(reader, core_file)


EntryTypeManager.register_handler(UnkBlock2)
