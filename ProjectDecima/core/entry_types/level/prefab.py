from enum import IntEnum
from typing import List
from uuid import UUID

from .world_data import ParentWorldNode
from ..resource import Resource
from ..rtti_object import RTTIRefObject
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class EPODVariantType(IntEnum):
    Invalid = 0
    Integer = 1
    Integer8 = 2
    UnsignedInteger = 3
    UnsignedInteger8 = 4
    Float = 5
    Boolean = 6
    Enum = 7
    IntegerRange = 8
    FloatColor = 9
    FloatRange = 10


class PODVariant:
    def __init__(self):
        self.type = EPODVariantType.Invalid
        self.binary_value = b''

    def parse(self, reader: ByteIODS):
        self.type = EPODVariantType(reader.read_uint8())
        self.binary_value = reader.read_bytes(4)[::-1]


class PrefabPODAttributeOverride:
    def __init__(self):
        self.group = HashedString()
        self.name = HashedString()
        self.value = PODVariant()

    def parse(self, reader: ByteIODS):
        self.group = reader.read_hashed_string()
        self.name = reader.read_hashed_string()
        self.value.parse(reader)


class PrefabShaderOverride:
    def __init__(self):
        self.variable_id = HashedString()
        self.element_count = 0
        self.value = []

    def parse(self, reader: ByteIODS):
        self.variable_id = reader.read_hashed_string()
        self.element_count = reader.read_uint32()
        self.value = reader.read_fmt('4f')


class PrefabObjectOverrides:
    def __init__(self):
        self.runtime_object = UUID(int=0)
        self.orientation = []
        self.is_removed = 0
        self.is_transform_overriden = 0
        self.attributes_overrides = []
        self.shader_overrides = []

    def parse(self, reader: ByteIODS):
        self.runtime_object = reader.read_guid()
        self.orientation = reader.read_fmt('16f')
        self.is_removed = reader.read_uint8()
        self.is_transform_overriden = reader.read_uint8()
        for _ in reader.range32():
            override = PrefabPODAttributeOverride()
            override.parse(reader)
            self.attributes_overrides.append(override)
        for _ in reader.range32():
            override = PrefabShaderOverride()
            override.parse(reader)
            self.shader_overrides.append(override)


class PrefabBaseInstance(ParentWorldNode):
    magic = 0xA066CA182AC8087A

    def __init__(self):
        super().__init__()
        self.overrides: List[EntryReference] = []
        self.original_guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.overrides = []
        for _ in reader.range32():
            override = PrefabObjectOverrides()
            override.parse(reader)
            self.overrides.append(override)
        self.original_guid = reader.read_guid()


EntryTypeManager.register_handler(PrefabBaseInstance)


class PrefabInstance(PrefabBaseInstance):
    magic = 0xBE81C6DC6FACEEB8

    def __init__(self):
        super().__init__()
        self.prefab = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        with open("test.bin", 'wb') as f:
            f.write(reader.read_bytes(-1))
            reader.seek(0)
        super().parse(reader, core_file)
        self.prefab.parse(reader, core_file)
        pass


EntryTypeManager.register_handler(PrefabInstance)


class PrefabResource(RTTIRefObject):
    magic = 0x88D76748A619F52E

    def __init__(self):
        super().__init__()
        self.object_collection = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.object_collection.parse(reader, core_file)


EntryTypeManager.register_handler(PrefabResource)
