from enum import IntEnum, Enum, IntFlag, Flag

from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIInt(RTTIType, int):
    pass


class RTTIBool(RTTIType, int):
    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_int8()) == 1

    def to_file(self, buffer: ByteIODS):
        buffer.write_int8(self)


class RTTIInt8(RTTIInt):
    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_int8())

    def to_file(self, buffer: ByteIODS):
        buffer.write_int8(self)


class RTTIUInt8(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint8())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint8(self)


class RTTIInt16(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_int16())

    def to_file(self, buffer: ByteIODS):
        buffer.write_int16(self)


class RTTIUInt16(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint16())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint16(self)


class RTTIInt32(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_int32())

    def to_file(self, buffer: ByteIODS):
        buffer.write_int32(self)


class RTTIUInt32(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint32())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(self)


class RTTIInt64(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_int64())

    def to_file(self, buffer: ByteIODS):
        buffer.write_int64(self)


class RTTIUInt64(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint64())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint64(self)


class RTTIUInt128(RTTIInt):

    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(int.from_bytes(buffer.read_bytes(16), byteorder='little'))

    def to_file(self, buffer: ByteIODS):
        buffer.write_bytes(self.to_bytes(16, byteorder='little'))


class RTTIEnum(RTTIType, Enum):
    pass


class RTTIEnumUInt8(RTTIInt8, RTTIEnum):
    pass


class RTTIEnumUInt16(RTTIInt16, RTTIEnum):
    pass


class RTTIEnumUInt32(RTTIInt32, RTTIEnum):
    pass


class RTTIFlag(RTTIType, IntFlag):
    pass


class RTTIFlagUInt8(RTTIFlag):
    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint8())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint8(self)


class RTTIFlagUInt16(RTTIFlag):
    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint16())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint16(self)


class RTTIFlagUInt32(RTTIFlag):
    @classmethod
    def from_buffer(cls, buffer: ByteIODS):
        return cls(buffer.read_uint32())

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(self)
