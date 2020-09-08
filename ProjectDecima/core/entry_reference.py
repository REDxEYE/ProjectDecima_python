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
    _archive_manager = None

    @classmethod
    def set_archive_manager(cls, manager):
        """Setter for **ArchiveManager** instance
        :param manager: Instance of ArchiveManager
        Should be called before any core file parsing
        """
        cls._archive_manager = manager

    def __init__(self):
        self.load_method = LoadMethod(0)
        self.guid = UUID(int=0)
        self._file_ref = HashedString()
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
        if self._archive_manager:
            if self.load_method in [LoadMethod.ImmediateCoreFile, LoadMethod.CoreFile]:
                print(f'Loading referenced core file: {self._file_ref}')
                core = self._archive_manager.queue_file(self._file_ref, True)
                self.ref = core.get_by_guid(self.guid)
                self._core_file = core
        else:
            raise Exception('No archive manager instance were provided')