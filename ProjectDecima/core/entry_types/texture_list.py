from typing import List

from .resource import Resource
from .texture import TextureEntry
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class TextureList(Resource):
    magic = 0x2CD10F6FF48962C9

    def __init__(self):
        super().__init__()
        self.textures: List[TextureEntry] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.textures = [TextureEntry().parse(reader) for _ in reader.range32()]
        pass


EntryTypeManager.register_handler(TextureList)
