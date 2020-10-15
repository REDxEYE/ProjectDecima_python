from enum import IntEnum
from uuid import UUID

from .byte_io import ByteIO
from ..core.entry_reference import EntryReference
from ..core.entry_types.rtti_object import RTTIRefObject
from ..core.pod.strings import HashedString, UnHashedString


class DSJsonSerializer:
    __storage = {'entry_points': [], 'objects': {}}

    @classmethod
    def begin(cls):
        cls.__storage = {'objects': {}, 'entry_points': []}

    @classmethod
    def add_object(cls, rtti_object: RTTIRefObject):
        def write_data(storage, value=None, name=None, is_list=False):
            import base64
            add = lambda val: storage.append(val) if is_list else storage.update({name: val})

            if not is_list and (name.startswith('_') or name.endswith('_')):
                return
            if type(value) in [str, int, float, HashedString, UnHashedString]:
                add(value)
            elif isinstance(value, UUID):
                add(str(value))
            elif isinstance(value, IntEnum):
                add(int(value))
            elif isinstance(value, bool):
                add(int(value))
            elif type(value) in [bytearray, bytes]:
                add(base64.b64encode(value).decode('utf-8'))
            elif isinstance(value, RTTIRefObject):
                add(cls.add_object(value))
            elif isinstance(value, ByteIO):
                value.seek(0)
                add({
                    'data': base64.b64encode(value.read_bytes(-1)).decode('utf-8'),
                    'size': value.tell()
                })
            elif isinstance(value, EntryReference):
                if value.ref is not None:
                    add(cls.add_object(value.ref))
                elif value.load_method == 0:
                    add(None)
                else:
                    add(str(value.guid))
            elif isinstance(value, (list, tuple, set)):
                tmp = []
                [write_data(tmp, v, is_list=True) for v in value]
                add(tmp)
            elif isinstance(value, dict):
                tmp = {}
                [write_data(tmp, v, str(k)) for (k, v) in value.items()]
                add(tmp)
            else:
                add(dump_object(value))

        def dump_object(obj):
            tmp_storage = {}
            for name, value in obj.__dict__.items():  # type:str,object
                write_data(tmp_storage, value, name)
            return tmp_storage

        object_dump = dump_object(rtti_object)
        if 'class' in object_dump:
            raise Exception(f'"class" field is present in {rtti_object.class_name}')
        object_dump['class'] = rtti_object.class_name
        cls.__storage['objects'][str(rtti_object.guid)] = object_dump
        if rtti_object.exportable:
            cls.__storage['entry_points'].append({'class': rtti_object.class_name, 'guid': str(rtti_object.guid)})

        return str(rtti_object.guid)

    @classmethod
    def finalize(cls):
        return cls.__storage
