from enum import IntEnum
from uuid import UUID

from . import CoreDummy
from ...core.stream_reference import StreamReference
from ...byte_io_ds import ByteIODS


class TexturePixelFormat(IntEnum):
    UNK = 0
    RGBA8 = 0xC
    A8 = 0x1F
    BC1 = 0x42
    BC2 = 0x43
    BC3 = 0x44
    BC4 = 0x45
    BC5 = 0x47
    BC7 = 0x4B


class Texture(CoreDummy):

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.width = 0
        self.height = 0
        self.layer_count = 0
        self.total_mips = 0
        self.pixel_format = TexturePixelFormat(0)
        self.unk_1 = 0
        self.unk_2 = 0
        self.guid_0 = UUID(int=0)
        self.buffer_size = 0
        self.total_size = 0
        self.stream_size = 0
        self.stream_mips = 0
        self.unk_3 = 0
        self.unk_4 = 0
        self.stream = StreamReference()
        self.data_buffer = b''

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.unk_0, self.width, self.height, self.layer_count = reader.read_fmt('4H')
        self.total_mips = reader.read_uint8()
        self.pixel_format = TexturePixelFormat(reader.read_uint8())
        self.unk_1 = reader.read_uint16()
        self.unk_2 = reader.read_uint32()
        self.guid_0 = reader.read_guid()
        (self.buffer_size, self.total_size, self.stream_size,
         self.stream_mips, self.unk_3, self.unk_4) = reader.read_fmt('6I')
        if self.stream_size > 0:
            self.stream.parse(reader)
        self.data_buffer = reader.read_bytes(self.buffer_size)
