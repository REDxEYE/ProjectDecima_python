import importlib
from pathlib import Path
import importlib.util

from ..utils.byte_io_ds import ByteIODS


class EntryTypeManager:
    """``Class for registering core handlers.``

    To register handler, call EntryTypeManager.register_handler with handler class and magic or handler with `magic` member.
    """
    _handler = {}
    _default_handler = None
    __already_seen = []

    @classmethod
    def load_handlers(cls, directory: str):
        for file in Path(directory).rglob('*.py'):
            importlib.import_module(str(file.with_suffix('')).replace('\\', '.'))

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
        print(f'Registered handler for 0x{magic:016X} {handler_class.__name__} ')
        cls._handler[magic] = handler_class

    @classmethod
    def _get_handler(cls, magic):
        """Shortcut for handler dictionary"""
        return cls._handler.get(magic, cls._default_handler)

    @classmethod
    def handle(cls, reader: ByteIODS, core_file):
        magic, size = reader.peek_fmt('QI')
        core_handler = cls._get_handler(magic)
        from .entry_types.dummy import CoreDummy
        if core_handler is CoreDummy:
            if magic not in cls.__already_seen:
                cls.__already_seen.append(magic)
                print(f'Unhandled type: 0x{magic:X}')
        core_entry = core_handler()
        sub_reader = ByteIODS(reader.read_bytes(size + 12))
        core_entry.parse(sub_reader, core_file)
        return core_entry
