from . import CoreDummy
from ...utils.byte_io import ByteIO
from ...utils.byte_io_ds import ByteIODS
from ...utils.dx_shader.shader import DXShader


class CoreShader(CoreDummy):

    def __init__(self):
        super().__init__()
        self.raw_shader_size = 0
        self.dxbc_header = DXShader()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.raw_shader_size = reader.read_uint32()
        reader.skip(84)
        shader_reader = ByteIO(reader.read_bytes(self.raw_shader_size))
        self.dxbc_header.parse(shader_reader)
        pass
