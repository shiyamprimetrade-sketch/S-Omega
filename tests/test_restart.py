import tempfile
import unittest
from pathlib import Path
from journal import Journal
from restart import interrupt, anchor_record, check_record
from transactional import verify_record

class RestartTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db=str(Path(tmp.name)/"state.db")
        self.key=b"k"*32
        Journal(self.db).begin("a")
    def test_exclusive_required(self):
        with self.assertRaises(ValueError):
            interrupt(self.db,"a",self.key)
        self.assertEqual(Journal(self.db).pending(),["a"])
    def test_interruption(self):
        evidence=interrupt(self.db,"a",self.key,exclusive=True)
        self.assertTrue(verify_record("a","interrupted",evidence,self.key))
        with self.assertRaises(ValueError):
            interrupt(self.db,"a",self.key,exclusive=True)
    def test_anchor(self):
        interrupt(self.db,"a",self.key,exclusive=True)
        anchor=anchor_record(self.db,"a",2,self.key)
        self.assertTrue(check_record(self.db,"a",2,self.key,anchor))
        with self.assertRaises(ValueError):
            check_record(self.db,"a",1,self.key,anchor)
    def test_unfinished_anchor(self):
        with self.assertRaises(ValueError):
            anchor_record(self.db,"a",1,self.key)
