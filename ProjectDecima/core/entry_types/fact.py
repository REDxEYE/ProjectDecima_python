from typing import List

from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.entry_types.propetry import Property
from ProjectDecima.core.entry_types.resource import Resource
from ProjectDecima.utils.byte_io_ds import ByteIODS


class Fact(Property):
    magic = 0xBEC7C5F43BD64D76

    def __init__(self):
        super().__init__()
        self.persistent = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.persistent = reader.read_uint8()
        assert self.persistent in [0, 1]


EntryTypeManager.register_handler(Fact)


class EnumFactDefinition(Resource):
    magic = 0xD5273899E6B082DC

    def __init__(self):
        super().__init__()
        self.enum_values: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.enum_values.append(ref)


EntryTypeManager.register_handler(EnumFactDefinition, 0xD5273899E6B082DC)
