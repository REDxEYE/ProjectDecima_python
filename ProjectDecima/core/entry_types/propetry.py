from ProjectDecima.core.entry_types.resource import ResourceWithName
from ProjectDecima.utils.byte_io_ds import ByteIODS
from ProjectDecima.core.entry_types.rtti_object import RTTIObject, RTTIRefObject


class Property(ResourceWithName):
    magic = 0x37413FF53E9F25EC

    def __init__(self):
        super().__init__()
        self.flags = 0

    def parse(self, reader: ByteIODS, core_file):
        super(RTTIRefObject, self).parse(reader, core_file)
        self.flags = reader.read_uint32()
        self.guid = reader.read_guid()
        self.name = reader.read_hashed_string()
