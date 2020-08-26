from enum import IntEnum, auto, IntFlag
from typing import List

from ..byte_io import ByteIO


class DXChunk:

    def __init__(self):
        self.id = 'NONE'
        self.size = 0

    def parse(self, reader: ByteIO):
        self.id = reader.read_ascii_string(4)
        self.size = reader.read_uint32()


class D3DShaderCBufferFlags(IntEnum):
    D3D_CBF_USERPACKED = 0
    D3D10_CBF_USERPACKED = 1
    D3D_CBF_FORCE_DWORD = 2


class D3D11CBufferType(IntEnum):
    D3D11_CT_CBUFFER = 0
    D3D11_CT_TBUFFER = 1
    D3D11_CT_INTERFACE_POINTERS = 2
    D3D11_CT_RESOURCE_BIND_INFO = 3


class D3DShaderVariableClass(IntEnum):
    D3D_SVC_SCALAR = 0
    D3D_SVC_VECTOR = auto()
    D3D_SVC_MATRIX_ROWS = auto()
    D3D_SVC_MATRIX_COLUMNS = auto()
    D3D_SVC_OBJECT = auto()
    D3D_SVC_STRUCT = auto()
    D3D_SVC_INTERFACE_CLASS = auto()
    D3D_SVC_INTERFACE_POINTER = auto()
    D3D10_SVC_SCALAR = auto()
    D3D10_SVC_VECTOR = auto()
    D3D10_SVC_MATRIX_ROWS = auto()
    D3D10_SVC_MATRIX_COLUMNS = auto()
    D3D10_SVC_OBJECT = auto()
    D3D10_SVC_STRUCT = auto()
    D3D11_SVC_INTERFACE_CLASS = auto()
    D3D11_SVC_INTERFACE_POINTER = auto()
    D3D_SVC_FORCE_DWORD = auto()


