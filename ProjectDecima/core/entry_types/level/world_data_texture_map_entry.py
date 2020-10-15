from enum import IntEnum

from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class ETextureChannel(IntEnum):
    R = 0
    G = 1
    B = 2
    A = 3
    Constant0 = 4
    Constant1 = 5
    RGB = 6
    All = 7


class WorldDataTextureMapEntry(Resource):
    magic = 0xB1FDBD01091420C8

    def __init__(self):
        super().__init__()
        self.type = EntryReference()
        self.channel = ETextureChannel.R

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.type.parse(reader, core_file)
        self.channel = ETextureChannel(reader.read_uint32())


EntryTypeManager.register_handler(WorldDataTextureMapEntry)
