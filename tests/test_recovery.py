import unittest
from recovery import receipt, verify_anchor

class RecoveryTests(unittest.TestCase):
    def test_valid(self):
        key = b"k"*32
        self.assertTrue(verify_anchor(2, {"x":2}, key, receipt(2, {"x":2}, key)))
    def test_rollback(self):
        key = b"k"*32
        with self.assertRaises(ValueError):
            verify_anchor(1, {"x":1}, key, receipt(2, {"x":2}, key))
    def test_mutation(self):
        key = b"k"*32
        with self.assertRaises(ValueError):
            verify_anchor(2, {"x":3}, key, receipt(2, {"x":2}, key))
