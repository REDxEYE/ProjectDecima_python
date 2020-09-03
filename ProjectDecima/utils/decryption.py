from hashlib import md5
from typing import List

import numpy as np

from ..constants import seed, encryption_key_2

try:
    from ..utils import mmh3
except ImportError:
    import mmh3


def decrypt(input_key: List[bytes], data: np.ndarray):
    return np.bitwise_xor(data, np.frombuffer(mmh3.hash_bytes(input_key[0], seed) +
                                              mmh3.hash_bytes(input_key[1], seed), np.uint32, 8))


def decrypt_chunk_data(data, input_key):
    iv: np.ndarray = np.frombuffer(mmh3.hash_bytes(input_key, seed), np.uint32, 4)
    iv = np.bitwise_xor(iv, np.array(encryption_key_2, np.uint32))
    digest = np.frombuffer(md5(iv.tobytes()).digest(), np.uint8, 16)
    size = len(data)
    tmp = np.zeros((size + 16 - (size % 16),), dtype=np.uint8)
    tmp[:size] = np.frombuffer(data, np.uint8)
    # data: np.ndarray = np.frombuffer(data, np.uint8)
    # size = data.size
    # data = np.append(data, np.zeros((16 - (size % 16)), np.uint8))
    data = tmp.reshape((-1, 16))
    data = np.bitwise_xor(data, digest)[:size]
    return data.tobytes()[:size]


def hash_string(input_string):
    tmp = input_string.encode("utf8") + b'\x00'
    return mmh3.hash64(tmp, seed, signed=False)[0]
