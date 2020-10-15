import json
from pathlib import Path
from typing import List, Dict, Tuple

from ..resource import Resource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ...pod.strings import HashedString
from ....utils.byte_io_ds import ByteIODS


class OrientationHelper:
    def __init__(self):
        self.matrix = []
        self.name = HashedString()
        self.index = 0

    def parse(self, reader: ByteIODS):
        self.matrix = reader.read_fmt('16f')
        self.name = reader.read_hashed_string()
        self.index = reader.read_uint32()
        return self



class SkeletonHelpers(Resource):
    exportable = True
    magic = 0xF95259E7154F2739

    def __init__(self):
        super().__init__()
        self.helpers: List[OrientationHelper] = []
        self.names_hashes = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.helpers = [OrientationHelper().parse(reader) for _ in reader.range32()]
        self.names_hashes = [reader.read_uint32() for _ in reader.range32()]

    def export(self, output_path: Path):
        with (output_path / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)



EntryTypeManager.register_handler(SkeletonHelpers)
