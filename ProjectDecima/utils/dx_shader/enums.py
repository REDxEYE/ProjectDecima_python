from enum import IntEnum, auto, IntFlag


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
