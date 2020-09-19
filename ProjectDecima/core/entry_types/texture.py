from enum import IntEnum
from pathlib import Path
from uuid import UUID

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ...core.stream_reference import StreamingDataSource
from ...utils.byte_io_ds import ByteIODS


class ETextureType(IntEnum):
    Tex2D = 0
    Tex3D = 1
    TexCubeMap = 2
    Tex2DArray = 3


class TexturePixelFormat(IntEnum):
    INVALID = 76
    RGBA_5551 = 0
    RGBA_5551_REV = 1
    RGBA_4444 = 2
    RGBA_4444_REV = 3
    RGB_888_32 = 4
    RGB_888_32_REV = 5
    RGB_888 = 6
    RGB_888_REV = 7
    RGB_565 = 8
    RGB_565_REV = 9
    RGB_555 = 10
    RGB_555_REV = 11
    RGBA_8888 = 12
    RGBA_8888_REV = 13
    RGBE_REV = 14
    RGBA_FLOAT_32 = 15
    RGB_FLOAT_32 = 16
    RG_FLOAT_32 = 17
    R_FLOAT_32 = 18
    RGBA_FLOAT_16 = 19
    RGB_FLOAT_16 = 20
    RG_FLOAT_16 = 21
    R_FLOAT_16 = 22
    RGBA_UNORM_32 = 23
    RG_UNORM_32 = 24
    R_UNORM_32 = 25
    RGBA_UNORM_16 = 26
    RG_UNORM_16 = 27
    R_UNORM_16 = 28
    RGBA_UNORM_8 = 29
    RG_UNORM_8 = 30
    R_UNORM_8 = 31
    RGBA_NORM_32 = 32
    RG_NORM_32 = 33
    R_NORM_32 = 34
    RGBA_NORM_16 = 35
    RG_NORM_16 = 36
    R_NORM_16 = 37
    RGBA_NORM_8 = 38
    RG_NORM_8 = 39
    R_NORM_8 = 40
    RGBA_UINT_32 = 41
    RG_UINT_32 = 42
    R_UINT_32 = 43
    RGBA_UINT_16 = 44
    RG_UINT_16 = 45
    R_UINT_16 = 46
    RGBA_UINT_8 = 47
    RG_UINT_8 = 48
    R_UINT_8 = 49
    RGBA_INT_32 = 50
    RG_INT_32 = 51
    R_INT_32 = 52
    RGBA_INT_16 = 53
    RG_INT_16 = 54
    R_INT_16 = 55
    RGBA_INT_8 = 56
    RG_INT_8 = 57
    R_INT_8 = 58
    RGB_FLOAT_11_11_10 = 59
    RGBA_UNORM_10_10_10_2 = 60
    RGB_UNORM_11_11_10 = 61
    DEPTH_FLOAT_32_STENCIL_8 = 62
    DEPTH_FLOAT_32_STENCIL_0 = 63
    DEPTH_24_STENCIL_8 = 64
    DEPTH_16_STENCIL_0 = 65
    BC1 = 66
    BC2 = 67
    BC3 = 68
    BC4U = 69
    BC4S = 70
    BC5U = 71
    BC5S = 72
    BC6U = 73
    BC6S = 74
    BC7 = 75


class Texture(CoreDummy):
    magic = 0xA664164D69FD2B38

    def __init__(self):
        super().__init__()
        self.texture_type = 0
        self.width = 0
        self.height = 0
        self.layer_count = 0
        self.tex_3d_depth = 0
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
        self.stream = StreamingDataSource()
        self.data_buffer = b''

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.texture_type = ETextureType(reader.read_uint8())
        reader.skip(1)
        self.width, self.height = reader.read_fmt('2H')
        if self.texture_type in [ETextureType.Tex2D, ETextureType.TexCubeMap]:
            reader.read_uint16()
        elif self.texture_type == ETextureType.Tex3D:
            self.tex_3d_depth = 1 << reader.read_uint16()
        elif self.texture_type == ETextureType.Tex2DArray:
            self.layer_count = reader.read_uint16()
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
            TexturePixelFormat.RGBA_8888: ('RGBA', 'raw', 4),
            TexturePixelFormat.R_UNORM_8: ('L', 'raw', 1),
            TexturePixelFormat.BC1: ('RGBA', ('bcn', 1, 0), 0.5),
            TexturePixelFormat.BC2: ('RGBA', ('bcn', 2, 0), 1),
            TexturePixelFormat.BC3: ('RGBA', ('bcn', 3, 0), 1),
            TexturePixelFormat.BC4U: ('L', ('bcn', 4, 0), 0.5),
            TexturePixelFormat.BC5U: ('RGBA', ('bcn', 5, 0), 1),
            TexturePixelFormat.BC7: ('RGBA', ('bcn', 7, 0), 1),
        }
        if self.stream:
            if self.pixel_format in pixel_type:
                pixel_info = pixel_type[self.pixel_format]
                size = int(pixel_info[2] * self.width * self.height)
                im = Image.frombuffer(pixel_info[0], (self.width, self.height),
                                      self.stream.stream_reader.read_bytes(size),
                                      *pixel_info[1])
                im.save(base_dir / (self.stream.stream_path + '.tga'))


EntryTypeManager.register_handler(Texture)
