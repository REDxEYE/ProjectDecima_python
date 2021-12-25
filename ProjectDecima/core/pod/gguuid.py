import uuid

from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIGGUUID(RTTIType, uuid.UUID):

    def __init__(self):
        super().__init__(int=0)

    def from_buffer(self, buffer: ByteIODS):
        bytes_le = buffer.read_bytes(16)
        self.__dict__['int'] = int.from_bytes((bytes_le[4 - 1::-1] + bytes_le[6 - 1:4 - 1:-1] +
                                               bytes_le[8 - 1:6 - 1:-1] + bytes_le[8:]), byteorder='big')
        return self

    def to_file(self, buffer: ByteIODS):
        buffer.write_bytes(self.bytes_le)
