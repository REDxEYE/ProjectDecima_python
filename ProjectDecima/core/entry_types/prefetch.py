from enum import IntEnum
from typing import List

from ..core_entry_handler_manager import EntryTypeManager
from ..core_object import CoreObject
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class PrefetchList(CoreObject):
    magic = 0xD05789EAE3ACBF02

    def __init__(self):
        super().__init__()
        self.files = []
        self.sizes = []
        self.total_links = 0
        self.links = []
        self.refs = {}

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.files = [reader.read_hashed_string() for _ in reader.range32()]
        self.sizes = [reader.read_uint32() for _ in reader.range32()]
        self.total_links = reader.read_uint32()
        self.links = [reader.read_fmt(f'{reader.read_uint32()}I') for _ in range(len(self.files))]

        for file_id, links in enumerate(self.links):
            self.refs[self.files[file_id]] = [self.files[link] for link in links]


EntryTypeManager.register_handler(PrefetchList)