class D3DShaderVariableType(IntEnum):
    D3D_SVT_VOID = 0
    D3D_SVT_BOOL = auto()
    D3D_SVT_INT = auto()
    D3D_SVT_FLOAT = auto()
    D3D_SVT_STRING = auto()
    D3D_SVT_TEXTURE = auto()
    D3D_SVT_TEXTURE1D = auto()
    D3D_SVT_TEXTURE2D = auto()
    D3D_SVT_TEXTURE3D = auto()
    D3D_SVT_TEXTURECUBE = auto()
    D3D_SVT_SAMPLER = auto()
    D3D_SVT_SAMPLER1D = auto()
    D3D_SVT_SAMPLER2D = auto()
    D3D_SVT_SAMPLER3D = auto()
    D3D_SVT_SAMPLERCUBE = auto()
    D3D_SVT_PIXELSHADER = auto()
    D3D_SVT_VERTEXSHADER = auto()
    D3D_SVT_PIXELFRAGMENT = auto()
    D3D_SVT_VERTEXFRAGMENT = auto()
    D3D_SVT_UINT = auto()
    D3D_SVT_UINT8 = auto()
    D3D_SVT_GEOMETRYSHADER = auto()
    D3D_SVT_RASTERIZER = auto()
    D3D_SVT_DEPTHSTENCIL = auto()
    D3D_SVT_BLEND = auto()
    D3D_SVT_BUFFER = auto()
    D3D_SVT_CBUFFER = auto()
    D3D_SVT_TBUFFER = auto()
    D3D_SVT_TEXTURE1DARRAY = auto()
    D3D_SVT_TEXTURE2DARRAY = auto()
    D3D_SVT_RENDERTARGETVIEW = auto()
    D3D_SVT_DEPTHSTENCILVIEW = auto()
    D3D_SVT_TEXTURE2DMS = auto()
    D3D_SVT_TEXTURE2DMSARRAY = auto()
    D3D_SVT_TEXTURECUBEARRAY = auto()
    D3D_SVT_HULLSHADER = auto()
    D3D_SVT_DOMAINSHADER = auto()
    D3D_SVT_INTERFACE_POINTER = auto()
    D3D_SVT_COMPUTESHADER = auto()
    D3D_SVT_DOUBLE = auto()
    D3D_SVT_RWTEXTURE1D = auto()
    D3D_SVT_RWTEXTURE1DARRAY = auto()
    D3D_SVT_RWTEXTURE2D = auto()
    D3D_SVT_RWTEXTURE2DARRAY = auto()
    D3D_SVT_RWTEXTURE3D = auto()
    D3D_SVT_RWBUFFER = auto()
    D3D_SVT_BYTEADDRESS_BUFFER = auto()
    D3D_SVT_RWBYTEADDRESS_BUFFER = auto()
    D3D_SVT_STRUCTURED_BUFFER = auto()
    D3D_SVT_RWSTRUCTURED_BUFFER = auto()
    D3D_SVT_APPEND_STRUCTURED_BUFFER = auto()
    D3D_SVT_CONSUME_STRUCTURED_BUFFER = auto()
    D3D_SVT_MIN8FLOAT = auto()
    D3D_SVT_MIN10FLOAT = auto()
    D3D_SVT_MIN16FLOAT = auto()
    D3D_SVT_MIN12INT = auto()
    D3D_SVT_MIN16INT = auto()
    D3D_SVT_MIN16UINT = auto()
    D3D10_SVT_VOID = auto()
    D3D10_SVT_BOOL = auto()
    D3D10_SVT_INT = auto()
    D3D10_SVT_FLOAT = auto()
    D3D10_SVT_STRING = auto()
    D3D10_SVT_TEXTURE = auto()
    D3D10_SVT_TEXTURE1D = auto()
    D3D10_SVT_TEXTURE2D = auto()
    D3D10_SVT_TEXTURE3D = auto()
    D3D10_SVT_TEXTURECUBE = auto()
    D3D10_SVT_SAMPLER = auto()
    D3D10_SVT_SAMPLER1D = auto()
    D3D10_SVT_SAMPLER2D = auto()
    D3D10_SVT_SAMPLER3D = auto()
    D3D10_SVT_SAMPLERCUBE = auto()
    D3D10_SVT_PIXELSHADER = auto()
    D3D10_SVT_VERTEXSHADER = auto()
    D3D10_SVT_PIXELFRAGMENT = auto()
    D3D10_SVT_VERTEXFRAGMENT = auto()
    D3D10_SVT_UINT = auto()
    D3D10_SVT_UINT8 = auto()
    D3D10_SVT_GEOMETRYSHADER = auto()
    D3D10_SVT_RASTERIZER = auto()
    D3D10_SVT_DEPTHSTENCIL = auto()
    D3D10_SVT_BLEND = auto()
    D3D10_SVT_BUFFER = auto()
    D3D10_SVT_CBUFFER = auto()
    D3D10_SVT_TBUFFER = auto()
    D3D10_SVT_TEXTURE1DARRAY = auto()
    D3D10_SVT_TEXTURE2DARRAY = auto()
    D3D10_SVT_RENDERTARGETVIEW = auto()
    D3D10_SVT_DEPTHSTENCILVIEW = auto()
    D3D10_SVT_TEXTURE2DMS = auto()
    D3D10_SVT_TEXTURE2DMSARRAY = auto()
    D3D10_SVT_TEXTURECUBEARRAY = auto()
    D3D11_SVT_HULLSHADER = auto()
    D3D11_SVT_DOMAINSHADER = auto()
    D3D11_SVT_INTERFACE_POINTER = auto()
    D3D11_SVT_COMPUTESHADER = auto()
    D3D11_SVT_DOUBLE = auto()
    D3D11_SVT_RWTEXTURE1D = auto()
    D3D11_SVT_RWTEXTURE1DARRAY = auto()
    D3D11_SVT_RWTEXTURE2D = auto()
    D3D11_SVT_RWTEXTURE2DARRAY = auto()
    D3D11_SVT_RWTEXTURE3D = auto()
    D3D11_SVT_RWBUFFER = auto()
    D3D11_SVT_BYTEADDRESS_BUFFER = auto()
    D3D11_SVT_RWBYTEADDRESS_BUFFER = auto()
    D3D11_SVT_STRUCTURED_BUFFER = auto()
    D3D11_SVT_RWSTRUCTURED_BUFFER = auto()
    D3D11_SVT_APPEND_STRUCTURED_BUFFER = auto()
    D3D11_SVT_CONSUME_STRUCTURED_BUFFER = auto()
    D3D_SVT_FORCE_DWORD = auto()


