from typing import List

from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.entry_types.resource import Resource, ResourceWithNameHash
from ProjectDecima.utils.byte_io_ds import ByteIODS


class ArtPartsExtraResource(ResourceWithNameHash):
    magic = 0xF3AEED3F35ACEE67

    def __init__(self):
        super().__init__()
        self.extra_object = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.extra_object.parse(reader,core_file)

EntryTypeManager.register_handler(ArtPartsExtraResource)
