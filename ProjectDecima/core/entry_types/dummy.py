from pathlib import Path
from uuid import UUID

from .rtti_object import RTTIObject, RTTIRefObject
from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io_ds import ByteIODS
from ...core.pod.core_header import CoreHeader


class CoreDummy(RTTIRefObject):
    magic = 0xFFFF_FFFF_FFFF_FFFF
    exportable = False

    def __init__(self, ):
        super().__init__()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        reader.skip(self.header.size - 16)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.guid}>'


EntryTypeManager.set_default(CoreDummy)


class CoreDummy_60(CoreDummy):
    magic = 0x2F8D786D07E19A72

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(60)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 16)


EntryTypeManager.register_handler(CoreDummy_60, CoreDummy_60.magic)


class CoreDummy_4(CoreDummy):
    magic = 0x3650BFD5E3DDF318

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        reader.skip(4)
        self.guid = reader.read_guid()
        reader.skip(self.header.size - 20)


class PhysicsSimpleShapeResource(CoreDummy):
    magic = 0x71F9F6716E87D88D


class DSRenderEffectSwapperElement(CoreDummy):
    magic = 0xE5A008AAA3BDDACA


class DSRenderEffectSwapper(CoreDummy):
    magic = 0xC574EFD30DB911E4


class PhysicsCollisionInstance(CoreDummy_4):
    magic = 0xE59AB7DFD80B9421


class PhysicsHeightMapOffsetCollisionResource(CoreDummy_4):
    magic = 0x8FAA995D50547F10


class PhysicsWaterPoolFromHeightMap(CoreDummy_4):
    magic = 0xFF5B35CA05453AC


class PhysicsCollisionResource(CoreDummy_4):
    magic = 0x3650BFD5E3DDF318


EntryTypeManager.register_handler(PhysicsSimpleShapeResource)

EntryTypeManager.register_handler(DSRenderEffectSwapperElement)
EntryTypeManager.register_handler(DSRenderEffectSwapper)
EntryTypeManager.register_handler(PhysicsCollisionInstance)
EntryTypeManager.register_handler(PhysicsHeightMapOffsetCollisionResource)
EntryTypeManager.register_handler(PhysicsWaterPoolFromHeightMap)
EntryTypeManager.register_handler(PhysicsCollisionResource)
