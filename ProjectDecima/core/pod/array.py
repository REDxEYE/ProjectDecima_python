from typing import Optional, List, Union, Type

from ProjectDecima.core.type_proxy import RTTITypeProxy
from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIArray(RTTIType, List[RTTIType]):
    _expected_type: Type[Union[RTTIType, RTTITypeProxy]] = None

    def __init__(self):
        assert self._expected_type is not None
        super().__init__()

    def __repr__(self) -> str:
        return f'Array<{self._expected_type.__name__}>'

    def from_buffer(self, buffer: ByteIODS):
        item_count = buffer.read_uint32()
        if isinstance(self._expected_type, RTTITypeProxy):
            self._expected_type = self._expected_type.resolve()
        self.extend([self._expected_type().from_buffer(buffer) for _ in range(item_count)])
        return self

    def to_file(self, buffer: ByteIODS):
        buffer.write_uint32(len(self))
        [item.to_file(buffer) for item in self]
