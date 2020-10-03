from typing import List

from .rtti_object import RTTIRefObjectSet
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from . import CoreDummy
from ...utils.byte_io_ds import ByteIODS


class ObjectCollection(RTTIRefObjectSet):
    magic = 0xf3586131b4f18516


EntryTypeManager.register_handler(ObjectCollection)
