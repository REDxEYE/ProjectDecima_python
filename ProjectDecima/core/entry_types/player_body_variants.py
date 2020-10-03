from typing import List

from .resource import Resource
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class DSPlayerBodyVariantInterface(Resource):
    magic = 0x81DDDF3B246E8603


class DSPlayerBodyVariant(DSPlayerBodyVariantInterface):
    magic = 0x452a16dd4427b5db

    def __init__(self):
        super().__init__()
        self.skinned_mesh_resource = EntryReference()
        self.boots_skinned_model_resource = EntryReference()
        self.art_parts_variations: List[EntryReference] = []
        self.shoes_art_parts_variations = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.skinned_mesh_resource.parse(reader, core_file)
        self.boots_skinned_model_resource.parse(reader, core_file)
        count = reader.read_uint32()
        for _ in range(count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.art_parts_variations.append(ref)
        self.shoes_art_parts_variations.parse(reader, core_file)


EntryTypeManager.register_handler(DSPlayerBodyVariant)

