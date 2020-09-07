from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class Settings(CoreDummy):
    magic = 0x7FC28103CEBC534C

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.ref_0 = EntryReference()
        self.unk_1 = 0
        self.unk_2 = 0
        self.unk_3 = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint8()
        self.ref_0.parse(reader, core_file)
        self.unk_1 = reader.read_uint16()
        self.unk_2 = reader.read_uint32()
        self.unk_3 = reader.read_int32()


EntryTypeManager.register_handler(Settings)
