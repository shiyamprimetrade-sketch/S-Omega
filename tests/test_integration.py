import os
import tempfile
import unittest
from pathlib import Path
from integration import inspect
from security import sign
from continuum import Store

@unittest.skipUnless(hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd,"POSIX required")
class IntegrationTests(unittest.TestCase):
    def test_inspection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"task").mkdir()
            (root/"task"/"compute.py").write_bytes(b"42")
            db = str(root/"state.db")
            key = b"k"*32
            req = {"version":2,"id":"task","operation":"synthesize","spec":{"parameters":[],"expression":"42"}}
            tag = sign(req,key)
            result = inspect(req,tag,key,db,root)
            self.assertEqual(result["bytes"],2)
            self.assertEqual(Store(db,key).load("task"),result)
            with self.assertRaises(ValueError):
                inspect(req,tag,key,db,root)
