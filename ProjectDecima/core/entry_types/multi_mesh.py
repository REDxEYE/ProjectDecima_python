import json
from pathlib import Path
from typing import List

from ProjectDecima.core.entry_types.model.model_resource import MeshResourceBase, RegularSkinnedMeshResource
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

    def dump(self):
        return {
            'class': self.__class__.__name__,
            'pos': self.world_pos,
            'rot': self.rot_matrix,
            'mesh': self.mesh.dump()
        }


class MultiMeshResource(MeshResourceBase):
    # exportable = True
    magic = 0x9FC36C15337A680A

    def __init__(self):
        super().__init__()
        self.parts: List[MultiMeshResourcePart] = []

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        # reader.skip(4)
        for _ in range(reader.read_uint32()):
            part = MultiMeshResourcePart()
            part.parse(reader, core_file)
            self.parts.append(part)

    def export(self, output_path: Path):
        with (output_path / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'parts': [part.dump() for part in self.parts],
        })
        return out


class LodMeshResourcePart:

    def __init__(self):
        self.mesh = EntryReference()
        self.distance = 0

    def parse(self, reader: ByteIODS, core_file):
        self.mesh.parse(reader, core_file)
        self.distance = reader.read_float()

    def dump(self):
        return {
            'class': self.__class__.__name__,
            'distance': self.distance,
            'mesh': self.mesh.dump()
        }


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
        for _ in range(reader.read_uint32()):
            lod = LodMeshResourcePart()
            lod.parse(reader, core_file)
            self.lods.append(lod)

    def export(self, output_path: Path):
        with (output_path / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)

    def dump(self):
        out = super().dump()
        out.update({
            'class': self.class_name,
            'lods': [part.dump() for part in self.lods]
        })
        return out


EntryTypeManager.register_handler(LodMeshResource)
