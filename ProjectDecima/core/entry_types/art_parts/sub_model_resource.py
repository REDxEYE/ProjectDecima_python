from enum import IntEnum

from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ..model.model_part import ModelPartResource
from ....utils.byte_io_ds import ByteIODS


class EArtPartsSubModelKind(IntEnum):
    NONE = 0
    Cover = 1
    CoverAndAnim = 2


class ArtPartsSubModelResource(ModelPartResource):
    magic = 0x2ED3FA0EE459E5AC

    def __init__(self):
        super().__init__()
        self.helper_resource = EntryReference()
        self.skinned_model_pose_deformer_resource = EntryReference()
        self.skeleton = EntryReference()
        self.local_offset_matrix = []
        self.extra_resource = EntryReference()
        self.model_kind = EArtPartsSubModelKind.NONE
        self.is_hide_default = False

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.helper_resource.parse(reader, core_file)
        self.skinned_model_pose_deformer_resource.parse(reader, core_file)
        self.skeleton.parse(reader, core_file)
        self.local_offset_matrix = reader.read_fmt('<16f')
        self.extra_resource.parse(reader, core_file)
        self.model_kind = EArtPartsSubModelKind(reader.read_uint32())
        self.is_hide_default = reader.read_uint8()


EntryTypeManager.register_handler(ArtPartsSubModelResource)