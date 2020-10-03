from enum import IntEnum
from typing import List

from . import CoreDummy
from .resource import Resource
from ..core_entry_handler_manager import EntryTypeManager
from ..pod.strings import HashedString
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class EImageCompressionMethod(IntEnum):
    PerceptualData = 0
    NormalData = 1
    VariableData = 2
    DefaultData = 3


class ETexColorSpace(IntEnum):
    Linear = 0
    sRGB = 1


class ETextureSetType(IntEnum):
    Invalid = 0
    Color = 1
    Alpha = 2
    Normal = 3
    Reflectance = 4
    AO = 5
    Roughness = 6
    Height = 7
    Mask = 8
    Mask_Alpha = 9
    Incandescence = 10
    Translucency_Diffusion = 11
    Translucency_Amount = 12
    Misc_01 = 13
    Count = 14


class ETextureSetStorageType(IntEnum):
    RGB = 0
    R = 1
    G = 2
    B = 3
    A = 4
    Count = 5
    Unk = 6


class ETextureSetQualityType(IntEnum):
    Default = 0
    Compressed_High = 1
    Compressed_Low = 2
    Uncompressed = 3
    Normal_BC6 = 4
    Normal_High = 5
    Normal_Low = 6
    BC4 = 8
    Clean = 7
    NormalRoughnessBC7 = 9
    AlphaToCoverageBC4 = 10
    Count = 11


class ETexAddress(IntEnum):
    Wrap = 0
    Clamp = 1
    Mirror = 2
    ClampToBorder = 3


class TextureSetEntry:

    def __init__(self):
        self.compression_method = EImageCompressionMethod.PerceptualData
        self.create_mipmaps = 0
        self.color_space = ETexColorSpace.Linear
        self.packing_info = 0
        self.texture_type = 0
        self.texture_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.compression_method = EImageCompressionMethod(reader.read_uint32())
        self.create_mipmaps = reader.read_uint8()
        self.color_space = ETexColorSpace(reader.read_uint32())
        self.packing_info = reader.read_uint32()
        self.texture_type = reader.read_uint32()
        self.texture_ref.parse(reader, core_file)


class TextureSetTextureDesc:
    def __init__(self):
        self.texture_type = ETextureSetType.Invalid
        self.path = HashedString()
        self.active = 0
        self.gamma_space = 0
        self.storage_type = ETextureSetStorageType.RGB
        self.quality_type = ETextureSetQualityType.Default
        self.compression_method = EImageCompressionMethod.PerceptualData
        self.width = 0
        self.height = 0
        self.default_color = []

    def parse(self, reader: ByteIODS):
        self.texture_type = ETextureSetType(reader.read_uint32())
        self.path = reader.read_hashed_string()
        self.active, self.gamma_space = reader.read_fmt('2B')
        self.storage_type = ETextureSetStorageType(reader.read_uint32())
        self.quality_type = ETextureSetQualityType(reader.read_uint32())
        self.compression_method = EImageCompressionMethod(reader.read_uint32())
        if self.active:
            self.width, self.height = reader.read_fmt('2I')
        else:
            reader.skip(4)

        self.default_color = reader.read_fmt('4f')


class TextureSet(Resource):
    magic = 0xA321E8C307328D2E

    def __init__(self):
        super().__init__()
        self.entries: List[TextureSetEntry] = []
        self.mipmap_mode = ETexAddress.Wrap
        self.descriptions: List[TextureSetTextureDesc] = []
        self.preset = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        entry_count = reader.read_uint32()
        for _ in range(entry_count):
            entry = TextureSetEntry()
            entry.parse(reader, core_file)
            self.entries.append(entry)
        self.mipmap_mode = ETexAddress(reader.read_uint32())
        src_entry_count = reader.read_uint32()
        for _ in range(src_entry_count):
            entry = TextureSetTextureDesc()
            entry.parse(reader)
            self.descriptions.append(entry)
        self.preset.parse(reader, core_file)


EntryTypeManager.register_handler(TextureSet)
