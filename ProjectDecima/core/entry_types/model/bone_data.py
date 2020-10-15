from uuid import UUID

from ..dummy import CoreDummy
from ..resource import Resource
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.utils.byte_io_ds import ByteIODS


class SkinnedMeshIndexedJointBindings(Resource):
    magic = 0xBCE84D96052C041E

    def __init__(self):
        super().__init__()
        self.joint_indices = []
        self.inv_bind_matrices = []
        self.data_hash = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        bone_count = reader.read_uint32()
        self.joint_indices = reader.read_fmt(f'{bone_count}H')
        matrix_count = reader.read_uint32()
        self.inv_bind_matrices = [reader.read_fmt('16f') for _ in range(matrix_count)]
        self.data_hash = reader.read_guid()



EntryTypeManager.register_handler(SkinnedMeshIndexedJointBindings)
