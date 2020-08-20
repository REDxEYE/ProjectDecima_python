from enum import IntEnum
from pathlib import Path
from uuid import UUID

from . import CoreDummy
from ...core.stream_reference import StreamReference
from ...utils.byte_io_ds import ByteIODS


class TexturePixelFormat(IntEnum):
    UNK = 0
    RGBA8 = 0xC
    UNK_FORMAT_0 = 0x12
    UNK_FORMAT_1 = 0x13
    UNK_FORMAT_2 = 0x16
    UNK_FORMAT_3 = 0x1C
    A8 = 0x1F
    UNK_FORMAT_4 = 0x31
    BC1 = 0x42
    BC2 = 0x43
    BC3 = 0x44
    BC4 = 0x45
    BC5 = 0x47
    CUBEMAP = 0x49
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
        self.data_buffer = reader.read_bytes(self.total_size)

    def export(self, base_dir: str):
        base_dir = Path(base_dir)
        try:
            from PIL import Image
        except ImportError:
            return
        pixel_type = {
            TexturePixelFormat.RGBA8: ('RGBA', 'raw', 4),
            TexturePixelFormat.A8: ('L', 'raw', 1),
            TexturePixelFormat.BC1: ('RGBA', ('bcn', 1, 0), 0.5),
            TexturePixelFormat.BC2: ('RGBA', ('bcn', 2, 0), 1),
            TexturePixelFormat.BC3: ('RGBA', ('bcn', 3, 0), 1),
            TexturePixelFormat.BC4: ('L', ('bcn', 4, 0), 0.5),
            TexturePixelFormat.BC5: ('RGBA', ('bcn', 5, 0), 1),
            TexturePixelFormat.BC7: ('RGBA', ('bcn', 7, 0), 1),
        }
        if self.stream:
            if self.pixel_format in pixel_type:
                pixel_info = pixel_type[self.pixel_format]
                size = int(pixel_info[2] * self.width * self.height)
                im = Image.frombuffer(pixel_info[0], (self.width, self.height),
                                      self.stream.stream_reader.read_bytes(size),
                                      *pixel_info[1])
                im.save(base_dir / (self.stream.stream_path.string + '.tga'))
