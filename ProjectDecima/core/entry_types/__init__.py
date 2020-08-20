from .dummy import CoreDummy
from .texture import Texture
from .model import CoreModel
from .shader import CoreShader
from .armature import Armature
from .bone_data import CoreBoneData
from .texture_set import TextureSet
from .unk_entry import UnkEntry, MaterialReference
from .sound_bank import SoundDesc, WWiseSound, SoundUnk
from .unk_model_entry import UnkModelEntry, UnkModelEntry2
from .level.level_tile_collection import LevelTileCollection
from .level.level_lod_info import LevelTileLodInfo, LevelTileLod
from .mesh_info import IndicesInfo, UnkVertexInfo, MeshInfo, VertexInfo

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
    0xEB0930FE3433F89F: SoundDesc,
    0x150c273beb8f2d0c: WWiseSound,
    0xf3586131b4f18516: SoundUnk,
    0x3c0d150db02d8c80: LevelTileCollection,
    0x8C348AF2D505E5BC: LevelTileLodInfo,
    0x25591EC41134AEA2: LevelTileLod,

}
