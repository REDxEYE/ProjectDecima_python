from pathlib import Path
from typing import List, Dict, Type

from .. import CoreDummy
from ..fact import Fact
from ..resource import ResourceWithName
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


# class Propety(CoreDummy):


class BooleanFact(Fact):
    magic = 0xF3BA66D1703DDED2

    def __init__(self):
        super().__init__()
        self.value = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.value = reader.read_uint8()
        assert self.value in [0, 1]


EntryTypeManager.register_handler(BooleanFact)


class EnumFactEntry(ResourceWithName):
    magic = 0xD91716B58198721B

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'<ControlName: "{self.name}">'


EntryTypeManager.register_handler(EnumFactEntry)


class FloatFact(Fact):
    magic = 0x9F9CD2EFBEC10AD0

    def __init__(self):
        super().__init__()
        self.value = 0.0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.value = reader.read_float()


EntryTypeManager.register_handler(FloatFact)


class EnumFact(Fact):
    magic = 0x12EE0426C2998362

    def __init__(self):
        super().__init__()
        self.value = EntryReference()
        self.definition = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.value.parse(reader, core_file)
        self.definition.parse(reader, core_file)


EntryTypeManager.register_handler(EnumFact)
