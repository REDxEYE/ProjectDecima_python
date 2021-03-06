from hashlib import md5
from typing import List

import numpy as np

from ..constants import seed, encryption_key_2

try:
    from ..utils import mmh3
except ImportError:
    import mmh3


def decrypt(input_key: List[bytes], data: np.ndarray):
    return np.bitwise_xor(data, np.frombuffer(mmh3.hash_bytes(input_key[0], seed) + mmh3.hash_bytes(input_key[1], seed),
                                              np.uint32, 8))


def decrypt_chunk_data(data: bytes, input_key: bytes):
    iv: np.ndarray = np.frombuffer(mmh3.hash_bytes(input_key, seed), np.uint32, 4)
    iv = np.bitwise_xor(iv, np.array(encryption_key_2, np.uint32))
    digest = np.frombuffer(md5(iv.tobytes()).digest(), np.uint8, 16)
    size = len(data)
    data = np.frombuffer(data, np.uint8)
    data = np.resize(data, (size + 16 - (size % 16),))
    data = np.bitwise_xor(data.reshape((-1, 16)), digest)
    return data.tobytes()[:size]


def hash_string(input_string):
    tmp = input_string.encode("utf8") + b'\x00'
    return mmh3.hash64(tmp, seed, signed=False)[0]
