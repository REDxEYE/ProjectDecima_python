from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIType:
    def from_buffer(self, buffer: ByteIODS):
        raise NotImplementedError('Implement me')

    def to_file(self, buffer: ByteIODS):
        raise NotImplementedError('Implement me')
