import binascii
from pathlib import Path

from PIL import Image
from prettytable import PrettyTable

from ProjectDecima.utils.byte_io import ByteIO

pixel_type = {
    0x1F: ("RGBA", ('bcn', 1, 0)),
    19: ("RGBA", ('bcn', 1, 0)),
    12: ("RGBA", ('bcn', 1, 0)),
    0x42: ('RGBA', ('bcn', 1, 0)),
    0x43: ('RGBA', ('bcn', 2, 0)),
    0x44: ('RGBA', ('bcn', 3, 0)),
    0x45: ('L', ('bcn', 4, 0)),
    0x47: ('RGBA', ('bcn', 5, 0)),
    0x4B: ('RGBA', ('bcn', 7, 0)),
}

if __name__ == '__main__':

    # noinspection PyListCreation
    tab_header = ['Real size', 'Size', 'Guid', 'Unk1', 'Width', 'Height', 'Layers', 'Mips',
                  'Pxl fmt',
                  'Unk4',
                  'always 16754944', 'Guid2', 'buffer size', 'ttl data size', 'four ints', 'strlen', 'stream']
    tab_header.append('File')
    table = PrettyTable(tab_header)
    # for file in Path(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\textures').rglob('*.core'):
    for file in Path(r'F:\SteamLibrary\steamapps\common\Death Stranding\dump').rglob('*.core'):
        r = ByteIO(file)
        if r.read_uint64() != 11989732629713595192:
            continue
        file_size = r.read_uint32()
        file_guid = r.read_bytes(16)
        unk = r.read_int16()
        width, height = r.read_fmt('HH')
        layers = r.read_int16()
        mip_count = r.read_int8()
        pixel_fmt = r.read_int8()
        unk4 = r.read_int16()
        unk5 = r.read_uint32()
        file_guid2 = r.read_bytes(16)
        buffer_size = r.read_uint32()
        total_data_size = r.read_uint32()
        four_ints = r.read_fmt('4I')
        str_len = r.read_uint32()
        divider = 1
        try:

            assert str_len < 1000
            divider = 32
            str = Path(r.read_ascii_string(str_len)).stem
            if not str:
                divider = 1
                str = None
                # str = 'KEK_' + file.stem

        except:
            r.rewind(4)

            # str = "ERROR_" + file.stem
            str = None
        u1 = bin(four_ints[0])[2:].zfill(32)
        u2 = bin(four_ints[1])[2:].zfill(32)
        values = [r.size(), file_size + 12, binascii.hexlify(file_guid).upper().decode(), unk, width, height, layers,
                  mip_count, pixel_fmt, unk4, unk5, binascii.hexlify(file_guid2).upper().decode(), buffer_size,
                  total_data_size, (u1,u2), str_len, str, file.stem]
        table.add_row(values)
        img_data = r.read_bytes(total_data_size)
        print(file, hex(pixel_fmt), pixel_type[pixel_fmt], (width // divider, height // divider))
        try:
            if layers != 0:
                # for j in range(unk2):
                im = Image.frombytes(pixel_type[pixel_fmt][0], (width // divider, height // divider * layers), img_data,
                                     *pixel_type[pixel_fmt][1])
                # im.save(f'{str}.png')
            else:
                im = Image.frombytes(pixel_type[pixel_fmt][0], (width // divider, height // divider), img_data,
                                     *pixel_type[pixel_fmt][1])
                # im.save(f'{str}.png')
        except Exception as e:
            print(e)
            print("FAIL")
    print(table)
