import ctypes
from ctypes import c_size_t, c_char_p, c_int32, c_uint64, c_void_p
import numpy as np


# typedef int (*WINAPI CompressFn)(int format, const std::uint8_t* src, std::size_t src_len, std::uint8_t* dst, int level, void*, std::size_t, std::size_t, void*, std::size_t);
# typedef int (*WINAPI DecompressFn)(const std::uint8_t* src, std::size_t src_len, std::uint8_t* dst, std::size_t dst_len, int fuzz, int crc, int verbose, std::uint8_t*, std::size_t, void*, void*, void*, std::size_t, int);

class Oodle:
    _lib = ctypes.CDLL('./oo2core_7_win64.dll')
    _compress = _lib.CompressFn
    _compress.argtypes = [c_int32, c_char_p, c_size_t, c_char_p, c_int32, c_void_p, c_size_t, c_size_t, c_void_p,
                          c_size_t]
    _compress.restype = c_int32
    _decompress = _lib.DecompressFn
    _decompress.argtypes = [c_char_p, c_size_t, c_char_p, c_size_t, c_int32, c_int32, c_int32, c_char_p, c_size_t,
                            c_void_p, c_void_p, c_void_p, c_size_t, c_int32]
    _decompress.restype = c_int32

    @staticmethod
    def decompress(input_buffer: np.ndarray, output_size):
        output_buffer = np.zeros(output_size, dtype=np.uint8)

        out_data_p = output_buffer.ctypes.data_as(c_char_p)
        in_data_p = input_buffer.ctypes.data_as(c_char_p)

        result = Oodle._decompress(in_data_p, input_buffer.size, out_data_p, output_size, 0, 0, ctypes.c_void_p(0), 0,
                                   ctypes.c_void_p(0), ctypes.c_void_p(0), ctypes.c_void_p(0), 0, 3)
        assert result >= 0, 'Error decompressing chunk'
        return output_buffer
