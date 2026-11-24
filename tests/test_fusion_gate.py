import tempfile
import unittest
from pathlib import Path
from fusion_gate import execute
from security import sign
from journal import Journal
from transactional import verify_record

class GateTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db=str(Path(tmp.name)/"gate.db")
        self.key=b"k"*32
        self.req={"version":2,"id":"a","operation":"synthesize","spec":{"parameters":[],"expression":1}}
        self.calls=[]
    def worker(self,request):
        self.calls.append(request)
        return {"value":1}
    def test_bad_signature(self):
        with self.assertRaises(ValueError):
            execute(self.req,"bad",self.key,self.db,self.worker)
        self.assertEqual(self.calls,[])
    def test_replay(self):
        sig=sign(self.req,self.key)
        result=execute(self.req,sig,self.key,self.db,self.worker)
        self.assertTrue(verify_record("a","completed",result,self.key))
        with self.assertRaises(Exception):
            execute(self.req,sig,self.key,self.db,self.worker)
        self.assertEqual(len(self.calls),1)
    def test_denied_operation(self):
        self.req["operation"]="knowledge"
        with self.assertRaises(ValueError):
            execute(self.req,sign(self.req,self.key),self.key,self.db,self.worker)
        self.assertEqual(self.calls,[])
    def test_failure(self):
        def fail(request):
            raise RuntimeError("worker failed")
        with self.assertRaises(RuntimeError):
            execute(self.req,sign(self.req,self.key),self.key,self.db,fail)
        status,evidence=Journal(self.db).get("a")
        self.assertEqual(status,"failed")
        self.assertTrue(verify_record("a",status,evidence,self.key))
