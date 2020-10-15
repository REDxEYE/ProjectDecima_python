from enum import IntEnum
from typing import List

from .dummy import CoreDummy
from .rtti_object import RTTIRefObject
from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io import ByteIO
from ...utils.byte_io_ds import ByteIODS
from ...utils.dx_shader.shader import DXShader


class ShaderType(IntEnum):
    Compute = 0
    Geometry = 1
    Vertex = 2
    Pixel = 3


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


class CoreShader(RTTIRefObject):
    magic = 0x16bb69a9e5aa0d9e

    def __init__(self):
        super().__init__()
        self.total_size = 0
        self.unks_0 = []
        self.shaders: List[ShaderEntry] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.total_size = reader.read_uint32()
        self.unks_0 = reader.read_fmt(f'{28 // 4}I')
        shader_count = reader.read_uint32()
        for _ in range(shader_count):
            shader = ShaderEntry().parse(reader)
            self.shaders.append(shader)


EntryTypeManager.register_handler(CoreShader)
