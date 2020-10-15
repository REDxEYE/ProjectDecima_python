from typing import List
from uuid import UUID

from ..utils.byte_io_ds import ByteIODS
from .pod.strings import UnHashedString


class StreamingDataSource:
    _archive_manager = None

    @classmethod
    def set_archive_manager(cls, manager):
        """Setter for **ArchiveManager** instance
        :param manager: Instance of ArchiveManager
        Should be called before any core file parsing
        """
        cls._archive_manager = manager

    def __init__(self):
        self.stream_path = UnHashedString()
        self.mempool_tag = UUID(int=0)
        self.channel = 0
        self.offset = 0
        self.size = 0
        self.stream_reader: ByteIODS = ByteIODS()

    def parse(self, reader: ByteIODS):
        self.stream_path = reader.read_unhashed_string()
        self.mempool_tag = reader.read_guid()
        self.channel, self.offset, self.size = reader.read_fmt('3I')
        if self._archive_manager is not None:
            stream_path = self.stream_path
            if not stream_path.endswith('.core.stream'):
                stream_path += '.core.stream'
            self.stream_reader = ByteIODS(self._archive_manager.queue_file(stream_path, False))
        else:
            raise Exception('No archive manager instance were provided')


    def __bool__(self):
        return self.stream_reader.size() != 0

    def __repr__(self):
        return f'<Stream "{self.stream_path}":{self.size}>'
