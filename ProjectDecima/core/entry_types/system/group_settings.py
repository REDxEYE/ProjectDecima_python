from enum import IntEnum
from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class ESoundGroupType(IntEnum):
    SoundEffect = 0
    Dialogue = 1
    Music = 2
    MusicAmadeus = 3


class SoundGroup(Resource):
    magic = 0x7FC28103CEBC534C

    def __init__(self):
        super().__init__()
        self.type = ESoundGroupType.SoundEffect
        self.destination = EntryReference()
        self.pause_with_game = 0
        self.reverb = 0
        self.priority = 0
        self.instance_limit = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.type = ESoundGroupType(reader.read_uint8())
        self.destination.parse(reader, core_file)
        self.pause_with_game = reader.read_uint8()
        self.reverb = reader.read_uint8()
        self.priority = reader.read_uint32()
        self.instance_limit = reader.read_int32()


EntryTypeManager.register_handler(SoundGroup)
