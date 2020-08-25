from typing import List
from uuid import UUID

from ..utils.byte_io_ds import ByteIODS
from .pod.strings import UnHashedString


class StreamReference:
    _all_refs: List['StreamReference'] = []

    @classmethod
    def register_ref(cls, self):
        cls._all_refs.append(self)

    @classmethod
    def resolve(cls, archive_array):
        from ..archive.archive_array import ArchiveSet
        archive_array: ArchiveSet
        for ref in cls._all_refs:
            print(f'Loading referenced stream: {ref.stream_path.string}')
            ref.stream_reader = ByteIODS(archive_array.queue_file(ref.stream_path.string, False))

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
        self.register_ref(self)

    def __bool__(self):
        return self.stream_reader.size() != 0

    def __repr__(self):
        return f'<Stream "{self.stream_path}":{self.size}>'
