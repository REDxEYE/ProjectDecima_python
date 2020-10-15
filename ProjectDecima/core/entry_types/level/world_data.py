from enum import IntEnum
from typing import List

from ..resource import Resource
from ..rtti_object import RTTIObject, RTTIRefObject
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class WorldNode(CoreObject):
    magic = 0x86C9FAD4999D5CE3

    def __init__(self):
        super().__init__()
        self.pos = []
        self.rot = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.pos = reader.read_fmt('3d')
        self.rot = reader.read_fmt('9f')
        self.guid = reader.read_guid()


EntryTypeManager.register_handler(WorldNode)


class ParentWorldNode(WorldNode):
    magic = 0x924C5ADB2F8C4523

    def __init__(self):
        super().__init__()
        self.child_transforms_relative = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.child_transforms_relative = reader.read_uint8()


EntryTypeManager.register_handler(ParentWorldNode)


class WorldDataShape(ParentWorldNode):
    magic = 0x790BC2D5C036FDD0

    def __init__(self):
        super().__init__()
        self.nodes: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in reader.range32():
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.nodes.append(ref)


EntryTypeManager.register_handler(WorldDataShape)


class WorldDataShapeNode(ParentWorldNode):
    magic = 0xEBE7227F6FA9F4FB

    def __init__(self):
        super().__init__()
        self.tangent = []
        self.uv = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.tangent = reader.read_fmt('3f')
        self.uv = reader.read_fmt('2f')


EntryTypeManager.register_handler(WorldDataShapeNode)
