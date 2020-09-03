from .dummy import CoreDummy, CoreDummy_60, CoreDummy_4
from .entity import EntityModelInfo, EntityMeshInfo
from .material import Material
from .texture import Texture
from .model import CoreModel
from .shader import CoreShader
from .armature import Armature, ArmatureReference
from .bone_data import CoreBoneData
from .texture_set import TextureSet
from .translation import Translation, VoiceRef, VoiceTranslation, SpeakerInfo
from .unk_entry import BoneRelatedEntry, MaterialReference, UnkEntry, UnkEntry2
from .sound_bank import SoundDesc, WWiseSound
from .collection import CoreRefCollection
from .unk_model_entry import UnkModelEntry, UnkModelEntry2
from .level.level_tile_collection import LevelTileCollection
from .level.level_lod_info import LevelTileLodInfo, LevelTileLod, LevelLodUnk
from .mesh_info import IndicesInfo, UnkVertexInfo, MeshInfo, Vectices, MeshStreamInfo

handlers = {
    0x2F8D786D07E19A72: CoreDummy_60,
    0x3650BFD5E3DDF318: CoreDummy_4,
    0xE59AB7DFD80B9421: CoreDummy_4,
    0x8FAA995D50547F10: CoreDummy_4,
    0xFF5B35CA05453AC: CoreDummy_4,
    0xE2A812418ABC2172: CoreModel,
    0x16bb69a9e5aa0d9e: CoreShader,
    0xBCE84D96052C041E: CoreBoneData,
    0x9FC36C15337A680A: UnkModelEntry,
    0x36B88667B0A33134: UnkModelEntry2,
    0x118378C2F191097A: BoneRelatedEntry,
    0xEE49D93DA4C1F4B8: MeshInfo,
    0xA4341E94120AA306: MeshStreamInfo,
    0x3AC29A123FAABAB4: Vectices,
    0x5FE633B37CEDBF84: IndicesInfo,
    0x8EB29E71F97E460F: UnkVertexInfo,
    0xFE2843D4AAD255E7: MaterialReference,
    0xA321E8C307328D2E: TextureSet,
    0xA664164D69FD2B38: Texture,
    0x11E1D1A40B933E66: Armature,
    0xEB0930FE3433F89F: SoundDesc,
    0x150c273beb8f2d0c: WWiseSound,
    0xf3586131b4f18516: CoreRefCollection,
    0x3c0d150db02d8c80: LevelTileCollection,
    0x8C348AF2D505E5BC: LevelTileLodInfo,
    0x25591EC41134AEA2: LevelTileLod,
    0x81879C362F35924C: LevelLodUnk,
    0x452a16dd4427b5db: EntityModelInfo,
    0xBC79DACC10E13CB7: EntityMeshInfo,
    0xb1d37c8f8304785b: ArmatureReference,
    0x5D1FB9F0D8EA70F4: UnkEntry,
    0x2ED3FA0EE459E5AC: UnkEntry2,
    0xe844b010bf3cfd73: Material,
    0x31be502435317445: Translation,
    0xAD7F486B5DD745A4: VoiceRef,
    0xC726DF870437D774: VoiceTranslation,
    0xE676A549155DA53B: SpeakerInfo,

}
