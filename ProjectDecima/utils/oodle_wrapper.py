import ctypes
from ctypes import c_size_t, c_char_p, c_int32, c_uint64, c_void_p
from pathlib import Path
from typing import Union

import numpy as np


# typedef int (*WINAPI CompressFn)(int format, const std::uint8_t* src, std::size_t src_len, std::uint8_t* dst, int level, void*, std::size_t, std::size_t, void*, std::size_t);
# typedef int (*WINAPI DecompressFn)(const std::uint8_t* src, std::size_t src_len, std::uint8_t* dst, std::size_t dst_len, int fuzz, int crc, int verbose, std::uint8_t*, std::size_t, void*, void*, void*, std::size_t, int);

class Oodle:
    _local_path = Path(__file__).absolute().parent
    _lib = ctypes.WinDLL(str(_local_path / 'oo2core_7_win64.dll'))
    _compress = _lib.OodleLZ_Compress
    _compress.argtypes = [c_int32, c_char_p, c_size_t, c_char_p, c_int32, c_size_t, c_size_t, c_size_t, c_size_t,
                          c_size_t]
    _compress.restype = c_int32
    _decompress = _lib.OodleLZ_Decompress
    _decompress.argtypes = [c_char_p, c_size_t, c_char_p, c_size_t, c_int32, c_int32, c_int32, c_size_t, c_size_t,
                            c_size_t, c_size_t, c_size_t, c_size_t, c_int32]
    _decompress.restype = c_int32

    @staticmethod
    def decompress(input_buffer: Union[bytes, bytearray], output_size):
        # output_buffer = np.zeros(output_size, dtype=np.uint8)

        # out_data_p = output_buffer.ctypes.data_as(c_char_p)
        out_data_p = ctypes.create_string_buffer(output_size)
        in_data_p = ctypes.create_string_buffer(bytes(input_buffer))
        # print(in_data_p, len(input_buffer), out_data_p, output_size)
        result = Oodle._decompress(in_data_p, len(input_buffer), out_data_p, output_size, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0)
        assert result >= 0, 'Error decompressing chunk'
        return bytes(out_data_p)

    @staticmethod
    def compress(input_buffer: Union[bytes, bytearray], fmt: int = 8, level: int = 4):
        def calculate_compression_bound(size):
            return size + 274 * ((size + 0x3FFFF) // 0x40000)

        out_size = calculate_compression_bound(len(input_buffer))
        out_data_p = ctypes.create_string_buffer(out_size)
        in_data_p = ctypes.create_string_buffer(bytes(input_buffer))

        result = Oodle._compress(fmt, in_data_p, len(input_buffer), out_data_p, level, 0, 0, 0, 0, 0)
        assert result >= 0, 'Error compressing chunk'
        return bytes(out_data_p[:result])
