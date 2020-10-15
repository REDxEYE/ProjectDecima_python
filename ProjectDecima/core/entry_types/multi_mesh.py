import json
from pathlib import Path
from typing import List

from .model.model_resource import MeshResourceBase, RegularSkinnedMeshResource
from ..core_entry_handler_manager import EntryTypeManager
from ...utils.byte_io_ds import ByteIODS
from ..entry_reference import EntryReference


class MultiMeshResourcePart:
    def __init__(self):
        self.mesh = EntryReference()
        self.world_pos = []
        self.rot_matrix = []

    def parse(self, reader: ByteIODS, core_file):
        self.mesh.parse(reader, core_file)
        self.world_pos = reader.read_fmt('3d')
        self.rot_matrix = reader.read_fmt('3f'), reader.read_fmt('3f'), reader.read_fmt('3f')



class MultiMeshResource(MeshResourceBase):
    # exportable = True
    magic = 0x9FC36C15337A680A

    def __init__(self):
        super().__init__()
        self.parts: List[MultiMeshResourcePart] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        # reader.skip(4)
        for _ in reader.range32():
            part = MultiMeshResourcePart()
            part.parse(reader, core_file)
            self.parts.append(part)

    def export(self, output_path: Path):
        with (output_path / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)


class LodMeshResourcePart:

    def __init__(self):
        self.mesh = EntryReference()
        self.distance = 0

    def parse(self, reader: ByteIODS, core_file):
        self.mesh.parse(reader, core_file)
        self.distance = reader.read_float()



EntryTypeManager.register_handler(MultiMeshResource)


class LodMeshResource(MeshResourceBase):
    exportable = True
    magic = 0x36B88667B0A33134

    def __init__(self):
        super().__init__()
        self.max_distance = 0
        self.lods = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.max_distance = reader.read_float()
        for _ in reader.range32():
            lod = LodMeshResourcePart()
            lod.parse(reader, core_file)
            self.lods.append(lod)

    def export(self, output_path: Path):
        with (output_path / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)



EntryTypeManager.register_handler(LodMeshResource)
