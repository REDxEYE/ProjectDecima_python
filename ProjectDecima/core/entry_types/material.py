import struct
from typing import List
from uuid import UUID

from . import CoreDummy
from ...core.stream_reference import StreamReference
from ..entry_reference import EntryReference
from ...utils.byte_io import ByteIO
from ...utils.byte_io_ds import ByteIODS


class MatVar:
    def __init__(self):
        self.ref = EntryReference()
        self.data = []

    def parse(self, reader: ByteIODS, core_file):
        self.ref.parse(reader, core_file)
        tmp = reader.peek_fmt('I2H')
        print(tmp)
        type_magic = reader.read_uint64()

        if type_magic in [1131449004589570, 2257898667246082, 10139198015144450, 11265097921987074, 1131998760403458,
                          9013298108301826, 7887398201459202, 6098853560834, 31531296245154306, 34908995965682178,
                          32657196151996930, 37160795779367426, 36034895872524802, 22524096990413314, 15768697549357570,
                          13516897735672322, 14642797642514946, 20272297176728066, 12390997828829698, 24775896804098562,
                          30405396338311682, 29279496431469058, 27027696617783810, 18020497363042818, 25901796710941186,
                          16894597456200194, 3383798574088706, 5635598387773954, 6761498294616578, 4509698480931330,
                          21398197083570690, 19146397269885442, 10141946794213890, 4512447260000770, 5638347166843394,
                          1132548516217346]:
            print('6I\n')
            self.data = reader.read_fmt('6I')
        elif type_magic in [5549097746946, 6648609374722]:
            print("4I4f16I\n")
            reader.skip(12)
            self.data = reader.read_fmt(f'4f{52 // 4}I')
        elif type_magic in [23649996897255938, 6764247073686018]:
            print("QN->4fQHIBBH\n")
            reader.skip(8)
            count = reader.read_uint32()
            # reader.skip(16)
            for _ in range(count):
                self.data.append(reader.read_fmt(f'<4fQHIBBH'))

        else:
            raise NotImplementedError(f"Unknown type:{type_magic} offset: {reader.tell()}")
        return self


class MatEntry:
    def __init__(self):
        self.unks_0 = []
        self.unk_shorts_1 = []
        self.unk_blocks_2 = []
        self.unk_3 = 0
        self.unk_4 = 0
        self.unk_5 = 0
        self.unk_blocks_6 = []
        self.unks_7 = []
        self.unks_8 = []

        self.vars: List[MatVar] = []
        self.shader_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        print(reader._peek(28))
        self.unks_0 = reader.read_fmt(f'{28 // 4}I')
        print(self.unks_0)
        unk_count = reader.read_uint32()
        self.unk_shorts_1 = reader.read_fmt(f'{unk_count}H')
        unk_block_count = reader.read_uint32()
        for _ in range(unk_block_count):
            self.unk_blocks_2.append(reader.read_fmt('<BBIBB'))
        self.unk_3, self.unk_4, self.unk_5 = reader.read_fmt('3I')
        unk_block_count = reader.read_uint32()
        for _ in range(unk_block_count):
            self.unk_blocks_6.append(reader.read_bytes(16))
        ref_count = reader.read_uint32()
        if ref_count > 0:
            self.unks_8 = reader.read_fmt(f'4I')
        else:
            self.unks_8 = reader.read_fmt('I')
        for _ in range(ref_count):
            var = MatVar().parse(reader, core_file)
            self.vars.append(var)
        self.shader_ref.parse(reader, core_file)
        return self


class Material(CoreDummy):

    def __init__(self):
        super().__init__()
        self.unks_0 = []

        self.entries: List[MatEntry] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()

        while reader:
            try:
                entry = MatEntry().parse(reader, core_file)
            except EOFError:
                break
            except struct.error:
                break
            self.entries.append(entry)
