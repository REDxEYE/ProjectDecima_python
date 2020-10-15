from typing import List

from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ..resource import ResourceWithNameHash
from ....utils.byte_io_ds import ByteIODS


class ArtPartsSubModelWithChildrenResource(ResourceWithNameHash):
    magic = 0x5D1FB9F0D8EA70F4

    def __init__(self):
        super().__init__()
        self.children: List[EntryReference] = []
        self.art_parts_sub_model_part_resource = EntryReference()
        self.hidden = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.children.append(ref)
        self.art_parts_sub_model_part_resource.parse(reader, core_file)
        self.hidden = reader.read_uint8()



EntryTypeManager.register_handler(ArtPartsSubModelWithChildrenResource)
