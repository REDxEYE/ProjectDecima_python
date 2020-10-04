import struct
from builtins import bytes
from enum import IntEnum
from typing import List
from uuid import UUID

from . import CoreDummy
from .resource import Resource
from ..core_entry_handler_manager import EntryTypeManager
from ..entry_reference import EntryReference
from ...utils.byte_io_ds import ByteIODS


class ERenderTechniqueSetType(IntEnum):
    Invalid_rendering_techniques = -1
    Normal_rendering_techniques = 0
    Instanced_techniques = 1


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


class ESortMode(IntEnum):
    FrontToBack = 1
    BackToFront = 2
    Off = 0


class ESortOrder(IntEnum):
    SR_0 = 0
    SR_1 = 1
    SR_2 = 2
    SR_3 = 3
    SR_4 = 4
    SR_5 = 5
    SR_6 = 6
    SR_7 = 7
    SR_8 = 8
    SR_9 = 9
    SR_10 = 10
    SR_11 = 11
    SR_12 = 12
    SR_13 = 13
    SR_14 = 14
    SR_15 = 15


class ERenderEffectType(IntEnum):
    Object = 0,
    Spotlight = 1,
    Omnilight = 2,
    Sunlight = 3,


class EnvironmentInteractionTargets(IntEnum):
    Unknown = 0
    Snow = 1
    PrecipitationOcclusion = 2
    Vegetation = 4
    ForceSystemBit = -2147483648


class ShaderSamplerBinding:
    def __init__(self):
        self.binding_name_hash = 0
        self.sampler_data = 0

    def parse(self, reader: ByteIODS):
        self.binding_name_hash, self.sampler_data = reader.read_fmt('2I')

    def dump(self):
        return {
            'binding_name_hash': self.binding_name_hash,
            'sampler_data': self.sampler_data,
        }


class SamplerBindingWithHandle(ShaderSamplerBinding):
    def __init__(self):
        super().__init__()
        self.sampler_binding_handle = 0

    def parse(self, reader: ByteIODS):
        super().parse(reader)
        self.sampler_binding_handle = reader.read_uint64()

    def dump(self):
        out = super().dump()
        out.update({
            'sampler_binding_handle': self.sampler_binding_handle
        })
        return out


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

    def dump(self):
        return {
            'binding_name_hash': self.binding_name_hash,
            'swizzle_hash': self.swizzle_hash,
            'sampler_name_hash': self.sampler_name_hash,
            'packed_data': self.packed_data,
            'texture': self.texture.dump(),
        }


class TextureBindingWithHandle(ShaderTextureBinding):
    def __init__(self):
        super().__init__()
        self.texture_binding_handle = 0
        self.swizzle_binding_handle = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.texture_binding_handle = reader.read_uint64()
        self.swizzle_binding_handle = reader.read_uint64()

    def dump(self):
        out = super().dump()
        out.update({
            'texture_binding_handle': self.texture_binding_handle,
            'swizzle_binding_handle': self.swizzle_binding_handle,
        })
        return out


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
        self.variable_data = reader.read_bytes(16)
        (self.binding_name_hash, self.variable_id_hash) = reader.read_fmt('2I')
        self.type = EShaderVariableType(reader.read_uint8())
        self.animator.parse(reader, core_file)

    def dump(self):
        import base64
        return {
            'binding_name_hash': self.binding_name_hash,
            'variable_id_hash': self.variable_id_hash,
            'type': self.type.value,
            'variable_data': base64.b64encode(self.variable_data).decode('utf-8'),
            'animator': self.animator.dump(),

        }


class VariableBindingWithHandle(ShaderVariableBinding):
    def __init__(self):
        super().__init__()
        self.var_binding_handle = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.var_binding_handle = reader.read_uint64()

    def dump(self):
        out = super().dump()
        out.update({
            'var_binding_handle': self.var_binding_handle,
        })
        return out


