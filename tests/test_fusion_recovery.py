import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from fusion_gate import execute
from fusion_recovery import recover_result
from security import sign
from journal import Journal
from restart import interrupt

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db=str(Path(tmp.name)/"state.db")
        self.key=b"k"*32
        self.req={"version":2,"id":"a","operation":"synthesize","spec":{"parameters":["a"],"expression":"a"}}
    def complete(self):
        return execute(self.req,sign(self.req,self.key),self.key,self.db,lambda r:{"source":"def compute(a): return a"},allowed=("synthesize",))
    def test_recover(self):
        result,_=self.complete()
        self.assertEqual(recover_result(self.db,"a",self.key),result)
    def test_tamper(self):
        _,evidence=self.complete()
        evidence["record"]["result"]["source"]="changed"
        with closing(sqlite3.connect(self.db)) as c,c:
            c.execute("UPDATE tasks SET evidence=? WHERE id='a'",(json.dumps(evidence).encode(),))
        with self.assertRaises(ValueError):
            recover_result(self.db,"a",self.key)
    def test_interruption(self):
        Journal(self.db).begin("a")
        with self.assertRaises(ValueError):
            recover_result(self.db,"a",self.key)
        interrupt(self.db,"a",self.key,exclusive=True)
        self.assertEqual(Journal(self.db).get("a")[0],"interrupted")
        with self.assertRaises(ValueError):
            recover_result(self.db,"a",self.key)
    def test_wrong_key(self):
        self.complete()
        with self.assertRaises(ValueError):
            recover_result(self.db,"a",b"x"*32)