class D3DShaderVariableFlags(IntEnum):
    D3D_SVF_USERPACKED = 0
    D3D_SVF_USED = auto()
    D3D_SVF_INTERFACE_POINTER = auto()
    D3D_SVF_INTERFACE_PARAMETER = auto()
    D3D10_SVF_USERPACKED = auto()
    D3D10_SVF_USED = auto()
    D3D11_SVF_INTERFACE_POINTER = auto()
    D3D11_SVF_INTERFACE_PARAMETER = auto()
    D3D_SVF_FORCE_DWORD = auto()


class ConstantVariable:
    class TypeInfo:
        def __init__(self):
            self.klass = D3DShaderVariableClass(0)
            self.type = D3DShaderVariableType(0)
            self.rows = 0
            self.cols = 0
            self.array_len = 0
            self.struct_size = 0
            self.offset = 0

        def parse(self, reader: ByteIO):
            self.klass = D3DShaderVariableClass(reader.read_uint8())
            self.type = D3DShaderVariableType(reader.read_uint8())
            self.rows, self.cols, self.array_len, self.struct_size, self.offset = reader.read_fmt('5B')
            return self

    def __init__(self):
        self.name = ''
        self.buffer_offset = 0
        self.size = 0
        self.flags = D3DShaderVariableFlags(0)
        self.type = ''
        self.def_val = 0

    def parse(self, start, reader: ByteIO):
        name_offset = start + reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(name_offset)
            self.name = reader.read_ascii_string()
        self.buffer_offset = reader.read_uint32()
        self.size = reader.read_uint32()
        self.flags = D3DShaderVariableFlags(reader.read_uint32())
        var_typ_offset = start + reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(var_typ_offset)
            self.type = self.TypeInfo().parse(reader)
        def_val_offset = reader.read_uint32()
        if def_val_offset != 0:
            with reader.save_current_pos():
                reader.seek(def_val_offset + start)
                self.def_val = reader.read_uint32()

        return self


class ConstantBuffer:
    def __init__(self):
        self.name = ''
        self.flags = D3DShaderCBufferFlags(0)
        self.type = D3D11CBufferType(0)
        self.variables: List[ConstantVariable] = []

    def parse(self, chunk_start, reader: ByteIO):
        start = reader.tell()
        name_offset = chunk_start + reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(name_offset)
            self.name = reader.read_ascii_string()
        varialbe_count = reader.read_uint32()
        variable_offsets = reader.read_uint32()
        variables_size = reader.read_uint32()
        self.flags = D3DShaderCBufferFlags(reader.read_uint32())
        self.type = D3D11CBufferType(reader.read_uint32())
        reader.seek(chunk_start + variable_offsets)
        for _ in range(varialbe_count):
            var = ConstantVariable().parse(chunk_start, reader)
            self.variables.append(var)

        return self


