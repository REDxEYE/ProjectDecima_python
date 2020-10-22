import os
from enum import IntEnum
from pathlib import Path
from uuid import UUID

from .byte_io import ByteIO
from ..core.entry_reference import EntryReference
from ..core.entry_types.rtti_object import RTTIRefObject
from ..core.entry_types.texture import Texture, TextureEntry, ETextureType
from ..core.pod.strings import HashedString, UnHashedString
from ..core.stream_reference import StreamingDataSource


class DSJsonSerializer:
    __storage = {'dump_path': '', 'entry_points': [], 'objects': {}}
    __filepath = Path()
    __dump_path = Path()

    @classmethod
    def begin(cls, dump_path, output_path):
        cls.__storage = {'dump_path': str(dump_path), 'entry_points': [], 'objects': {}}
        cls.__filepath = Path(output_path)
        cls.__dump_path = Path(dump_path)

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
                    'compression': 'zlib',
                    'size': value.tell()
                })

            elif isinstance(value, StreamingDataSource):
                if value.stream_path:
                    stream_path = value.stream_path
                    if not stream_path.endswith('.core.stream'):
                        stream_path += '.core.stream'
                    os.makedirs((cls.__dump_path / stream_path).parent, exist_ok=True)
                    with (cls.__dump_path / stream_path).open('wb') as f:
                        value.stream_reader.seek(0)
                        f.write(value.stream_reader.read_bytes(-1))
                add({
                    'stream_path': value.stream_path,
                    'size': value.size,
                    'offset': value.offset,
                    'channel': value.channel,
                })

            elif isinstance(value, Texture):
                value: Texture
                texture_entry = value.texture_item
                dump_path: str = cls.__storage['dump_path']
                if value.streamed:
                    texture_entry.export(dump_path)
                    texture_path = Path(dump_path) / texture_entry.stream.stream_path
                else:
                    texture_entry.export(Path(cls.__filepath).parent)
                    texture_path = Path(cls.__filepath).parent / str(texture_entry.uuid)
                tmp = {
                    'path': texture_path,
                    'width': texture_entry.width,
                    'height': texture_entry.height,
                    'pixel_format': texture_entry.pixel_format,
                    'type': texture_entry.texture_type,
                }
                if texture_entry.texture_type == ETextureType.Tex3D:
                    tmp['3d_depth'] = texture_entry.tex_3d_depth
                elif texture_entry.texture_type == ETextureType.Tex2DArray:
                    tmp['layers'] = texture_entry.layer_count

                add(tmp)

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
