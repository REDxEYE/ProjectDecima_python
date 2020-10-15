from uuid import UUID

from .sub_model_extra_resource import ArtPartsSubModelExtraResource
from ..resource import Resource
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ....utils.byte_io_ds import ByteIODS


class ArtPartsCoverModelResource(ArtPartsSubModelExtraResource):
    magic = 0x8FB6D1083030A794

    def __init__(self):
        super().__init__()
        self.default_pose_rotations = []
        self.default_pose_translations = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.default_pose_rotations = [reader.read_fmt('4f') for _ in reader.range32()]
        self.default_pose_translations = [reader.read_fmt('3f') for _ in reader.range32()]


EntryTypeManager.register_handler(ArtPartsCoverModelResource)
