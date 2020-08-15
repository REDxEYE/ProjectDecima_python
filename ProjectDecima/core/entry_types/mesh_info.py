from typing import List
from uuid import UUID

from . import CoreDummy
from ...byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class IndicesInfo(CoreDummy):

    def __init__(self, core_file):
        super().__init__(core_file)
        self.indices_count = 0
        self.unks_0 = []
        self.guid = UUID(int=0)

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.indices_count = reader.read_uint32()
        self.unks_0 = reader.read_fmt('3I')
        self.guid = reader.read_guid()


class UnkVertexInfo(CoreDummy):

    def __init__(self, core_file):
        super().__init__(core_file)
        self.unks_0 = []
        self.vertex_count = 0
        self.unk_1 = 0
        self.guid = EntryReference(core_file)
        self.unks_2 = []

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.unks_0 = reader.read_fmt('7I')
        self.vertex_count = reader.read_uint32()
        self.unk_1 = reader.read_uint32()
        self.guid.parse(reader)
        self.unks_2 = reader.read_fmt('3I')


class MeshInfo(CoreDummy):

    def __init__(self, core_file):
        super().__init__(core_file)
        self.unk_0 = 0
        self.guid_0 = EntryReference(core_file)
        self.guid_1 = EntryReference(core_file)
        self.index_count = 0

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.unk_0 = reader.read_uint32()
        self.guid_0.parse(reader)
        self.guid_1.parse(reader)
        reader.skip(24)
        reader.skip(5)
        self.index_count = reader.read_uint32()


class VertexInfo(CoreDummy):

    def __init__(self, core_file):
        super().__init__(core_file)
        self.vertex_count = 0
        self.unks_0 = []
        self.guid_0 = EntryReference(core_file)

    def parse(self, reader: ByteIODS):
        self.header.parse(reader)
        self.vertex_count = reader.read_uint32()
        self.unks_0 = reader.read_fmt(f'{72//4}I')
        self.guid_0.parse(reader)