class RDEF(DXChunk):

    def __init__(self):
        super().__init__()
        self.resounce_binding_count = 0
        self.version = (0, 0)
        self.program_type = 0x0
        self.flags = 0
        self.compiler_name = ''
        self.constant_buffers: List[ConstantBuffer] = []

    def parse(self, reader: ByteIO):
        super().parse(reader)
        start = reader.tell()
        constant_buffers = reader.read_uint32()
        buffer_offset = start + reader.read_uint32()
        self.resounce_binding_count = reader.read_uint32()
        resource_offset = start + reader.read_uint32()
        self.version = reader.read_fmt('2B')
        self.program_type = reader.read_uint16()
        self.flags = reader.read_uint32()
        compiler_name_offset = start + reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(compiler_name_offset)
            self.compiler_name = reader.read_ascii_string()

        for _ in range(constant_buffers):
            reader.seek(buffer_offset)
            buffer = ConstantBuffer().parse(start, reader)
            self.constant_buffers.append(buffer)


class D3DRegisterComponentType(IntEnum):
    UNKNOWN = 0
    UINT32 = auto()
    SINT32 = auto()
    FLOAT32 = auto()


class D3DName(IntEnum):
    UNDEFINED = 0
    POSITION = auto()
    CLIP_DISTANCE = auto()
    CULL_DISTANCE = auto()
    RENDER_TARGET_ARRAY_INDEX = auto()
    VIEWPORT_ARRAY_INDEX = auto()
    VERTEX_ID = auto()
    PRIMITIVE_ID = auto()
    INSTANCE_ID = auto()
    IS_FRONT_FACE = auto()
    SAMPLE_INDEX = auto()
    FINAL_QUAD_EDGE_TESSFACTOR = auto()
    FINAL_QUAD_INSIDE_TESSFACTOR = auto()
    FINAL_TRI_EDGE_TESSFACTOR = auto()
    FINAL_TRI_INSIDE_TESSFACTOR = auto()
    FINAL_LINE_DETAIL_TESSFACTOR = auto()
    FINAL_LINE_DENSITY_TESSFACTOR = auto()
    BARYCENTRICS = auto()
    SHADINGRATE = auto()
    CULLPRIMITIVE = auto()
    TARGET = auto()
    DEPTH = auto()
    COVERAGE = auto()
    DEPTH_GREATER_EQUAL = auto()
    DEPTH_LESS_EQUAL = auto()
    STENCIL_REF = auto()
    INNER_COVERAGE = auto()


class D3DComponentMask(IntFlag):
    X = 1
    Y = 2
    Z = 4
    W = 8


class ISGNElement:
    def __init__(self, reader: ByteIO):
        name_offset = reader.read_int32()

        with reader.save_current_pos():
            reader.seek(name_offset)
            self.name = reader.read_ascii_string()

        self.semantic_index = reader.read_int32()
        self.system_value_type = D3DName(reader.read_int32())
        self.component_type = D3DRegisterComponentType(reader.read_int32())
        self.register_index = reader.read_int32()
        self.mask = D3DComponentMask(reader.read_int8())
        self.rw_mask = reader.read_int8()
        reader.skip(2)


class ISGN(DXChunk):
    def __init__(self):
        super().__init__()
        self.elements: List[ISGNElement] = []

    def parse(self, reader: ByteIO):
        super().parse(reader)

        count = reader.read_int32()
        reader.skip(4)
        self.elements = [ISGNElement(reader) for _ in range(count)]


_chunks = {
    'RDEF': RDEF,
    'ISGN': ISGN
}


class DXShader:

    def __init__(self):
        self.checksum = b''
        self.total_size = 0
        self.chunk_count = 0
        self.chunks: List[DXChunk] = []

    def parse(self, reader: ByteIO):
        assert reader.read_ascii_string(4) == 'DXBC', 'Invalid shader magic'
        self.checksum = reader.read_bytes(16)
        assert reader.read_uint32() == 1, 'Invalid always 1'
        self.total_size = reader.read_uint32()
        self.chunk_count = reader.read_uint32()
        chunk_offsets = reader.read_fmt(f'{self.chunk_count}I')
        for chunk_offset in chunk_offsets:
            reader.seek(chunk_offset)
            cid = reader.peek_fourcc()
            chunk_class = _chunks.get(cid, DXChunk)
            chunk = chunk_class()
            chunk.parse(reader)
            self.chunks.append(chunk)
