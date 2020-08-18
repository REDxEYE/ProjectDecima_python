from typing import List
from uuid import UUID

from . import CoreDummy
from ...byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class UnkModelEntry(CoreDummy):

    def __init__(self):
        super().__init__()
        self.unk1 = 0
        self.model_refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        reader.skip(28)
        self.unk1 = reader.read_uint32()
        reader.skip(16)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader)
            reader.skip(60)
            self.model_refs.append(ref)


class UnkModelEntry2(UnkModelEntry):

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        reader.skip(28)
        self.unk1 = reader.read_uint32()
        reader.skip(20)
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader)
            reader.skip(4)
            self.model_refs.append(ref)
