import zlib
from functools import reduce
from pathlib import Path
from urllib.parse import unquote

import png
from PIL import Image

from ..utils.byte_io import ByteIO


def read_until_crlf(reader: ByteIO):
    acc = ''
    while True:
        data = reader.read_ascii_string(1)
        if data == '\r' and reader.peek_fmt('1s')[0] == b'\n':
            reader.skip(1)
            break
        else:
            acc += data
    return acc


class SaveFile:
    def __init__(self, path: str):
        self.path = Path(path)
        self._reader = ByteIO(self.path)

        self.unk_0 = ''
        self.unk_1 = ''
        self.unk_2 = ''
        self.slot = ''
        self.title = ''
        self.sub_title = ''
        self.detail = ''
        self.user_param = ''
        self.modification_date = ''

        self.thumbnail: Image.Image = None

    def parse(self):
        reader = self._reader
        self.unk_0 = reader.read_ascii_string(8)
        self.unk_1 = reader.read_ascii_string(8)
        self.unk_2 = reader.read_ascii_string(8)
        self.slot = unquote(read_until_crlf(reader))
        self.title = unquote(read_until_crlf(reader))
        self.sub_title = unquote(read_until_crlf(reader))
        self.detail = unquote(read_until_crlf(reader))
        self.user_param = unquote(read_until_crlf(reader))
        self.modification_date = unquote(read_until_crlf(reader))

        data = png.Reader(reader.file)
        width, height, rows, info = data.asRGBA8()
        rgba_data = bytes(reduce(lambda a, b: a + b, rows))
        self.thumbnail = Image.frombytes('RGBA', (width, height), rgba_data)
        reader.skip(16)
        data = reader.read_bytes(-1)
        decompressed = zlib.decompress(data)
        pass
