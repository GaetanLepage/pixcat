import sys
import numpy as np
import cv2  # type: ignore
from base64 import standard_b64encode


def serialize_gr_command(**cmd) -> bytes:
    payload = cmd.pop('payload', None)
    cmd_string: str = ','.join('{}={}'.format(k, v) for k, v in cmd.items())
    ans: list[bytes] = []
    w = ans.append
    w(b'\033_G'), w(cmd_string.encode('ascii'))
    if payload:
        w(b';')
        w(payload)
    w(b'\033\\')
    return b''.join(ans)


def write_chunked(**cmd) -> None:
    data: bytes = standard_b64encode(cmd.pop('data'))
    chunk: bytes

    while data:
        chunk, data = data[:4096], data[4096:]
        m = 1 if data else 0
        sys.stdout.buffer.write(serialize_gr_command(payload=chunk, m=m, **cmd))
        sys.stdout.flush()
        cmd.clear()


def display(image_bytes: bytes) -> None:
    write_chunked(a='T', f=100, data=image_bytes)
    print()


def display_numpy(image_array: np.ndarray) -> None:

    encoded_image: np.ndarray = cv2.imencode('.png', image_array)[1]

    display(image_bytes=encoded_image.tobytes())
