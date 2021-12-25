from typing import List, Union, Type
from uuid import UUID
from enum import IntEnum

from ProjectDecima.core.pod.base_type import RTTIType
from ProjectDecima.core.pod.gguuid import RTTIGGUUID
from ProjectDecima.core.pod.int import RTTIEnumUInt8
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.core.type_proxy import RTTITypeProxy
from ProjectDecima.utils.byte_io_ds import ByteIODS


class LoadMethod(RTTIEnumUInt8):
    NotPresent = 0x0
    Embedded = 0x1
    ImmediateCoreFile = 0x2
    CoreFile = 0x3
    WorkOnly = 0x5


class RTTIRef(RTTIType):
    _expected_type: Type[Union[RTTIType, RTTITypeProxy]] = None

    def __init__(self):
        assert self._expected_type is not None
        self.load_method: LoadMethod = LoadMethod(0)
        self.guid = RTTIGGUUID()
        self.file_ref = HashedString()

    def __repr__(self):
        return f"<Ref {self.guid} {self.load_method.name}>"

    def from_buffer(self, buffer: ByteIODS):
        if isinstance(self._expected_type, RTTITypeProxy):
            self._expected_type = self._expected_type.resolve()
        self.load_method = self.load_method.from_buffer(buffer)
        if self.load_method != LoadMethod.NotPresent:
            self.guid.from_buffer(buffer)
        if self.load_method >= LoadMethod.ImmediateCoreFile:
            self.file_ref.from_buffer(buffer)
        return self

    def to_file(self, buffer: ByteIODS):
        self.load_method.to_file(buffer)
        if self.load_method != LoadMethod.NotPresent:
            self.guid.to_file(buffer)
        if self.load_method >= LoadMethod.ImmediateCoreFile:
            self.file_ref.to_file(buffer)
