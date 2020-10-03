from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ..resource import ResourceWithName
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class SubmixResource(ResourceWithName):
    magic = 0x826244CBF27285EF

    def __init__(self):
        super().__init__()
        self.destination = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.destination.parse(reader, core_file)


EntryTypeManager.register_handler(SubmixResource)


class SoundMasterBusResource(SubmixResource):
    magic = 0x890BA0407588EE24


EntryTypeManager.register_handler(SoundMasterBusResource)
