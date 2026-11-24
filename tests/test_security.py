from contextlib import closing
import sqlite3
import tempfile
import unittest
from pathlib import Path
from security import sign, claim
from continuum import Store

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = str(Path(self.tmp.name) / "state.db")
        self.key = b"x" * 32
        self.request = {"version":2,"id":"a","operation":"knowledge"}
    def test_replay(self):
        tag = sign(self.request, self.key)
        self.assertEqual(claim(self.request, tag, self.key, self.db), ("a","knowledge"))
        with self.assertRaises(ValueError):
            claim(self.request, tag, self.key, self.db)
    def test_modified_request(self):
        tag = sign(self.request, self.key)
        self.request["id"] = "b"
        with self.assertRaises(ValueError):
            claim(self.request, tag, self.key, self.db)
    def test_wrong_key(self):
        with self.assertRaises(ValueError):
            claim(self.request, sign(self.request, self.key), b"y"*32, self.db)
    def test_restart(self):
        Store(self.db, self.key).save("a", {"step":3})
        self.assertEqual(Store(self.db, self.key).load("a"), {"step":3})
    def test_tamper(self):
        store = Store(self.db, self.key)
        store.save("a", {"step":3})
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("UPDATE snapshots SET payload=?", (b'{"step":4}',))
        with self.assertRaises(ValueError):
            store.load("a")
    def test_short_key(self):
        with self.assertRaises(ValueError):
            sign(self.request, b"short")
