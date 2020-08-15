from pathlib import Path
from typing import List, Union
from uuid import UUID

from .byte_io_ds import ByteIODS

from .core.entry_types import *

known_magics = {
    0x11e1d1a40b933e66: "Armature",
    0xa664164d69fd2b38: "Texture",
    0xa321e8c307328d2e: "TextureSet",
    0x31be502435317445: "Translation",
    0xE2A812418ABC2172: "Model",
    0xBCE84D96052C041E: "BoneData",
    0x16bb69a9e5aa0d9e: "Shader",
}


class CoreFile:

    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)
        self.reader = ByteIODS(filepath)
        self.entries: List[CoreDummy] = []

    @staticmethod
    def get_handler(magic) -> type(CoreDummy):
        return handlers.get(magic, CoreDummy)

    def parse(self):
        while self.reader:
            core_entry_class = self.get_handler(self.reader.peek_uint64())
            core_entry: CoreDummy = core_entry_class(self)
            start = self.reader.tell()
            core_entry.parse(self.reader)
            # print(core_entry_class.__name__)
            self.reader.seek(start + core_entry.header.size + 12)
            self.entries.append(core_entry)

    def get_by_guid(self, guid: UUID):
        for entry in self.entries:
            if entry.header.guid.int == guid.int:
                return entry
        return None
