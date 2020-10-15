from enum import IntEnum
from typing import List

from .state_object_resource import StateObjectResource
from ..resource import Resource
from ..rtti_object import RTTIObject, RTTIRefObject
from ...core_entry_handler_manager import EntryTypeManager
from ...core_object import CoreObject
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class PBDVtxSkinBinding:
    def __init__(self):
        self.infl_idx = []
        self.weights = []

    def parse(self, reader: ByteIODS):
        self.infl_idx = reader.read_fmt(f'{reader.read_uint32()}H')
        self.weights = reader.read_fmt(f'{reader.read_uint32()}B')
        return self


class PBDGraphSimBody:
    def __init__(self):
        self.body = EntryReference()
        self.vtx_topology_list = []
        self.vtx_skin_binding_list_rt = []

    def parse(self, reader: ByteIODS, core_file):
        self.body.parse(reader, core_file)
        self.vtx_topology_list = [reader.read_fmt(f'<{reader.read_uint32()}H') for _ in reader.range32()]
        self.vtx_skin_binding_list_rt = [PBDVtxSkinBinding().parse(reader) for _ in reader.range32()]


class PBDNodeStateResource(StateObjectResource):
    magic = 0x7858C24C3F2B847B

    def __init__(self):
        super().__init__()
        self.solver_iterations = 0
        self.solver_update_freq = 0.0
        self.friction = 0.0
        self.restitution = 0.0
        self.world_motion_limit_enabled = 0
        self.world_motion_limit = 0.0
        self.world_motion_influence = 0.0
        self.body_list = []
        self.skeleton = EntryReference()
        self.inv_biding_matrices = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        (
            self.solver_iterations, self.solver_update_freq,
            self.friction, self.restitution,
            self.world_motion_limit_enabled,
            self.world_motion_limit, self.world_motion_influence
        ) = reader.read_fmt('<ifffbff')
        for _ in reader.range32():
            body = PBDGraphSimBody()
            body.parse(reader, core_file)
            self.body_list.append(body)
        self.skeleton.parse(reader, core_file)
        self.inv_biding_matrices = [reader.read_fmt('16f') for _ in reader.range32()]


EntryTypeManager.register_handler(PBDNodeStateResource)


class PBDVertexDesc:
    def __init__(self):
        self.pos = []
        self.mass = 0.0
        self.area = 0.0
        self.max_dist = 0.0
        self.backstop = 0.0

    def parse(self, reader: ByteIODS):
        self.pos = reader.read_fmt('3f')
        self.mass, self.area, self.max_dist, self.backstop = reader.read_fmt('4f')
        return self


class EPBDConstraintDescType(IntEnum):
    Distance = 1
    Unk_2 = 2
    Unk_3 = 3
    Unk_4 = 4
    Unk_5 = 5
    DistanceLRA = 6
    Bend = 7


class PBDConstraintDesc:
    def __init__(self):
        self.type = EPBDConstraintDescType.Distance
        self.stiffness = 0.0
        self.vtx_index = 0

    def parse(self, reader: ByteIODS):
        self.type = EPBDConstraintDescType(reader.read_uint32())
        self.stiffness = reader.read_float()
        self.vtx_index = reader.read_fmt('4H')
        return self


class PBDBodyResource(Resource):
    magic = 0x4B97B474C24E991A

    def __init__(self):
        super().__init__()
        self.vertices = []
        self.constraints = []
        self.trianlge_index_list = []
        self.global_motion_damping = 0.0
        self.force_field_influence = 0.0
        self.drag = 0.0
        self.list = 0.0
        self.constraint_size_rt = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.vertices = [PBDVertexDesc().parse(reader) for _ in reader.range32()]
        self.constraints = [PBDConstraintDesc().parse(reader) for _ in reader.range32()]
        self.trianlge_index_list = reader.read_fmt(f'{reader.read_uint32()}H')
        (
            self.global_motion_damping, self.force_field_influence,
            self.drag, self.list, self.constraint_size_rt
        ) = reader.read_fmt('4fi')


EntryTypeManager.register_handler(PBDBodyResource)
