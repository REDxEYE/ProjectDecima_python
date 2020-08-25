from typing import List
from uuid import UUID
from enum import IntEnum

from .pod.strings import HashedString
from .stream_reference import StreamReference
from ..utils.byte_io_ds import ByteIODS


class LoadMethod(IntEnum):
    NotPresent = 0x0
    Embedded = 0x1
    ImmediateCoreFile = 0x2
    CoreFile = 0x3
    WorkOnly = 0x5


class EntryReference:
    _global_refs: List['EntryReference'] = []
    dirty = False

    @classmethod
    def register_global_ref(cls, self):
        cls._global_refs.append(self)
        cls.dirty = True

    @classmethod
    def resolve(cls, archive_array):
        from .core_file import CoreFile
        from ..archive.archive_array import ArchiveSet
        core_file: CoreFile
        archive_array: ArchiveSet
        cls.dirty = False

        for ref in cls._global_refs.copy():
            if ref.guid.int == 0:
                cls._global_refs.remove(ref)
                continue
            if ref.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
                print(f'Loading referenced core file: {ref._file_ref.string}')
                core = archive_array.queue_file(ref._file_ref.string, True)
                ref.ref = core.get_by_guid(ref.guid)
                ref._core_file = core
            if ref.ref:
                cls._global_refs.remove(ref)
        pass

    def __init__(self):
        self.load_method = LoadMethod(0)
        self.guid = UUID(int=0)
        self._file_ref = HashedString(0, '')
        self.ref = None
        self._core_file = None

    def __repr__(self):
        if self.ref is None:
            return f"<Ref {self.guid} {self.load_method.name}>"
        else:
            return f"<Ref {self.ref.__class__.__name__} {self.load_method.name}>"

    def parse(self, reader: ByteIODS, core_file):
        self.load_method = LoadMethod(reader.read_uint8())
        if self.load_method != LoadMethod.NotPresent:
            self.guid = reader.read_guid()
        if self.load_method >= LoadMethod.ImmediateCoreFile:
            self._file_ref = reader.read_hashed_string()

        if self.load_method == LoadMethod.Embedded:
            core_file.local_links.append(self)
        elif self.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
            self.register_global_ref(self)
