import os
import tempfile
import unittest
from pathlib import Path
from transactional import inspect, verify_record
from security import sign
from journal import Journal

@unittest.skipUnless(hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd,"POSIX required")
class TransactionalTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.db=str(self.root/"state.db")
        self.key=b"k"*32
        self.req={"version":2,"id":"a","operation":"synthesize","spec":{"parameters":[],"expression":"1"}}
    def test_success(self):
        (self.root/"a").mkdir()
        (self.root/"a"/"compute.py").write_bytes(b"1")
        evidence=inspect(self.req,sign(self.req,self.key),self.key,self.db,self.root)
        self.assertEqual(Journal(self.db).get("a"),("completed",evidence))
        self.assertTrue(verify_record("a","completed",evidence,self.key))
        evidence["record"]["bytes"]=2
        self.assertFalse(verify_record("a","completed",evidence,self.key))
    def test_failure(self):
        with self.assertRaises(OSError):
            inspect(self.req,sign(self.req,self.key),self.key,self.db,self.root)
        status,evidence=Journal(self.db).get("a")
        self.assertEqual(status,"failed")
        self.assertTrue(verify_record("a",status,evidence,self.key))
    def test_bad_auth(self):
        with self.assertRaises(ValueError):
            inspect(self.req,"invalid",self.key,self.db,self.root)
        self.assertEqual(Journal(self.db).pending(),[])
