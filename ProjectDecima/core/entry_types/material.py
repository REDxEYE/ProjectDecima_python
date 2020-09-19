import struct
from builtins import bytes
from enum import IntEnum
from typing import List
from uuid import UUID

from . import CoreDummy
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class MatVar:
    def __init__(self):
        self.ref = EntryReference()
        self.data = []

    def parse(self, reader: ByteIODS, core_file):
        self.ref.parse(reader, core_file)
        type_magic = reader.read_uint64()

        if type_magic in [1131449004589570, 2257898667246082, 10139198015144450, 11265097921987074, 1131998760403458,
                          9013298108301826, 7887398201459202, 6098853560834, 31531296245154306, 34908995965682178,
                          32657196151996930, 37160795779367426, 36034895872524802, 22524096990413314, 15768697549357570,
                          13516897735672322, 14642797642514946, 20272297176728066, 12390997828829698, 24775896804098562,
                          30405396338311682, 29279496431469058, 27027696617783810, 18020497363042818, 25901796710941186,
                          16894597456200194, 3383798574088706, 5635598387773954, 6761498294616578, 4509698480931330,
                          21398197083570690, 19146397269885442, 10141946794213890, 4512447260000770, 5638347166843394,
                          1132548516217346]:
            self.data = reader.read_fmt('6I')
        elif type_magic in [5549097746946, 6648609374722]:
            reader.skip(12)
            self.data = reader.read_fmt(f'4f{52 // 4}I')
        elif type_magic in [23649996897255938, 6764247073686018]:
            reader.skip(8)
            count = reader.read_uint32()
            for _ in range(count):
                self.data.append(reader.read_fmt(f'<4fQHIBBH'))

        else:
            raise NotImplementedError(f"Unknown type:{type_magic} offset: {reader.tell()}")
        return self


class ERenderTechniqueSetType(IntEnum):
    Invalid_rendering_techniques = -1
    Normal_rendering_techniques = 0
    Instanced_techniques = 1


class ERenderEffectType(IntEnum):
    Object_render_effect = 0
    Spotlight_render_effect = 1
    Omnilight_render_effect = 2
    Sunlight_render_effect = 3


class ERenderTechniqueType(IntEnum):
    Invalid = -1
    Direct = 0
    Unlit = 1
    DepthOnly = 2
    MaskedDepthOnly = 3
    Deferred = 4
    DeferredSimplified = 12
    DeferredEmissive = 5
    DeferredTransAcc = 6
    DeferredTrans = 7
    CustomDeferredBackground = 8
    CustomDeferredNormalRead = 10
    CustomDeferredDepthWrite = 11
    CustomDeferred = 9
    HalfDepthOnly = 13
    LightSampling = 14
    CustomForward = 15
    Transparency = 16
    ForwardBackground = 17
    ForwardWaterFromBelow = 18
    ForwardHalfRes = 19
    ForwardQuarterRes = 20
    ForwardMotionVectors = 21
    ForwardForeground = 22
    VolumeLightAmount = 23
    Shadowmap = 24


class ShaderSamplerBinding:
    def __init__(self):
        self.binding_name_hash = 0
        self.sampler_data = 0

    def parse(self, reader: ByteIODS):
        self.binding_name_hash, self.sampler_data = reader.read_fmt('2I')


class SamplerBindingWithHandle(ShaderSamplerBinding):
    def __init__(self):
        super().__init__()
        self.sampler_binding_handle = 0

    def parse(self, reader: ByteIODS):
        super().parse(reader)
        self.sampler_binding_handle = reader.read_uint32()


class ShaderTextureBinding:
    def __init__(self):
        self.binding_name_hash = 0
        self.swizzle_hash = 0
        self.sampler_name_hash = 0
        self.packed_data = 0
        self.texture = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        (self.binding_name_hash, self.swizzle_hash, self.sampler_name_hash, self.packed_data) = reader.read_fmt('4I')
        self.texture.parse(reader, core_file)


class TextureBindingWithHandle(ShaderTextureBinding):
    def __init__(self):
        super().__init__()
        self.texture_binding_handle = 0
        self.swizzle_binding_handle = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.texture_binding_handle = reader.read_uint32()
        self.swizzle_binding_handle = reader.read_uint32()


class EShaderVariableType(IntEnum):
    Float1 = 1
    Float2 = 2
    Float3 = 3
    Float4 = 4
    Uint1 = 9
    Uint2 = 10
    Uint3 = 11
    Uint4 = 12
    Int1 = 17
    Int2 = 18
    Int3 = 19
    Int4 = 20
    ShaderFloat1 = 33
    ShaderFloat2 = 34
    ShaderFloat3 = 35
    ShaderFloat4 = 36
    VertexFloat1 = 65
    VertexFloat2 = 66
    VertexFloat3 = 67
    VertexFloat4 = 68
    ConstFloat1 = 97
    ConstFloat2 = 98
    ConstFloat3 = 99
    ConstFloat4 = 100
    ConstUint1 = 105
    ConstUint2 = 106
    ConstUint3 = 107
    ConstUint4 = 108
    ConstInt1 = 113
    ConstInt2 = 114
    ConstInt3 = 115
    ConstInt4 = 116
    InstanceDataOffsetFloat1 = 129
    InstanceDataOffsetFloat2 = 130
    InstanceDataOffsetFloat3 = 131
    InstanceDataOffsetFloat4 = 132


class ShaderVariableBinding:
    def __init__(self):
        self.binding_name_hash = 0
        self.variable_id_hash = 0
        self.type = EShaderVariableType.Float1
        self.variable_data = bytes()
        self.animator = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        (self.binding_name_hash, self.variable_id_hash) = reader.read_fmt('2I')
        self.type = EShaderVariableType(reader.read_uint8())
        self.variable_data = reader.read_bytes(16)
        self.animator.parse(reader, core_file)


