from ..utils.byte_io_ds import ByteIODS


class EntryTypeManager:
    _handler = {}
    _default_handler = None

    @classmethod
    def set_default(cls, default_handler):
        cls._default_handler = default_handler

    @classmethod
    def register_handler(cls, handler_class, magic=None):
        if magic is None:
            magic = handler_class.magic
        if magic in cls._handler:
            raise Exception(
                f'Tried to register already registered magic {magic}!\n'
                f'\tRegistered: {cls._handler[magic]}\n'
                f'\tDuplicate : {handler_class}')
        cls._handler[magic] = handler_class

    @classmethod
    def get_handler(cls, magic):
        return cls._handler.get(magic, cls._default_handler)

    @classmethod
    def handle(cls, reader: ByteIODS, core_file):
        magic, size = reader.peek_fmt('QI')
        core_handler = cls.get_handler(magic)
        core_entry = core_handler()
        sub_reader = ByteIODS(reader.read_bytes(size + 12))
        core_entry.parse(sub_reader, core_file)
        return core_entry
