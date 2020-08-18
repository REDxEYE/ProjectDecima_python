from . import CoreDummy
from ...byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class UnkEntry(CoreDummy):

    def __init__(self):
        super().__init__()
        self.unk_0_count = 0
        self.unk_0_floats = []
        self.unk_1_count = 0
        self.bone_remap = 0

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.unk_0_count = reader.read_uint32()
        self.unk_0_floats = [reader.read_fmt('6f') for _ in range(self.unk_0_count)]
        self.unk_1_count = reader.read_uint32()
        self.bone_remap = reader.read_fmt(f'{self.unk_1_count}H')


class MaterialReference(CoreDummy):

    def __init__(self,):
        super().__init__()
        self.guid_0 = EntryReference()
        self.unk_0 = 0

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.guid_0.parse(reader)
        self.unk_0 = reader.read_uint8()
