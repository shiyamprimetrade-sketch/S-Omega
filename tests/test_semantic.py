import unittest
from semantic import verify_source

class SemanticTests(unittest.TestCase):
    spec={"parameters":["a","b"],"expression":["add","a","b"]}
    def test_correct(self):
        self.assertTrue(verify_source(self.spec,b"def compute(a,b): return a+b"))
    def test_wrong_operator(self):
        self.assertFalse(verify_source(self.spec,b"def compute(a,b): return a-b"))
    def test_extra_code(self):
        self.assertFalse(verify_source(self.spec,b"import os\ndef compute(a,b): return a+b"))
    def test_call(self):
        self.assertFalse(verify_source(self.spec,b"def compute(a,b): return sum([a,b])"))
    def test_defaults(self):
        self.assertFalse(verify_source(self.spec,b"def compute(a,b=1): return a+b"))
    def test_negative(self):
        self.assertTrue(verify_source({"parameters":["a"],"expression":-2},b"def compute(a): return -2"))
    def test_malformed(self):
        self.assertFalse(verify_source(self.spec,b"\xff"))
        self.assertFalse(verify_source({},b"def compute(a): return a"))
