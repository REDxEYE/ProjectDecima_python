from ..utils.byte_io_ds import ByteIODS


class EntryTypeManager:
    """``Class for registering core handlers.``

    To register handler, call EntryTypeManager.register_handler with handler class and magic or handler with `magic` member.
    """
    _handler = {}
    _default_handler = None

    @classmethod
    def set_default(cls, default_handler):
        """Setter of default core entry handler

        :param default_handler: any class with parse method accepting: ByteIODS object and CoreFile object
        """
        cls._default_handler = default_handler

    @classmethod
    def register_handler(cls, handler_class, magic=None):
        """
        :param handler_class: class for handling core entry
        :param magic: magic value for identifying core entry type
        If `magic` is None, `magic` will be took from handler_class
        """
        if magic is None:
            magic = handler_class.magic
        if magic in cls._handler:
            raise Exception(
                f'Tried to register already registered magic {magic}!\n'
                f'\tRegistered: {cls._handler[magic]}\n'
                f'\tDuplicate : {handler_class}')
        cls._handler[magic] = handler_class

    @classmethod
    def _get_handler(cls, magic):
        """Shortcut for handler dictionary"""
        return cls._handler.get(magic, cls._default_handler)

    @classmethod
    def handle(cls, reader: ByteIODS, core_file):
        magic, size = reader.peek_fmt('QI')
        core_handler = cls._get_handler(magic)
        core_entry = core_handler()
        sub_reader = ByteIODS(reader.read_bytes(size + 12))
        core_entry.parse(sub_reader, core_file)
        return core_entry