class VariableBindingWithHandle(ShaderVariableBinding):
    def __init__(self):
        super().__init__()
        self.var_binding_handle = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.var_binding_handle = reader.read_uint32()


class SRTBindingCache:
    def __init__(self):
        self.texture_binding_mask = 0
        self.binding_data_mask = 0
        self.srt_entries_mask = 0
        self.binding_data_indices = []
        self.srt_entry_handles = []

    def parse(self, reader: ByteIODS):
        self.texture_binding_mask, self.binding_data_mask, self.srt_entries_mask = reader.read_fmt('BHQ')
        array_size = reader.read_uint32()
        self.binding_data_indices = reader.read_fmt(f'{array_size}H')
        array_size = reader.read_int32()
        self.srt_entry_handles = reader.read_fmt(f'{array_size}Q')


class RenderTechnique:
    def __init__(self):
        self.state = bytes()
        self.srt_binding_cache = SRTBindingCache()
        self.type = ERenderTechniqueType(-1)
        self.gpu_skinned = 0
        self.write_global_vertex_cache = 0
        self.camera_facing = 0
        self.initially_enabled = 0
        self.material_layer_id = 0
        self.sampler_binding = []
        self.texture_binding = []
        self.variable_binding = []
        self.shader = EntryReference()
        self.id = 0
        self.force_lod_fade = 0

    def parse(self, reader: ByteIODS, core_file):
        self.state = reader.read_bytes(1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 4 + 4 + 2 + 2 + 4)
        self.srt_binding_cache.parse(reader)
        self.type = ERenderTechniqueType(reader.read_uint8())
        self.gpu_skinned = reader.read_uint8()
        self.write_global_vertex_cache = reader.read_uint8()
        self.camera_facing = reader.read_uint8()
        self.initially_enabled = reader.read_uint8()
        self.material_layer_id = reader.read_int32()
        array_size = reader.read_uint32()
        for _ in range(array_size):
            bind = SamplerBindingWithHandle()
            bind.parse(reader)
            self.sampler_binding.append(bind)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            bind = TextureBindingWithHandle()
            bind.parse(reader, core_file)
            self.texture_binding.append(bind)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            bind = VariableBindingWithHandle()
            bind.parse(reader, core_file)
            self.variable_binding.append(bind)
        self.shader.parse(reader, core_file)
        self.id = reader.read_uint32()
        self.force_lod_fade = reader.read_uint8()


class RenderTechniqueSet:
    def __init__(self):
        self.render_techniques: List[RenderTechnique] = []
        self.type = ERenderTechniqueSetType.Invalid_rendering_techniques
        self.effect_type = ERenderEffectType.Object_render_effect
        # self.unks_0 = []
        # self.unk_shorts_1 = []
        # self.unk_blocks_2 = []
        # self.unk_3 = 0
        # self.unk_4 = 0
        # self.unk_5 = 0
        # self.unk_blocks_6 = []
        # self.unks_7 = []
        # self.unks_8 = []
        #
        # self.vars: List[MatVar] = []
        # self.shader_ref = EntryReference()

    def parse(self, reader: ByteIODS, core_file):
        array_size = reader.read_uint32()
        for _ in range(array_size):
            rt = RenderTechnique()
            rt.parse(reader, core_file)
            self.render_techniques.append(rt)
        self.type = ERenderTechniqueSetType(reader.read_int32())
        self.effect_type = ERenderEffectType(reader.read_int32())
        # self.unks_0 = reader.read_fmt(f'{20 // 4}I')
        # unk_count = reader.read_uint32()
        # self.unk_shorts_1 = reader.read_fmt(f'{unk_count}H')
        # unk_block_count = reader.read_uint32()
        # for _ in range(unk_block_count):
        #     self.unk_blocks_2.append(reader.read_fmt('<BBIBB'))
        # self.unk_3, self.unk_4, self.unk_5 = reader.read_fmt('3I')
        # unk_block_count = reader.read_uint32()
        # for _ in range(unk_block_count):
        #     self.unk_blocks_6.append(reader.read_bytes(16))
        # ref_count = reader.read_uint32()
        # if ref_count > 0:
        #     self.unks_8 = reader.read_fmt(f'4I')
        # else:
        #     self.unks_8 = reader.read_fmt('I')
        # for _ in range(ref_count):
        #     var = MatVar().parse(reader, core_file)
        #     self.vars.append(var)
        # self.shader_ref.parse(reader, core_file)
        return self


class RenderEffectResource(CoreDummy):
    magic = 0xe844b010bf3cfd73

    def __init__(self):
        super().__init__()
        self.object_attribute_animator_resource = EntryReference()
        self.unks_0 = []

        self.technique_sets: List[RenderTechniqueSet] = []

    def parse(self, reader: ByteIODS, core_file):
        with open('SHADING_GROUP.bin', 'wb') as f:
            with reader.save_current_pos():
                reader.seek(0)
                f.write(reader.read_bytes(-1))
        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.object_attribute_animator_resource.parse(reader, core_file)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            entry = RenderTechniqueSet().parse(reader, core_file)

            self.technique_sets.append(entry)


EntryTypeManager.register_handler(RenderEffectResource)


class ShadingGroup(CoreDummy):
    magic = 0xFE2843D4AAD255E7

    def __init__(self, ):
        super().__init__()
        self.render_effect = EntryReference()
        self.material_type = 0

    def parse(self, reader: ByteIODS, core_file):

        self.header.parse(reader)
        self.guid = reader.read_guid()
        self.render_effect.parse(reader, core_file)
        self.material_type = reader.read_uint8()


EntryTypeManager.register_handler(ShadingGroup)
