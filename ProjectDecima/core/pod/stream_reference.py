from typing import List
from uuid import UUID

from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.core.pod.gguuid import RTTIGGUUID
from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.core.pod.strings import UnHashedString


class RTTIStreamRef(RTTIType):
    def __init__(self):
        self.stream_path = UnHashedString()
        self.mempool_tag = RTTIGGUUID()
        self.channel = 0
        self.offset = 0
        self.size = 0
        self.stream_reader: ByteIODS = ByteIODS()

    def from_buffer(self, buffer: ByteIODS):
        self.stream_path.from_buffer(buffer)
        self.mempool_tag.from_buffer(buffer)
        self.channel, self.offset, self.size = buffer.read_fmt('3I')
        return self

    def to_file(self, buffer: ByteIODS):
        self.stream_path.to_file(buffer)
        self.mempool_tag.to_file(buffer)
        buffer.write_fmt('3I', self.channel, self.offset, self.size)

    def __bool__(self):
        return self.stream_reader.size() != 0

    def __repr__(self):
        return f'<Stream "{self.stream_path}":{self.size}>'
