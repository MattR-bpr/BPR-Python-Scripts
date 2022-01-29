import struct
from typing import Any


def ReadValue(buffer: bytes, offset: int, format: str) -> Any:
    size = struct.calcsize(format)
    buffer = buffer[offset:offset + size]
    value = struct.unpack(format, buffer)
    return value[0] if len(value) == 1 else value


def ReadString(buffer: bytes, offset: int, encoding: str = "ascii") -> str:
    end = buffer.find(b"\x00", offset)
    string = buffer[offset:end]
    return string.decode(encoding)


def GetBytes(format: str, *value: Any) -> bytes:
    value = value[0] if len(value) == 1 else value
    return struct.pack(format, value)