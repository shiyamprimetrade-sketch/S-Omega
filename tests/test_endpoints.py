import socket
import unittest
from endpoints import reserve

class EndpointTests(unittest.TestCase):
    def test_loopback(self):
        with reserve() as sock:
            self.assertEqual(sock.getsockname()[0],"127.0.0.1")
    def test_distinct(self):
        with reserve() as a,reserve() as b:
            self.assertNotEqual(a.getsockname(),b.getsockname())
    def test_collision(self):
        with reserve() as a:
            with self.assertRaises(OSError):
                with reserve(a.getsockname()[1]): pass
    def test_reserved(self):
        with self.assertRaises(ValueError):
            with reserve(8766): pass
    def test_invalid(self):
        for port in (True,-1,65536,"1234"):
            with self.assertRaises(ValueError):
                with reserve(port): pass
    def test_connection(self):
        with reserve() as listener:
            listener.settimeout(2)
            with socket.create_connection(listener.getsockname(),timeout=2) as client:
                peer,_=listener.accept()
                with peer:
                    peer.settimeout(2)
                    client.sendall(b"x")
                    self.assertEqual(peer.recv(1),b"x")
