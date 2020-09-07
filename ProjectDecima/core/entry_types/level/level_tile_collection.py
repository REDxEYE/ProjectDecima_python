from typing import List

from .. import CoreDummy
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS
from ...pod.core_header import CoreHeader


class LevelTileCollection(CoreDummy):
    magic = 0x3c0d150db02d8c80

    def __init__(self):
        super().__init__()
        self.header = CoreHeader()
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        reader.skip(24 + 1)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)
        reader.skip(12)


EntryTypeManager.register_handler(LevelTileCollection)
