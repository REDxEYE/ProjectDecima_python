from typing import List

from ..entry_reference import EntryReference
from . import CoreDummy
from ...utils.byte_io_ds import ByteIODS


class CoreRefCollection(CoreDummy):
    def __init__(self):
        super().__init__()
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)
