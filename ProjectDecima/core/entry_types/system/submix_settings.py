from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class UnkSettings0(CoreDummy):
    magic = 0x826244CBF27285EF

    def __init__(self):
        super().__init__()
        self.name = HashedString()
        self.ref_0 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.name = reader.read_hashed_string()
        self.ref_0.parse(reader, core_file)


EntryTypeManager.register_handler(UnkSettings0)


class UnkSettings1(CoreDummy):
    magic = 0x890BA0407588EE24

    def __init__(self):
        super().__init__()
        self.name = HashedString()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.name = reader.read_hashed_string()


EntryTypeManager.register_handler(UnkSettings1)
