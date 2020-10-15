import json
from pathlib import Path
from typing import List

from ..resource import Resource
from ..rtti_object import EntityComponentResource
from ...core_entry_handler_manager import EntryTypeManager
from ...entry_reference import EntryReference
from ....utils.byte_io_ds import ByteIODS


class ArtPartsDataResource(EntityComponentResource):
    magic = 0x22105C35921E8D26
    exportable = True

    def __init__(self):
        super().__init__()
        self.root_model = EntryReference()
        self.root_helper_resource = EntryReference()
        self.skinned_model_pose_deformer_resource = EntryReference()
        self.logical_skinned_model_pose_deformer_resource = EntryReference()
        self.skeleton = EntryReference()
        self.representation_skeleton = EntryReference()

        self.effect_array: List[EntryReference] = []
        self.animation_array: List[EntryReference] = []
        self.extra_object_array: List[EntryReference] = []

        self.paint_mask_texture = EntryReference()
        self.pose_rotations = []
        self.pose_translations = []
        self.pose_bounds = []
        self.sub_model_parts_resources: List[EntryReference] = []
        self.model_name_handle = {}
        self.model_name_cover_pre_computed_resources = {}
        self.cover_model_pre_computed_resources: List[EntryReference] = []
        self.orientation_helpers: List[EntryReference] = []
        self.mesh_resource_count = 0
        self.is_rotated_root_model = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.root_model.parse(reader, core_file)
        self.root_helper_resource.parse(reader, core_file)
        self.skinned_model_pose_deformer_resource.parse(reader, core_file)
        self.logical_skinned_model_pose_deformer_resource.parse(reader, core_file)
        self.skeleton.parse(reader, core_file)
        self.representation_skeleton.parse(reader, core_file)

        self.effect_array = [reader.read_ref(core_file) for _ in reader.range32()]
        self.animation_array = [reader.read_ref(core_file) for _ in reader.range32()]
        self.extra_object_array = [reader.read_ref(core_file) for _ in reader.range32()]

        self.paint_mask_texture.parse(reader, core_file)
        self.pose_rotations = [reader.read_fmt('4f') for _ in reader.range32()]
        self.pose_translations = [reader.read_fmt('3f') for _ in reader.range32()]
        self.pose_bounds = reader.read_fmt('6f')
        self.sub_model_parts_resources = [reader.read_ref(core_file) for _ in reader.range32()]
        self.model_name_handle = {reader.read_fmt('2I')[1]: reader.read_uint32() for _ in reader.range32()}
        self.model_name_cover_pre_computed_resources = {reader.read_fmt('2I')[1]: reader.read_uint32() for _ in
                                                        reader.range32()}
        self.cover_model_pre_computed_resources = [reader.read_ref(core_file) for _ in reader.range32()]
        self.orientation_helpers = [reader.read_ref(core_file) for _ in reader.range32()]
        self.mesh_resource_count = reader.read_uint32()
        self.is_rotated_root_model = reader.read_uint8()

    def export(self, path: str):
        with (Path(path) / f'{self.guid}.ds_json').open('w') as f:
            json.dump(self.dump(), f, indent=2)



EntryTypeManager.register_handler(ArtPartsDataResource)
