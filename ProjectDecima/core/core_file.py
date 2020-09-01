from pathlib import Path
from typing import List, Union
from uuid import UUID

from .entry_reference import EntryReference
from ..utils.byte_io_ds import ByteIODS

from .entry_types import *

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

    def __init__(self, filepath: Union[str, Path, bytes], real_path: Union[str, Path] = ""):
        if isinstance(filepath, bytes):
            self.reader = ByteIODS(filepath)
            self.filepath = Path(real_path)
        else:
            self.filepath = Path(filepath)
            self.reader = ByteIODS(filepath)
        self.entries: List[CoreDummy] = []
        self.local_links: List[EntryReference] = []

    def get_entries_by_type(self, entry_type):
        res: List[CoreDummy] = []
        for entry in self.entries:
            if isinstance(entry, entry_type):
                res.append(entry)
        return res

    @staticmethod
    def get_handler(magic) -> type(CoreDummy):
        return handlers.get(magic, CoreDummy)

    def parse(self):
        while self.reader:
            core_entry_class = self.get_handler(self.reader.peek_uint64())
            core_entry: CoreDummy = core_entry_class()
            start = self.reader.tell()
            _, size = self.reader.peek_fmt('QI')
            sub_reader = ByteIODS(self.reader.read_bytes(size + 12))
            core_entry.parse(sub_reader, self)
            self.reader.seek(start + core_entry.header.size + 12)
            self.entries.append(core_entry)
        self.resolve_local_links()

    def get_by_guid(self, guid: UUID):
        for entry in self.entries:
            entry: CoreDummy
            if entry.guid.int == guid.int:
                return entry
        return None

    def resolve_local_links(self):
        for local_link in self.local_links.copy():
            local_link.ref = self.get_by_guid(local_link.guid)
            local_link._core_file = self
            if local_link.ref:
                self.local_links.remove(local_link)
