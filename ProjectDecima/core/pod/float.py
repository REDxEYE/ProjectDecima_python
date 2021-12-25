from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIFloat(RTTIType, float):
    pass


class RTTIFloat16(RTTIFloat):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_float16())

    def to_file(self, buffer: ByteIODS):
        buffer.write_float16(self)

class RTTIFloat32(RTTIFloat):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_float())

    def to_file(self, buffer: ByteIODS):
        buffer.write_float(self)


class RTTIFloat64(RTTIFloat):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_double())

    def to_file(self, buffer: ByteIODS):
        buffer.write_double(self)