class SRTBindingCache:
    def __init__(self):
        self.texture_binding_mask = 0
        self.binding_data_mask = 0
        self.srt_entries_mask = 0
        self.binding_data_indices = []
        self.srt_entry_handles = []

    def parse(self, reader: ByteIODS):
        self.texture_binding_mask, self.binding_data_mask, self.srt_entries_mask = reader.read_fmt('<BHQ')
        array_size = reader.read_uint32()
        self.binding_data_indices = reader.read_fmt(f'{array_size}H')
        array_size = reader.read_int32()
        self.srt_entry_handles = reader.read_fmt(f'{array_size}Q')

    def dump(self):
        return {
            'texture_binding_mask': self.texture_binding_mask,
            'binding_data_mask': self.binding_data_mask,
            'srt_entries_mask': self.srt_entries_mask,
            'binding_data_indices': self.binding_data_indices,
            'srt_entry_handles': self.srt_entry_handles,
        }


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
        self.state = reader.read_bytes(8)
        self.srt_binding_cache.parse(reader)
        self.type = ERenderTechniqueType(reader.read_uint32())

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
        self.id = reader.read_uint64()
        self.force_lod_fade = reader.read_uint8()

    def dump(self):
        import base64
        return {
            'state': base64.b64encode(self.state).decode('utf-8'),
            'srt_binding_cache': self.srt_binding_cache.dump(),
            'type': self.type.value,
            'gpu_skinned': self.gpu_skinned,
            'write_global_vertex_cache': self.write_global_vertex_cache,
            'camera_facing': self.camera_facing,
            'initially_enabled': self.initially_enabled,
            'material_layer_id': self.material_layer_id,
            'sampler_binding': [bind.dump() for bind in self.sampler_binding],
            'texture_binding': [bind.dump() for bind in self.texture_binding],
            'variable_binding': [bind.dump() for bind in self.variable_binding],
            'shader': self.shader.dump(),
            'id': self.id,
            'force_lod_fade': self.force_lod_fade,

        }


class RenderTechniqueSet:
    def __init__(self):
        self.render_techniques: List[RenderTechnique] = []
        self.type = ERenderTechniqueSetType.Invalid_rendering_techniques
        self.effect_type = ERenderEffectType.Object
        self.available_techniques_mask = 0
        self.init_enabled_techniques_mask = 0

    def parse(self, reader: ByteIODS, core_file):
        array_size = reader.read_uint32()
        for _ in range(array_size):
            rt = RenderTechnique()
            rt.parse(reader, core_file)
            self.render_techniques.append(rt)

        self.type = ERenderTechniqueSetType(reader.read_int32())
        self.effect_type = ERenderEffectType(reader.read_uint32())
        self.available_techniques_mask = reader.read_int32()
        self.init_enabled_techniques_mask = reader.read_int32()

        return self

    def dump(self):
        return {
            'render_techniques': [rt.dump() for rt in self.render_techniques],
            'type': self.type.value,
            'effect_type': self.effect_type.value,
            'available_techniques_mask': self.available_techniques_mask,
            'init_enabled_techniques_mask': self.init_enabled_techniques_mask,
        }


class RenderEffectResource(Resource):
    magic = 0xe844b010bf3cfd73

    def __init__(self):
        super().__init__()
        self.object_attribute_animator_resource = EntryReference()
        self.technique_sets: List[RenderTechniqueSet] = []
        self.sort_mode = ESortMode.Off
        self.sort_order = ESortOrder.SR_0
        self.render_effect = ERenderEffectType.Object
        self.env_interaction_targets = EnvironmentInteractionTargets.Snow

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.object_attribute_animator_resource.parse(reader, core_file)
        array_size = reader.read_uint32()
        for _ in range(array_size):
            entry = RenderTechniqueSet().parse(reader, core_file)
            self.technique_sets.append(entry)
        self.sort_mode = ESortMode(reader.read_uint32())
        self.sort_order = ESortOrder(reader.read_uint32())
        self.render_effect = ERenderEffectType(reader.read_uint32())
        reader.skip(2)
        self.env_interaction_targets = EnvironmentInteractionTargets(reader.read_uint32())

    def dump(self) -> dict:
        return {
            'object_attribute_animator_resource': self.object_attribute_animator_resource.dump(),
            'technique_sets': [ts.dump() for ts in self.technique_sets],
            'sort_mode': self.sort_mode.value,
            'sort_order': self.sort_order.value,
            'render_effect': self.render_effect.value,
            'env_interaction_targets': self.env_interaction_targets.value,
        }


EntryTypeManager.register_handler(RenderEffectResource)


class ShadingGroup(Resource):
    magic = 0xFE2843D4AAD255E7

    def __init__(self, ):
        super().__init__()
        self.render_effect = EntryReference()
        self.material_type = 0

    def parse(self, reader: ByteIODS, core_file):
        super().parse(reader, core_file)
        self.render_effect.parse(reader, core_file)
        self.material_type = reader.read_uint8()

    def dump(self):
        return {
            'class': self.class_name,
            'render_effect': self.render_effect.dump(),
            'material_type': self.material_type,
        }


EntryTypeManager.register_handler(ShadingGroup)
