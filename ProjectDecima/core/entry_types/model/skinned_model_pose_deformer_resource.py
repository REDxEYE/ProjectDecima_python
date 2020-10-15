from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class SkinnedModelPoseDeformerResource(Resource):
    magic = 0x54FB67EF4C52BEAF

    def __init__(self):
        super().__init__()
        self.pose_deformer_resource = EntryReference()
        self.pbd_lod_dist = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.pose_deformer_resource.parse(reader, core_file)
        self.pbd_lod_dist = reader.read_fmt('3f')


EntryTypeManager.register_handler(SkinnedModelPoseDeformerResource)
