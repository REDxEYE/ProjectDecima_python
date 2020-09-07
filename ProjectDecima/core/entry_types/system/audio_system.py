from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class AudioUnk(CoreDummy):
    magic = 0xF3BA66D1703DDED2

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.string = HashedString()
        self.unk_1 = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.unk_0 = reader.read_uint32()
        self.guid = reader.read_guid()
        self.string = reader.read_hashed_string()
        self.unk_1 = reader.read_uint16()


EntryTypeManager.register_handler(AudioUnk)


class ControlName(CoreDummy):
    magic = 0xD91716B58198721B

    def __init__(self):
        super().__init__()
        self.string = HashedString()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.string = reader.read_hashed_string()

    def __repr__(self):
        return f'<ControlName: "{self.string}">'


EntryTypeManager.register_handler(ControlName)


class AudioUnk3(CoreDummy):
    magic = 0x9F9CD2EFBEC10AD0

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.string = HashedString()
        self.unk_1 = 0
        self.unk_2 = 0.0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.unk_0 = reader.read_uint32()
        self.guid = reader.read_guid()
        self.string = reader.read_hashed_string()
        self.unk_1 = reader.read_uint8()
        self.unk_2 = reader.read_float()


EntryTypeManager.register_handler(AudioUnk3)


class AudioUnk4(CoreDummy):
    magic = 0x12EE0426C2998362

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.string = HashedString()
        self.unk_1 = 0
        self.ref_0 = EntryReference()
        self.ref_1 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.unk_0 = reader.read_uint32()
        self.guid = reader.read_guid()
        self.string = reader.read_hashed_string()
        self.unk_1 = reader.read_uint8()
        self.ref_0.parse(reader, core_file)
        self.ref_1.parse(reader, core_file)


EntryTypeManager.register_handler(AudioUnk4)
