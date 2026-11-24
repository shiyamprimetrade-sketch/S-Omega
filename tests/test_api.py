import unittest
from api import verify_record, sign
from transactional import seal

class APITests(unittest.TestCase):
    def test_malformed(self):
        for value in (None, [], {}, {"record":None,"tag":"a"}, {"record":{"id":"a","status":"completed"},"tag":"é"}):
            with self.subTest(value=value):
                self.assertFalse(verify_record("a","completed",value,b"k"*32))
    def test_binding(self):
        evidence=seal({"id":"a","status":"completed"},b"k"*32)
        self.assertTrue(verify_record("a","completed",evidence,b"k"*32))
        self.assertFalse(verify_record("b","completed",evidence,b"k"*32))
        self.assertFalse(verify_record("a","failed",evidence,b"k"*32))
        self.assertFalse(verify_record("a","completed",evidence,b"short"))
