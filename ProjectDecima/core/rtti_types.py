import json
from functools import partial
from hashlib import md5
from pathlib import Path
from typing import Dict, Type, cast
from .pod.array import RTTIArray
from yaml import load, CLoader

from .pod.dict import RTTIHashMap
from .pod.entry_reference import RTTIRef
from .pod.float import RTTIFloat32, RTTIFloat64, RTTIFloat16, RTTIFloat
from .pod.gguuid import RTTIGGUUID
from .pod.int import *
from .pod.stream_reference import RTTIStreamRef
from .pod.strings import HashedString, WUnHashedString, RTTIString
from .type_proxy import RTTITypeProxy
from ..utils.byte_io_ds import ByteIODS
from ..utils.singleton import SingletonMeta

indent = 0


class RTTIDummy(RTTIType):
    _size = 0

    def __init__(self):
        self.data = b''

    def from_buffer(self, buffer: ByteIODS):
        self.data = buffer.read_bytes(self._size)
        return self

    def to_file(self, buffer: ByteIODS):
        buffer.write_bytes(self.data)


class RTTITypeReadBase(RTTIType):
    _field_metadata = {}
    _base_order = []

    def __init__(self):
        _type_registry = RTTITypeRegistry()
        for base_name in self._base_order:
            for new_field in self._field_metadata[base_name]:
                new_type = _type_registry.construct_object(new_field['type'])
                if isinstance(new_type, type) and issubclass(new_type, (RTTIFlag, RTTIEnum)):
                    setattr(self, new_field['name'], new_type)
                else:
                    setattr(self, new_field['name'], new_type())

    def from_buffer(self, buffer: ByteIODS):
        global indent
        indent += 1
        print("\t" * indent, 'Reading', self._base_order[-1])
        indent += 1
        for base_name in self._base_order:
            for new_field in self._field_metadata[base_name]:
                if new_field.get('is_savestate', False):
                    continue
                field = getattr(self, new_field['name'])
                print("\t" * indent, 'Reading', new_field['name'], new_field['type'])
                from_buffer = field.from_buffer(buffer)
                setattr(self, new_field['name'], from_buffer)
                print("\t" * (indent + 1), field)
        indent -= 2
        return self

    def to_file(self, buffer: ByteIODS):
        pass

    def __repr__(self):
        return f"<RTTIObject {self.__class__.__name__!r}>"

    @classmethod
    def get_fields(cls):
        return cls._field_metadata

    @classmethod
    def get_base_order(cls):
        return cls._base_order

    @classmethod
    def add_base(cls, base_class: Type['RTTITypeReadBase']):
        cls._base_order = base_class.get_base_order().copy() + cls._base_order

    @classmethod
    def add_fields(cls, fields_dict):
        cls._field_metadata.update(fields_dict)


