from typing import List
from uuid import UUID

from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.pod.core_header import CoreHeader
from ProjectDecima.utils.byte_io_ds import ByteIODS


class RTTIObject:
    exportable = False
    magic = 0x69F066DDC22139DB

    @property
    def class_name(self):
        return self.__class__.__name__

    def __init__(self):
        self.header = CoreHeader()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)

    def export(self, path: str):
        pass

    def dump(self) -> dict:
        return dict()


EntryTypeManager.register_handler(RTTIObject)


class RTTIRefObject(RTTIObject):
    magic = 0xAA11412EDB60ECBC

    def __init__(self):
        super().__init__()
        self.guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.guid = reader.read_guid()


EntryTypeManager.register_handler(RTTIRefObject)


class RTTIRefObjectSet(RTTIRefObject):
    magic = 0xB79B49EADD3AF8FB

    def __init__(self):
        super().__init__()
        self.objects: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        for _ in range(reader.read_uint32()):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.objects.append(ref)


EntryTypeManager.register_handler(RTTIRefObjectSet)


class EntityComponentResource(RTTIRefObject):
    magic = 0x7619CB816B6502F6


EntryTypeManager.register_handler(EntityComponentResource)
