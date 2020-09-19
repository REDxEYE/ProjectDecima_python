from enum import IntEnum
from typing import List
from uuid import UUID

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..stream_reference import StreamingDataSource
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class EIndexFormat(IntEnum):
    Index16 = 0
    Index32 = 1


class IndexArrayResource(CoreDummy):
    magic = 0x5FE633B37CEDBF84

    def __init__(self):
        super().__init__()
        self.indices_count = 0
        self.flags = 0
        self.format = EIndexFormat.Index16
        self.is_streaming = 0
        self.resource_guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.indices_count = reader.read_uint32()
        if self.indices_count > 0:
            self.flags = reader.read_uint32()
            self.format = EIndexFormat(reader.read_uint32())
            self.is_streaming = reader.read_uint32()
            assert self.is_streaming in [0, 1]
            self.resource_guid = reader.read_guid()


EntryTypeManager.register_handler(IndexArrayResource)


class UnkVertexInfo(CoreDummy):
    magic = 0x8EB29E71F97E460F

    def __init__(self):
        super().__init__()
        self.unks_0 = []
        self.vertex_count = 0
        self.unk_1 = 0
        self.mesh_stream_info = EntryReference()
        self.unks_2 = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unks_0 = reader.read_fmt('7I')
        self.vertex_count = reader.read_uint32()
        self.unk_1 = reader.read_uint32()
        self.mesh_stream_info.parse(reader, core_file)
        self.unks_2 = reader.read_fmt('3I')


EntryTypeManager.register_handler(UnkVertexInfo)


class MeshStreamInfo(CoreDummy):
    magic = 0xA4341E94120AA306

    def __init__(self):
        super().__init__()
        self.unks_0 = []
        self.mesh_stream = StreamingDataSource()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unks_0 = reader.read_fmt('5I')
        self.mesh_stream.parse(reader)


EntryTypeManager.register_handler(MeshStreamInfo)


class PrimitiveResource(CoreDummy):
    magic = 0xEE49D93DA4C1F4B8

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.vertex_array = EntryReference()
        self.index_array = EntryReference()
        self.bbox = ((0.0, 0.0, 0.0,), (0.0, 0.0, 0.0))
        self.index_offset = 0
        self.skd_tree = EntryReference()
        self.index_count = 0
        self.index_end = 0
        self.hash = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        self.vertex_array.parse(reader, core_file)
        self.index_array.parse(reader, core_file)
        self.index_offset = reader.read_uint32()
        self.bbox = (reader.read_fmt('3f'), reader.read_fmt('3f'))
        self.skd_tree.parse(reader, core_file)
        self.index_count = reader.read_uint32()
        self.index_end = reader.read_uint32()
        # self.hash = reader.read_uint32()


EntryTypeManager.register_handler(PrimitiveResource)


class VertexBlockInfo:
    def __init__(self):
        self.flags = 0
        self.stride = 0
        self.element_count = 0
        self.unk_3 = 0
        self.unk_4 = []
        self.unk_data = []

    def parse(self, reader: ByteIODS):
        self.flags, self.stride, self.element_count, self.unk_3 = reader.read_fmt('4I')
        self.unk_4 = reader.read_fmt('3I')
        for _ in range(self.element_count):
            self.unk_data.append(reader.read_bytes(4))


class VertexArrayResource(CoreDummy):
    magic = 0x3AC29A123FAABAB4

    def __init__(self):
        super().__init__()
        self.vertex_count = 0
        self.vertex_stream_count = 0
        self.is_streaming = 0
        self.vertex_infos: List[VertexBlockInfo] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.vertex_count = reader.read_uint32()
        self.vertex_stream_count = reader.read_uint32()
        self.is_streaming = reader.read_uint8()
        for _ in range(self.vertex_stream_count):
            vertex_block_info = VertexBlockInfo()
            vertex_block_info.parse(reader)
            self.vertex_infos.append(vertex_block_info)


EntryTypeManager.register_handler(VertexArrayResource)
