# import bpy
import sys
from pathlib import Path

cur_path = Path(__file__).parent
sys.path.append(cur_path)

from ProjectDecima.archive.archive_manager import ArchiveManager
from ProjectDecima.core.pod.entry_reference import RTTIRef
from ProjectDecima.core.pod.stream_reference import StreamReference
import numpy as np

vertex_dtype = np.dtype([('pos', np.float32, (3,)), ('bone_ids', np.uint8, (8,)), ('weights', np.uint8, (8,))])


def handle_model(model: RegularSkinnedMeshResource, ar_set: ArchiveManager):
    mesh_stream = model.mesh_stream.stream_reader

    def pad_offset(block_size):
        mesh_stream.seek(mesh_stream.tell() + (block_size - (mesh_stream.tell() % block_size)))

    # for mesh_info_ref in model.mesh_info_ref:
    #     mesh_info: MeshInfo = mesh_info_ref.ref
    mesh_info: MeshInfo = model.mesh_info_ref[0].ref
    indices_info: IndicesInfo = mesh_info.indices_info.ref
    vertex_info: Vectices = mesh_info.vertex_info.ref
    vertex_count = vertex_info.vertex_count
    indices_count = indices_info.indices_count
    vertex_data = np.frombuffer(mesh_stream.read_bytes(vertex_dtype.itemsize * vertex_count), dtype=vertex_dtype)
    pad_offset(256)
    mesh_stream.skip(8 * vertex_count)
    pad_offset(256)
    uv = np.frombuffer(mesh_stream.read_bytes(4 * vertex_count), dtype=np.float16)
    uv.reshape((2, -1))
    mesh_stream.skip(12 * vertex_count)
    pad_offset(256)
    indices = np.frombuffer(mesh_stream.read_bytes(2 * indices_count), dtype=np.uint16)
    indices.reshape((3, -1))
    pad_offset(256)

    pass


archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
print(f'Loading archives from "{archive_dir}"')
dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
print(f'Dumping files to "{archive_dir}"')
ar_set = ArchiveManager(archive_dir)
ar_set.parse_all()

mesh_path = input("Mesh path:")
core_file = ar_set.queue_file(mesh_path, True)
StreamReference.resolve(ar_set)
RTTIRef.resolve(ar_set)
model_entries = core_file.get_entries_by_type(LodMeshResource)
for model_entry in model_entries:
    model_entry: LodMeshResource
    unk_model_entry: MultiMeshResource = model_entry.parts[0].ref
    models = model_entry.parts[1:]
    models.extend(unk_model_entry.parts)
    for model in models:
        handle_model(model.ref, ar_set)
    pass
