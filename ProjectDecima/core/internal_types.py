from enum import IntEnum
from typing import List
from uuid import UUID

from ProjectDecima.utils.byte_io import ByteIO
from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.utils.dx_shader.shader import DXShader


class ShaderType(IntEnum):
    Compute = 0
    Geometry = 1
    Vertex = 2
    Pixel = 3


class EIndexFormat(IntEnum):
    Index16 = 0
    Index32 = 1


class EDataBufferFormat(IntEnum):
    Invalid = 0
    R_FLOAT_16 = 1
    R_FLOAT_32 = 2
    RG_FLOAT_32 = 3
    RGB_FLOAT_32 = 4
    RGBA_FLOAT_32 = 5
    R_UINT_8 = 6
    R_UINT_16 = 7
    R_UINT_32 = 8
    RG_UINT_32 = 9
    RGB_UINT_32 = 10
    RGBA_UINT_32 = 11
    R_INT_32 = 12
    RG_INT_32 = 13
    RGB_INT_32 = 14
    RGBA_INT_32 = 15
    R_UNORM_8 = 16
    R_UNORM_16 = 17
    RGBA_UNORM_8 = 18
    RGBA_UINT_8 = 19
    RG_UINT_16 = 20
    RGBA_UINT_16 = 21
    RGBA_INT_8 = 22
    Structured = 23


class HwIndexArray:
    def __init__(self):
        self.indices_count = 0
        self.flags = 0
        self.format = EIndexFormat.Index16
        self.is_streaming = 0
        self.resource_guid = UUID(int=0)

    def parse(self, reader: ByteIODS):
        self.indices_count = reader.read_uint32()
        if self.indices_count > 0:
            self.flags = reader.read_uint32()
            self.format = EIndexFormat(reader.read_uint32())
            self.is_streaming = reader.read_uint32()
            assert self.is_streaming in [0, 1]
            self.resource_guid = reader.read_guid()


class EPrimitiveSkinInfoType(IntEnum):
    Basic = 0
    NBT = 1
    VsBasic = 2
    VsNbt = 3
    CsNrm = 4
    CsNbt = 5
    CsNrmGen = 6
    CsNbtGen = 7


class ESkinnedVtxType(IntEnum):
    SKVTXTYPE_1x8 = 0
    SKVTXTYPE_2x8 = 1
    SKVTXTYPE_3x8 = 2
    SKVTXTYPE_4x8 = 3
    SKVTXTYPE_5x8 = 4
    SKVTXTYPE_6x8 = 5
    SKVTXTYPE_7x8 = 6
    SKVTXTYPE_8x8 = 7
    SKVTXTYPE_1x16 = 8
    SKVTXTYPE_2x16 = 9
    SKVTXTYPE_3x16 = 10
    SKVTXTYPE_4x16 = 11
    SKVTXTYPE_5x16 = 12
    SKVTXTYPE_6x16 = 13
    SKVTXTYPE_7x16 = 14
    SKVTXTYPE_8x16 = 15


class EVertexElementStorageType(IntEnum):
    Undefined = 0
    SignedShortNormalized = 1
    Float = 2
    HalfFloat = 3
    UnsignedByteNormalized = 4
    SignedShort = 5
    X10Y10Z10W2NORMALIZED = 6
    UnsignedByte = 7
    UnsignedShort = 8
    UnsignedShortNormalized = 9
    UNorm8sRGB = 10
    X10Y10Z10W2UNorm = 11

    def get_value_size(self):
        if self.value in [self.Float, self.X10Y10Z10W2UNorm, self.X10Y10Z10W2NORMALIZED]:
            return 4
        elif self.value in [self.SignedShort, self.SignedShortNormalized,
                            self.HalfFloat,
                            self.UnsignedShort, self.UnsignedShortNormalized]:
            return 2
        elif self.value in [self.UnsignedByte, self.UnsignedByteNormalized, self.UNorm8sRGB]:
            return 1
        else:
            return 0


class EVertexElement(IntEnum):
    Pos = 0
    TangentBFlip = 1
    Tangent = 2
    Binormal = 3
    Normal = 4
    Color = 5
    UV0 = 6
    UV1 = 7
    UV2 = 8
    UV3 = 9
    UV4 = 10
    UV5 = 11
    UV6 = 12
    MotionVec = 13
    Vec4Byte0 = 14
    Vec4Byte1 = 15
    BlendWeights = 16
    BlendIndices = 17
    BlendWeights2 = 18
    BlendIndices2 = 19
    BlendWeights3 = 20
    BlendIndices3 = 21
    PivotPoint = 22
    AltPos = 23
    AltTangent = 24
    AltBinormal = 25
    AltNormal = 26
    AltColor = 27
    AltUV0 = 28
    Invalid = 29


class ShaderEntry:

    def __init__(self):
        self.shader_type = ShaderType.Compute
        self.shader_version = 0
        self.shader = DXShader()

    def parse(self, reader: ByteIODS):
        reader.skip(20)
        self.shader_type = ShaderType(reader.read_uint32())
        reader.skip(20)
        self.shader_version = reader.read_fmt('2H')
        size = reader.read_uint32()
        shader_reader = ByteIO(reader.read_bytes(size))
        self.shader.parse(shader_reader)
        return self


class VertexStream:
    def __init__(self):
        self.flags = 0
        self.stride = 0
        self.element_desc = []
        self.guid_0 = UUID(int=0)

    def parse(self, reader: ByteIODS):
        self.flags, self.stride, desc_count = reader.read_fmt('3I')
        for _ in range(desc_count):
            self.element_desc.append((
                reader.read_uint8(),  # offset
                EVertexElementStorageType(reader.read_uint8()),
                reader.read_uint8(),  # used elements count
                EVertexElement(reader.read_uint8())
            ))
        self.guid_0 = reader.read_guid()


class HwVertexArray:
    def __init__(self):
        self.vertex_count = 0
        self.vertex_stream_count = 0
        self.is_streaming = 0
        self.vertex_streams: List[VertexStream] = []

    def parse(self, reader: ByteIODS):
        self.vertex_count = reader.read_uint32()
        self.vertex_stream_count = reader.read_uint32()
        self.is_streaming = bool(reader.read_uint8())
        for _ in range(self.vertex_stream_count):
            vertex_block_info = VertexStream()
            vertex_block_info.parse(reader)
            self.vertex_streams.append(vertex_block_info)
