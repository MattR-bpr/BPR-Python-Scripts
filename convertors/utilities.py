import struct
from typing import BinaryIO, Any


def SwapBytes(fp: BinaryIO, format: str) -> Any:
    size = struct.calcsize(format)
    data = fp.read(size)[::-1]
    fp.seek(-size, 1)
    fp.write(data)
    return struct.unpack(format, data)[0]


def UnpackBytes(fp: BinaryIO, format: str) -> Any:
    size = struct.calcsize(format)
    data = fp.read(size)[::-1]
    return struct.unpack(format, data)[0]