from uuid import UUID

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..stream_reference import StreamReference
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class IndicesInfo(CoreDummy):
    magic = 0x5FE633B37CEDBF84

    def __init__(self):
        super().__init__()
        self.indices_count = 0
        self.unks_0 = []
        self.unk_guid = UUID(int=0)

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.indices_count = reader.read_uint32()
        self.unks_0 = reader.read_fmt('3I')
        self.unk_guid = reader.read_guid()


EntryTypeManager.register_handler(IndicesInfo)


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
        self.mesh_stream = StreamReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unks_0 = reader.read_fmt('5I')
        self.mesh_stream.parse(reader)


EntryTypeManager.register_handler(MeshStreamInfo)


class MeshInfo(CoreDummy):
    magic = 0xEE49D93DA4C1F4B8

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.vertex_info = EntryReference()
        self.indices_info = EntryReference()
        self.index_count = 0

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.unk_0 = reader.read_uint32()
        self.vertex_info.parse(reader, core_file)
        self.indices_info.parse(reader, core_file)
        reader.skip(24)
        reader.skip(5)
        self.index_count = reader.read_uint32()


EntryTypeManager.register_handler(MeshInfo)


class Vertices(CoreDummy):
    magic = 0x3AC29A123FAABAB4

    def __init__(self):
        super().__init__()
        self.vertex_count = 0
        self.unks_0 = []
        # self.guid_0 = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.vertex_count = reader.read_uint32()
        self.unks_0 = reader.read_fmt(f'={72 // 4}I')
        # self.guid_0.parse(reader, core_file)


EntryTypeManager.register_handler(Vertices)
