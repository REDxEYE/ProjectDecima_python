from typing import List

from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from . import CoreDummy
from ...utils.byte_io_ds import ByteIODS


class CoreRefCollection(CoreDummy):
    magic = 0xf3586131b4f18516

    def __init__(self):
        super().__init__()
        self.refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.refs.append(ref)


EntryTypeManager.register_handler(CoreRefCollection)
EntryTypeManager.register_handler(CoreRefCollection,0xD5273899E6B082DC)
EntryTypeManager.register_handler(CoreRefCollection,0x5C2B37CF67300726)
