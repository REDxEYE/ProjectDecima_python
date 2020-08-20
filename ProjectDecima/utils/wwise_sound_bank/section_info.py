from typing import List

from ProjectDecima.utils.byte_io import ByteIO


class WWiseSection:

    def __init__(self):
        self.name = ''
        self.size = 0

    def parse(self, reader: ByteIO):
        self.name = reader.read_fourcc()
        self.size = reader.read_uint32()


class GenericBlock(WWiseSection):
    def __init__(self):
        super().__init__()
        self.data = b''

    def parse(self, reader: ByteIO):
        super().parse(reader)
        self.data = reader.read_bytes(self.size)


class BKHD(WWiseSection):
    def __init__(self):
        super().__init__()
        self.version = 0
        self.id = 0

    def parse(self, reader: ByteIO):
        super().parse(reader)
        self.version = reader.read_uint32()
        self.id = reader.read_uint32()
        reader.skip(self.size - 8)


class WemDesc:
    def __init__(self):
        self.id = 0
        self.offset = 0
        self.size = 0

    def parse(self, reader: ByteIO):
        self.id, self.offset, self.size = reader.read_fmt('3I')


class DIDX(WWiseSection):

    def __init__(self):
        super().__init__()
        self.wem_descs: List[WemDesc] = []

    def parse(self, reader: ByteIO):
        super().parse(reader)
        for _ in range(self.size // 12):
            desc = WemDesc()
            desc.parse(reader)
            self.wem_descs.append(desc)


class DATA(WWiseSection):

    def __init__(self):
        super().__init__()
        self.sub_reader = ByteIO()

    def parse(self, reader: ByteIO):
        super().parse(reader)
        self.sub_reader = ByteIO(reader.read_bytes(self.size))
