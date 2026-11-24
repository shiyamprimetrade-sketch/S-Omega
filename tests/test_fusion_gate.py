import tempfile
import unittest
from pathlib import Path
from fusion_gate import execute
from security import sign
from journal import Journal

class FusionGateTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db=str(Path(tmp.name)/"gate.db")
        self.key=b"k"*32
        self.req={"version":2,"id":"a","operation":"synthesize","spec":{"parameters":[],"expression":1}}
        self.calls=[]
    def runner(self,req):
        self.calls.append(req)
        return {"value":1}
    def invoke(self,signature,allowed=()):
        return execute(self.req,signature,self.key,self.db,self.runner,allowed=allowed)
    def test_denied(self):
        with self.assertRaises(ValueError):
            self.invoke(sign(self.req,self.key))
        self.assertEqual(self.calls,[])
    def test_bad_signature(self):
        with self.assertRaises(ValueError):
            self.invoke("bad",("synthesize",))
        self.assertEqual(self.calls,[])
    def test_replay(self):
        sig=sign(self.req,self.key)
        self.invoke(sig,("synthesize",))
        with self.assertRaises(Exception):
            self.invoke(sig,("synthesize",))
        self.assertEqual(len(self.calls),1)
    def test_failure(self):
        def fail(req):
            raise RuntimeError("failure")
        with self.assertRaises(RuntimeError):
            execute(self.req,sign(self.req,self.key),self.key,self.db,fail,allowed=("synthesize",))
        self.assertEqual(Journal(self.db).get("a")[0],"failed")
