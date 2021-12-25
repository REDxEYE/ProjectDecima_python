from typing import Dict, Union, Type

from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.core.type_proxy import RTTITypeProxy
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIHashMap(RTTIType, Dict[int, RTTIType]):
    _expected_type: Type[Union[RTTIType, RTTITypeProxy]] = None

    def from_buffer(self, buffer: ByteIODS):
        assert self._expected_type is not None
        if isinstance(self._expected_type, RTTITypeProxy):
            self._expected_type = self._expected_type.resolve()

        item_count = buffer.read_uint32()
        for _ in range(item_count):
            key = buffer.read_uint32()
            self[key] = self._expected_type().from_buffer(buffer)
        pass

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(len(self))
        for key, value in self.items():
            buffer.write_uint32(key)
            value.to_file(buffer)
