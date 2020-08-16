from struct import unpack
from typing import List

import numpy as np

from ..constants import seed

try:
    from ..utils import mmh3
except ImportError:
    import mmh3


def dectypt(input_key: List[bytes], data: np.ndarray):
    for i in range(2):
        iv = np.frombuffer(mmh3.hash_bytes(input_key[i], seed), np.uint32, 4)
        for j in range(4):
            data[(i * 4) + j] ^= iv[j]
