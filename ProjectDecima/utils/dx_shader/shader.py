from enum import IntEnum, auto, IntFlag
from typing import List

from ..byte_io import ByteIO

from .enums import *


class DXChunk:

    def __init__(self, cid, size):
        self.id = cid
        self.size = size

    def parse(self, reader: ByteIO):
        reader.skip(self.size)


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

    def parse(self, reader: ByteIO):
        name_offset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(name_offset)
            self.name = reader.read_ascii_string()
        self.buffer_offset = reader.read_uint32()
        self.size = reader.read_uint32()
        self.flags = D3DShaderVariableFlags(reader.read_uint32())
        var_typ_offset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(var_typ_offset)
            self.type = self.TypeInfo().parse(reader)
        def_val_offset = reader.read_uint32()
        if def_val_offset != 0:
            with reader.save_current_pos():
                reader.seek(def_val_offset)
                self.def_val = reader.read_uint32()

        return self


class ConstantBuffer:
    def __init__(self):
        self.name = ''
        self.flags = D3DShaderCBufferFlags(0)
        self.type = D3D11CBufferType(0)
        self.variables: List[ConstantVariable] = []

    def parse(self, reader: ByteIO):
        start = reader.tell()
        name_offset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(name_offset)
            self.name = reader.read_ascii_string()
        varialbe_count = reader.read_uint32()
        variable_offsets = reader.read_uint32()
        variables_size = reader.read_uint32()
        self.flags = D3DShaderCBufferFlags(reader.read_uint32())
        self.type = D3D11CBufferType(reader.read_uint32())
        reader.seek(variable_offsets)
        for _ in range(varialbe_count):
            var = ConstantVariable().parse(reader)
            self.variables.append(var)

        return self


class RDEF(DXChunk):

    def __init__(self, cid, size):
        super().__init__(cid, size)
        self.resounce_binding_count = 0
        self.version = (0, 0)
        self.program_type = 0x0
        self.flags = 0
        self.compiler_name = ''
        self.constant_buffers: List[ConstantBuffer] = []

    def parse(self, reader: ByteIO):
        constant_buffers = reader.read_uint32()
        buffer_offset = reader.read_uint32()
        self.resounce_binding_count = reader.read_uint32()
        resource_offset = reader.read_uint32()
        self.version = reader.read_fmt('2B')
        self.program_type = reader.read_uint16()
        self.flags = reader.read_uint32()
        compiler_name_offset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(compiler_name_offset)
            self.compiler_name = reader.read_ascii_string()

        for _ in range(constant_buffers):
            reader.seek(buffer_offset)
            buffer = ConstantBuffer().parse(reader)
            self.constant_buffers.append(buffer)


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
        self.rw_mask = D3DComponentMask(reader.read_int8())
        reader.skip(2)

    def __repr__(self):
        return f'<Element "{self.name}":{self.component_type.name} {str(self.mask)} type:{self.system_value_type.name} register:{self.register_index} semantic:{self.semantic_index}>'


class ISGN(DXChunk):
    def __init__(self, cid, size):
        super().__init__(cid, size)
        self.elements: List[ISGNElement] = []

    def parse(self, reader: ByteIO):
        count = reader.read_int32()
        reader.skip(4)
        self.elements = [ISGNElement(reader) for _ in range(count)]


_chunks = {
    b'RDEF': RDEF,
    b'ISGN': ISGN
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
            cid, size = reader.read_fmt('4sI')
            chunk_class = _chunks.get(cid, DXChunk)
            chunk_reader = ByteIO(reader.read_bytes(size))
            chunk = chunk_class(cid, size)
            chunk.parse(chunk_reader)
            self.chunks.append(chunk)

    def print_vertex_fmt(self):
        for chunk in self.chunks:
            if chunk.id == b'ISGN':
                chunk: ISGN
                for e in chunk.elements:
                    print(e)
                print("\n\n")
