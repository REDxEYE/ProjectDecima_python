from enum import IntEnum
from typing import List

from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class EEcotopeSamplingMode(IntEnum):
    EcotopeMapping = 0
    EcotopeIndex = 1


class EcotopeTile(Resource):
    magic = 0xE76F6A8EC9EC8C11

    def __init__(self):
        super().__init__()
        self.grid_coordinates = []
        self.ecotope_sampling_mode = EEcotopeSamplingMode.EcotopeMapping
        self.ecotopes: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.grid_coordinates = reader.read_fmt('2i')
        self.ecotope_sampling_mode = EEcotopeSamplingMode(reader.read_uint8())
        self.ecotopes = [reader.read_ref(core_file) for _ in reader.range32()]


EntryTypeManager.register_handler(EcotopeTile)
