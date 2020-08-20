from typing import List
from uuid import UUID
from enum import IntEnum

from .pod.strings import HashedString
from ..utils.byte_io_ds import ByteIODS


class LoadMethod(IntEnum):
    NotPresent = 0x0
    Embedded = 0x1
    ImmediateCoreFile = 0x2
    CoreFile = 0x3
    WorkOnly = 0x5


class EntryReference:
    _all_refs: List['EntryReference'] = []

    @classmethod
    def register_ref(cls, self):
        cls._all_refs.append(self)

    @classmethod
    def resolve(cls, core_file, archive_array):
        from .core_file import CoreFile
        from ..archive.archive_array import ArchiveSet
        core_file: CoreFile
        archive_array: ArchiveSet

        for ref in cls._all_refs:
            if ref.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
                core = archive_array.queue_file(ref.file_ref.string, True)
                ref.ref = core.get_by_guid(ref.guid)
                pass
            elif ref.load_method == LoadMethod.Embedded:
                ref.ref = core_file.get_by_guid(ref.guid)

    def __init__(self):
        self.load_method = LoadMethod(0)
        self.guid = UUID(int=0)
        self.file_ref = HashedString(0, '')
        self.ref = None

    def __repr__(self):
        return f"<Ref {self.guid} {self.load_method.name}>"

    def parse(self, reader: ByteIODS):
        self.load_method = LoadMethod(reader.read_uint8())
        if self.load_method != LoadMethod.NotPresent:
            self.set_guid(reader.read_guid())
        if self.load_method >= LoadMethod.ImmediateCoreFile:
            self.file_ref = reader.read_hashed_string()
        self.register_ref(self)

    def set_guid(self, guid):
        if isinstance(guid, UUID):
            self.guid = guid
        elif isinstance(guid, bytes):
            self.guid = UUID(bytes=guid)

    # def resolve(self) -> CoreDummy:
    #     if self.load_method == LoadMethod.Embedded:
    #         return self._core_file.get_by_guid(self.guid)
    #
    # @property
    # def ref(self):
    #     return self.resolve()
