"""Local endpoint reservations; caller must retain the socket until shutdown."""
import socket
from contextlib import contextmanager

@contextmanager
def reserve(port=0):
    if type(port) is not int or not 0<=port<=65535 or port==8766:
        raise ValueError("invalid or reserved port")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        if hasattr(socket,"SO_EXCLUSIVEADDRUSE"):
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
        sock.bind(("127.0.0.1",port))
        if sock.getsockname()[1]==8766:
            raise ValueError("reserved port allocated")
        sock.listen(8)
        yield sock
