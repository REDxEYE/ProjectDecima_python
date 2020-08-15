from uuid import UUID
from enum import IntEnum

from .entry_types import CoreDummy
from .pod.strings import HashedString
from ..byte_io_ds import ByteIODS


class LoadMethod(IntEnum):
    NotPresent = 0x0
    Embedded = 0x1
    ImmediateCoreFile = 0x2
    CoreFile = 0x3
    WorkOnly = 0x5


class EntryReference:
    def __init__(self, core_file):
        from ..core_file import CoreFile
        self._core_file: CoreFile = core_file
        self.load_method = LoadMethod(0)
        self.guid = UUID(int=0)
        self.file_ref = HashedString(0, '')

    def __repr__(self):
        return f"<Ref {self.guid} {self.load_method.name}>"

    def parse(self, reader: ByteIODS):
        self.load_method = LoadMethod(reader.read_uint8())
        if self.load_method != LoadMethod.NotPresent:
            self.set_guid(reader.read_guid())
        if self.load_method >= LoadMethod.ImmediateCoreFile:
            self.file_ref = reader.read_hashed_string()

    def set_guid(self, guid):
        if isinstance(guid, UUID):
            self.guid = guid
        elif isinstance(guid, bytes):
            self.guid = UUID(bytes=guid)

    def resolve(self) -> CoreDummy:
        if self.load_method == LoadMethod.Embedded:
            return self._core_file.get_by_guid(self.guid)

    @property
    def ref(self):
        return self.resolve()
