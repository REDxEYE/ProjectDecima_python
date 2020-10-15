from enum import IntEnum
from typing import List

from ..resource import Resource
from ..rtti_object import RTTIObject, RTTIRefObject
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS

class StateObjectResource(Resource):
    pass