class RTTITypeRegistry(metaclass=SingletonMeta):
    def __init__(self):
        self._constructed_classes = {}
        self.registry_hash = {}
        self.name_to_hash = {}
        self.hash_to_name = {}

        self._internal_types = {
            'HashMap': RTTIHashMap,
            'HashSet': RTTIHashMap,
            'Array': RTTIArray,
            'Ref': RTTIRef,
            'CPtr': RTTIRef,
            'bool': RTTIUInt8,
            'int': RTTIInt32,
            'uint': RTTIUInt32,
            'int8': RTTIInt8,
            'uint8': RTTIUInt8,
            'int16': RTTIInt16,
            'uint16': RTTIUInt16,
            'wchar': RTTIUInt16,
            'ucs4': RTTIInt32,
            'int32': RTTIInt32,
            'uint32': RTTIUInt32,
            'int64': RTTIInt64,
            'uint64': RTTIUInt64,
            'uint128': RTTIUInt128,
            'LinearGainFloat': RTTIFloat32,
            'HalfFloat': RTTIFloat16,
            'float': RTTIFloat32,
            'double': RTTIFloat64,
            'GGUUID': RTTIGGUUID,
            'Filename': HashedString,
            'String': HashedString,
            'WString': WUnHashedString,
            'MaterialType': RTTIUInt16,
            'AnimationNodeID': RTTIUInt16,
            'AnimationTagID': RTTIUInt32,
            'PhysicsCollisionFilterInfo': RTTIUInt32,
            'AnimationEventID': RTTIUInt32,
            'AnimationSet': RTTIUInt32,
            'MusicTime': RTTIUInt64,
            'StreamHandle': RTTIStreamRef,
            'uint64_PLACEMENT_LAYER_MASK_SIZE': type(f'Array<UInt64>', (RTTIArray,),
                                                     {'_expected_type': RTTIUInt64}),
            'uint16_PBD_MAX_SKIN_WEIGHTS': type(f'Array<UInt16>', (RTTIArray,),
                                                {'_expected_type': RTTIUInt16}),
            'uint8_PBD_MAX_SKIN_WEIGHTS': type(f'Array<UInt8>', (RTTIArray,),
                                               {'_expected_type': RTTIUInt8}),
            'float_GLOBAL_APP_RENDER_VAR_COUNT': type(f'Array<Float>', (RTTIArray,),
                                                      {'_expected_type': RTTIFloat32}),
            'float_GLOBAL_RENDER_VAR_COUNT': type(f'Array<Float>', (RTTIArray,),
                                                  {'_expected_type': RTTIFloat32}),
            'ShaderProgramResourceSet_36': type(f'Array<ShaderProgramResourceSet>', (RTTIArray,),
                                                {'_expected_type': RTTITypeProxy('ShaderProgramResourceSet', self)}),
            'EnvelopeSegment_MAX_ENVELOPE_SEGMENTS': type(f'Array<EnvelopeSegment>', (RTTIArray,),
                                                          {'_expected_type': RTTITypeProxy('EnvelopeSegment', self)}),
            'GlobalRenderVariableInfo_GLOBAL_RENDER_VAR_COUNT': type(f'Array<GlobalRenderVariableInfo>', (RTTIArray,),
                                                                     {'_expected_type': RTTITypeProxy(
                                                                         'GlobalRenderVariableInfo', self)}),
            'GlobalAppRenderVariableInfo_GLOBAL_APP_RENDER_VAR_COUNT': type(f'Array<GlobalAppRenderVariableInfo>',
                                                                            (RTTIArray,),
                                                                            {'_expected_type': RTTITypeProxy(
                                                                                'GlobalAppRenderVariableInfo', self)}),
        }

    def inject(self, type_hash, type_class):
        self._constructed_classes[type_hash] = type_class

    def from_file(self, registry_path: Path):
        json_cache = {'hash': 0, 'types': []}
        types = []
        with registry_path.open('r') as f:

            yaml_hash = md5(f.read().encode('utf8')).hexdigest()
            f.seek(0)
            if registry_path.with_suffix('.json').exists():
                with registry_path.with_suffix('.json').open('r') as fj:
                    json_cache = json.load(fj)
                if json_cache['hash'] == yaml_hash:
                    types = json_cache['types']
            if not types:
                types = load(f, CLoader)
                json_cache['hash'] = yaml_hash
                json_cache['types'] = types
                with registry_path.with_suffix('.json').open('w') as fj:
                    json.dump(json_cache, fj)
        for type_name, type_info in types.items():
            type_info['name'] = type_name
            type_id = type_info['typeid']
            self.registry_hash[type_id] = type_info
            self.name_to_hash[type_name] = type_id
            self.hash_to_name[type_id] = type_name
        return self

    def find_by_hash(self, type_hash):
        python_class = self._constructed_classes.get(type_hash, None)
        if python_class is None:
            python_class = self.generate_python_class(self.registry_hash[type_hash])
            self._constructed_classes[type_hash] = python_class
        return python_class

    def find_by_name(self, type_name):
        type_hash = self.name_to_hash.get(type_name)
        if type_hash is None:
            return
        return self.find_by_hash(type_hash)

    def find_metadata_by_name(self, type_name):
        type_hash = self.name_to_hash.get(type_name, None)
        if type_hash is None:
            return
        return self.registry_hash[type_hash]

    def _parse_type_string(self, type_string: str):
        if '<' in type_string:
            start = type_string.find('<')
            base_type = self._parse_type_string(type_string[:start])
            the_rest = self._parse_type_string(type_string[start + 1:-1])
            return type(type_string, (base_type,), {'_expected_type': the_rest})
        if type_string in self._internal_types:
            return self._internal_types[type_string]
        elif type_string in self.name_to_hash:
            return self.find_by_name(type_string)
        return type_string

    def generate_python_class(self, type_info):
        type_name = type_info['name']
        if type_info['type'] == 'class':
            field_meta = type_info['members'] or []
            fields = {"_field_metadata": {type_name: field_meta},
                      '_base_order': [type_name]}
            bases = []
            if type_info['bases']:
                for base in type_info['bases']:
                    base_class: RTTITypeReadBase = self.find_by_name(base['name'])
                    bases.append(base_class)
            else:
                bases.append(RTTITypeReadBase)
            new_type: Type[RTTITypeReadBase] = cast(Type[RTTITypeReadBase], type(type_name, tuple(bases), fields))

            if type_info['bases']:
                for base in type_info['bases']:
                    base_name = base['name']
                    base_class: Type[RTTITypeReadBase] = self.find_by_name(base_name)
                    new_type.add_base(base_class)
                    new_type.add_fields(base_class.get_fields())
                    bases.append(base_class)
            return new_type

        elif type_info['type'] == 'enum':
            enum_size_to_base_class = {
                1: RTTIEnumUInt8,
                2: RTTIEnumUInt16,
                4: RTTIEnumUInt32,
            }
            return enum_size_to_base_class[type_info['size']](type_name,
                                                              {k: v for k, v in type_info['values']})

        elif type_info['type'] == 'enum class':
            enum_size_to_base_class = {
                1: RTTIFlagUInt8,
                2: RTTIFlagUInt16,
                4: RTTIFlagUInt32,
            }
            return enum_size_to_base_class[type_info['size']](type_name,
                                                              {k: v for k, v in type_info['values']})

        else:
            raise NotImplementedError(f'Failed to generate class for {type_info["name"]}')

    def construct_object(self, type_string):
        return self._parse_type_string(type_string)
