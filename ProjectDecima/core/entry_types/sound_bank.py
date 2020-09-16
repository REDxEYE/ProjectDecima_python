from pathlib import Path
from typing import List, Dict, Type, Tuple

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ..pod.strings import UnHashedString
from ...utils.byte_io_ds import ByteIODS
from ...utils.wwise_sound_bank.section_info import BKHD, DIDX, WWiseSection, DATA, GenericBlock


class SoundDesc(CoreDummy):
    magic = 0xEB0930FE3433F89F

    def __init__(self):
        super().__init__()
        self.sound_refs: List[EntryReference] = []

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        ref_count = reader.read_uint32()
        for _ in range(ref_count):
            ref = EntryReference()
            ref.parse(reader, core_file)
            self.sound_refs.append(ref)


EntryTypeManager.register_handler(SoundDesc)


class WWiseSound(CoreDummy):
    magic = 0x150c273beb8f2d0c
    _sections_handlers = {
        b'BKHD': BKHD,
        b'DIDX': DIDX,
        b'DATA': DATA,
    }

    def __init__(self):
        super().__init__()
        self.unk_0 = 0
        self.wwise_size = 0
        self.unk_1 = 0
        self.sections: Dict[bytes, WWiseSection] = {}
        self.wave_files = []
        self.unk_2 = []
        self.unk_3 = 0
        self.unk_strings: List[Tuple[UnHashedString, Tuple[int]]] = []

    def _get_section_handler(self, magic) -> Type[WWiseSection]:
        return self._sections_handlers.get(magic, GenericBlock)

    def parse(self, reader: ByteIODS, core_file):
        self.header.parse(reader)
        self.guid = reader.read_guid()
        start = reader.tell()
        self.unk_0, self.wwise_size, self.unk_1 = reader.read_fmt('3I')
        sub_reader = ByteIODS(reader.read_bytes(self.wwise_size))
        while sub_reader:
            header, size = sub_reader.peek_fmt('4sI')
            handler = self._get_section_handler(header)
            if handler is not None:
                section = handler()
                section.parse(sub_reader)
                self.sections[section.name] = section
                pass
            else:
                sub_reader.skip(size + 8)
        data: DATA = self.sections.get('DATA', None)
        if data:
            didx: DIDX = self.sections['DIDX']
            for entry in didx.wem_descs:
                data.sub_reader.seek(entry.offset)
                wav_data = data.sub_reader.read_bytes(entry.size)
                self.wave_files.append(wav_data)
        reader.seek(start+self.unk_1)
        reader.skip(4 * 3)
        str_count = reader.read_uint32()
        self.unk_2 = reader.read_fmt(f'{str_count}I')
        self.unk_3 = reader.read_uint8()
        for _ in range(str_count):
            unhased_string = reader.read_unhashed_string()
            unks = reader.read_fmt('7I')
            self.unk_strings.append((unhased_string, unks))

        # self.bank_header.parse(reader)

    def export(self, base_dir: str):
        base_dir = Path(base_dir)
        for n, file in enumerate(self.wave_files):
            with (base_dir / f'file_{n}.wem').open('wb') as f:
                f.write(file)


EntryTypeManager.register_handler(WWiseSound)
