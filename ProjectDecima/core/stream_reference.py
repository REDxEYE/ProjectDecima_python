from typing import List
from uuid import UUID

from ..utils.byte_io_ds import ByteIODS
from .pod.strings import UnHashedString


class StreamReference:
    _archive_manager = None
    _all_refs: List['StreamReference'] = []

    @classmethod
    def set_archive_manager(cls, manager):
        cls._archive_manager = manager

    @classmethod
    def register_ref(cls, self):
        cls._all_refs.append(self)

    @classmethod
    def resolve(cls, archive_array):
        from ..archive.archive_manager import ArchiveManager
        archive_array: ArchiveManager
        for ref in cls._all_refs:
            stream_path = ref.stream_path.string
            if not stream_path.endswith('.core.stream'):
                stream_path += '.core.stream'
            ref.stream_reader = ByteIODS(archive_array.queue_file(stream_path, False))

    def __init__(self):
        self.stream_path = UnHashedString()
        self.mempool_tag = UUID(int=0)
        self.unk_0 = 0
        self.offset = 0
        self.size = 0
        self.stream_reader: ByteIODS = ByteIODS()

    def parse(self, reader: ByteIODS):
        self.stream_path = reader.read_unhashed_string()
        self.mempool_tag = reader.read_guid()
        self.unk_0, self.offset, self.size = reader.read_fmt('3I')
        if self._archive_manager is not None:
            stream_path = self.stream_path
            if not stream_path.endswith('.core.stream'):
                stream_path += '.core.stream'
            self.stream_reader = ByteIODS(self._archive_manager.queue_file(stream_path, False))
        # self.register_ref(self)

    def __bool__(self):
        return self.stream_reader.size() != 0

    def __repr__(self):
        return f'<Stream "{self.stream_path}":{self.size}>'
