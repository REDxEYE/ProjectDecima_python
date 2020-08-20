from typing import List

from .. import CoreDummy
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS
from ...pod.core_header import CoreHeader


class LevelTileLodInfo(CoreDummy):
    def __init__(self):
        super().__init__()
        self.lod_refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)

        lod_count = reader.read_uint32()
        for _ in range(lod_count):
            ref = EntryReference()
            ref.parse(reader)
            self.lod_refs.append(ref)


class LevelTileLod(CoreDummy):
    def __init__(self):
        super().__init__()
        self.lod_level = 0
        self.lod_ref = EntryReference()

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.lod_level = reader.read_uint8()
        self.lod_ref.parse(reader)
