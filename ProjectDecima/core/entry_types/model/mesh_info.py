from enum import IntEnum
from typing import List
from uuid import UUID

from ProjectDecima.core.entry_types import CoreDummy
from ProjectDecima.core.entry_types.resource import Resource
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.core.stream_reference import StreamingDataSource
from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.core.entry_reference import EntryReference


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


class IndexArrayResource(Resource):
    magic = 0x5FE633B37CEDBF84

    def __init__(self):
        super().__init__()
        self.indices_count = 0
        self.flags = 0
        self.format = EIndexFormat.Index16
        self.is_streaming = 0
        self.resource_guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.indices_count = reader.read_uint32()
        if self.indices_count > 0:
            self.flags = reader.read_uint32()
            self.format = EIndexFormat(reader.read_uint32())
            self.is_streaming = reader.read_uint32()
            assert self.is_streaming in [0, 1]
            self.resource_guid = reader.read_guid()

    def dump(self):
        return {
            'class': self.class_name,
            'count': self.indices_count,
            'type': self.format.value,
            'streaming': self.is_streaming,
        }


EntryTypeManager.register_handler(IndexArrayResource)


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


class VertexSkin:

    def __init__(self):
        self.pos = []
        self.weight = []
        self.normal = []
        self.bone = []

    def parse(self, reader: ByteIODS):
        self.pos = reader.read_fmt('3h')
        self.weight = reader.read_fmt('7B')
        self.normal = reader.read_fmt('3B')
        self.bone = reader.read_fmt('8H')


class VertexSkinNBT(VertexSkin):
    def __init__(self):
        super().__init__()
        self.bi_tangent = []
        self.tangent = []

    def parse(self, reader: ByteIODS):
        super().parse(reader)
        self.bi_tangent = reader.read_fmt('3B')
        self.tangent = reader.read_fmt('3B')


class PrimitiveSkinInfo:
    def __init__(self):
        self.type = EPrimitiveSkinInfoType.Basic
        self.skin_vtx_type = ESkinnedVtxType.SKVTXTYPE_1x8
        self.blend_shape_mask = []
        self.vertex_count = 0
        self.vertex_compute_nbt_count = 0
        self.vtx_tri_list_buffer = EntryReference()
        self.vertices_skin: List[VertexSkin] = []
        self.vertices_skin_nbt: List[VertexSkinNBT] = []

    def parse(self, reader: ByteIODS, core_file):
        self.type = EPrimitiveSkinInfoType(reader.read_uint32())
        self.skin_vtx_type = ESkinnedVtxType(reader.read_uint32())
        self.blend_shape_mask = reader.read_fmt('4I')
        self.vertex_count = reader.read_uint32()
        self.vertex_compute_nbt_count = reader.read_uint32()
        self.vtx_tri_list_buffer.parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            skin = VertexSkin()
            skin.parse(reader)
            self.vertices_skin.append(skin)
        for _ in range(reader.read_uint32()):
            skin = VertexSkinNBT()
            skin.parse(reader)
            self.vertices_skin_nbt.append(skin)


class VertexDeltaDeformation:
    def __init__(self):
        self.pos = []
        self.nrm = []
        self.vertex_index = 0

    def parse(self, reader: ByteIODS):
        self.pos = reader.read_fmt('3f')
        self.nrm = reader.read_fmt('3B')
        self.vertex_index = reader.read_uint8()


class BlendTargetDeformation:
    def __init__(self):
        self.name = HashedString()
        self.deformations = []

    def parse(self, reader):
        self.name = reader.read_hashed_string()
        for _ in range(reader.read_uint32()):
            def_array = []
            for _ in range(reader.read_uint32()):
                deform = VertexDeltaDeformation()
                deform.parse(reader)
                def_array.append(deform)
            self.deformations.append(def_array)


class RegularSkinnedMeshResourceSkinInfo(Resource):
    magic = 0x8EB29E71F97E460F

    def __init__(self):
        super().__init__()
        self.parts = []
        self.blend_target_deforms = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            part = PrimitiveSkinInfo()
            part.parse(reader, core_file)
            self.parts.append(part)
        for _ in range(reader.read_uint32()):
            target = BlendTargetDeformation()
            target.parse(reader)
            self.blend_target_deforms.append(target)


EntryTypeManager.register_handler(RegularSkinnedMeshResourceSkinInfo)


class DataBufferResource(Resource):
    magic = 0xA4341E94120AA306

    def __init__(self):
        super().__init__()
        self.buffer_count = 0
        self.is_streaming = 0
        self.flags = 0
        self.format = EDataBufferFormat.Invalid
        self.buffer_stride = 0

        self.mesh_stream = StreamingDataSource()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.buffer_count = reader.read_uint32()
        if self.buffer_count > 0:
            self.is_streaming = reader.read_uint32()
            self.flags = reader.read_uint32()
            self.format = EDataBufferFormat(reader.read_uint32())
            self.buffer_stride = reader.read_uint32()
        self.mesh_stream.parse(reader)


EntryTypeManager.register_handler(DataBufferResource)


class PrimitiveResource(Resource):
    magic = 0xEE49D93DA4C1F4B8

    def __init__(self):
        super().__init__()
        self.flags = 0
        self.vertex_array = EntryReference()
        self.index_array = EntryReference()
        self.bbox = ((0.0, 0.0, 0.0,), (0.0, 0.0, 0.0))
        self.skd_tree = EntryReference()
        self.start_index = 0
        self.index_end = 0
        self.hash = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.flags = reader.read_uint32()
        self.vertex_array.parse(reader, core_file)
        self.index_array.parse(reader, core_file)
        self.bbox = (reader.read_fmt('3f'), reader.read_fmt('3f'))
        self.skd_tree.parse(reader, core_file)
        self.start_index = reader.read_uint32()
        self.index_end = reader.read_uint32()
        self.hash = reader.read_uint32()

    def dump(self):
        return {
            'vertex_array': self.vertex_array.ref.dump(),
            'index_array': self.index_array.ref.dump(),
            'index_start': self.start_index,
            'index_end': self.index_end,
        }


EntryTypeManager.register_handler(PrimitiveResource)


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

    def dump(self):
        return {
            'stride': self.stride,
            'elements': [
                {'offset': elem[0],
                 'element_type': elem[1].value,
                 'slot_count': elem[2],
                 'type': elem[3].value} for elem in self.element_desc],
        }


class VertexArrayResource(Resource):
    magic = 0x3AC29A123FAABAB4

    def __init__(self):
        super().__init__()
        self.vertex_count = 0
        self.vertex_stream_count = 0
        self.is_streaming = 0
        self.vertex_streams: List[VertexStream] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.vertex_count = reader.read_uint32()
        self.vertex_stream_count = reader.read_uint32()
        self.is_streaming = bool(reader.read_uint8())
        for _ in range(self.vertex_stream_count):
            vertex_block_info = VertexStream()
            vertex_block_info.parse(reader)
            self.vertex_streams.append(vertex_block_info)

    def dump(self):
        return {
            'class': self.class_name,
            'count': self.vertex_count,
            'streams': [block.dump() for block in self.vertex_streams],
            'streaming': self.is_streaming,
        }


EntryTypeManager.register_handler(VertexArrayResource)
