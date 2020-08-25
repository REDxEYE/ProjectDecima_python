from typing import List

from . import CoreDummy
from ..pod.strings import HashedString
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class TSEntry:

    def __init__(self):
        self.unk_0 = 0
        self.unk_1 = 0
        self.unk_2 = 0
        self.unk_3 = 0
        self.unk_4 = 0
        self.ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.unk_0, self.unk_1, self.unk_2, self.unk_3, self.unk_4 = reader.read_fmt('4IB')
        self.ref.parse(reader, core_file)


class SrcEntry:
    def __init__(self):
        self.slot_id = 0
        self.src_name = HashedString()
        self.unk_0 = 0
        self.unks_1 = []
        # self.unk_pad = 0
        self.width = 0
        self.height = 0
        self.unks_2 = []

    def parse(self, reader: ByteIODS):
        self.slot_id = reader.read_uint32()
        self.src_name = reader.read_hashed_string()
        self.unk_0 = reader.read_uint16()
        self.unks_1 = reader.read_fmt('3I')
        if self.unk_0 == 0:
            self.unk_pad = reader.read_uint32()
        else:
            self.width, self.height = reader.read_fmt('2I')
        self.unks_2 = reader.read_fmt('4f')


class TextureSet(CoreDummy):
    def __init__(self):
        super().__init__()
        self.ts_entries: List[TSEntry] = []
        self.unk_0 = 0
        self.src_entries: List[SrcEntry] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        entry_count = reader.read_uint32()
        for _ in range(entry_count):
            entry = TSEntry()
            entry.parse(reader, core_file)
            self.ts_entries.append(entry)
        self.unk_0 = reader.read_uint32()
        src_entry_count = reader.read_uint32()
        for _ in range(src_entry_count):
            entry = SrcEntry()
            entry.parse(reader)
            self.src_entries.append(entry)
