from enum import IntEnum
from typing import List

from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from .model_resource import MeshResourceBase
from ..resource import Resource
from ..rtti_object import EntityComponentResource
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.core.stream_reference import StreamingDataSource
from ProjectDecima.utils.byte_io_ds import ByteIODS


class StaticMeshResource(MeshResourceBase):
    magic = 0xB36C3ADC211AB947
    def __init__(self):
        super().__init__()
        self.draw_flags = 0
        self.primitives: List[EntryReference] = []
        self.shading_groups: List[EntryReference] = []
        self.orientation_helpers = EntryReference()
        self.simulation_info = EntryReference()
        self.render_effects_swapper = EntryReference()
        self.disable_sun_cascade1 = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.draw_flags = reader.read_uint32()
        self.primitives = [reader.read_ref(core_file) for _ in reader.range32()]
        self.shading_groups = [reader.read_ref(core_file) for _ in reader.range32()]
        self.orientation_helpers.parse(reader, core_file)
        self.simulation_info.parse(reader, core_file)
        self.render_effects_swapper.parse(reader, core_file)
        self.disable_sun_cascade1 = reader.read_uint8()


EntryTypeManager.register_handler(StaticMeshResource)
