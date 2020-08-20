from typing import List

from .. import CoreDummy
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS
from ...pod.core_header import CoreHeader


class LevelTileCollection(CoreDummy):
    def __init__(self):
        super().__init__()
        self.header = CoreHeader()
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        reader.skip(24 + 1)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader)
            self.refs.append(ref)
        reader.skip(12)
