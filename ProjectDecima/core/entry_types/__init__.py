from .dummy import CoreDummy
from .model import CoreModel
from .shader import CoreShader
from .bone_data import CoreBoneData
from .texture import Texture
from .texture_set import TextureSet
from .unk_model_entry import UnkModelEntry, UnkModelEntry2
from .unk_entry import UnkEntry, MaterialReference
from .mesh_info import IndicesInfo, UnkVertexInfo, MeshInfo, VertexInfo
from .armature import Armature

handlers = {
    0xE2A812418ABC2172: CoreModel,
    0x16bb69a9e5aa0d9e: CoreShader,
    0xBCE84D96052C041E: CoreBoneData,
    0x9FC36C15337A680A: UnkModelEntry,
    0x36B88667B0A33134: UnkModelEntry2,
    0x118378C2F191097A: UnkEntry,
    0xEE49D93DA4C1F4B8: MeshInfo,
    0x3AC29A123FAABAB4: VertexInfo,
    0x5FE633B37CEDBF84: IndicesInfo,
    0x8EB29E71F97E460F: UnkVertexInfo,
    0xFE2843D4AAD255E7: MaterialReference,
    0xA321E8C307328D2E: TextureSet,
    0xA664164D69FD2B38: Texture,
    0x11E1D1A40B933E66: Armature,

}
