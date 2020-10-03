from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.core_object import CoreObject
from ProjectDecima.core.pod.strings import HashedString
from ProjectDecima.utils.byte_io_ds import ByteIODS


class Resource(CoreObject):
    magic = 0x427090533D93D98A
    pass


EntryTypeManager.register_handler(Resource)


class ResourceWithName(Resource):
    magic = 0xBC5672CA3A1C549

    def __init__(self):
        super().__init__()
        self.name = HashedString()

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.name = reader.read_hashed_string()


EntryTypeManager.register_handler(ResourceWithName)


class ResourceWithNameHash(Resource):
    magic = 0x1157DF0F956BE95F

    def __init__(self):
        super().__init__()
        self.name_hash = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.name_hash = reader.read_uint32()


EntryTypeManager.register_handler(ResourceWithNameHash)

