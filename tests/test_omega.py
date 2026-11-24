import unittest
from omega import proof, verify, authorize, checkpoint, restore

class OmegaTests(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(proof({"a":1,"b":2}), proof({"b":2,"a":1}))
    def test_tamper(self):
        self.assertFalse(verify({"a":2}, proof({"a":1})))
    def test_deny(self):
        self.assertFalse(authorize("read"))
        self.assertFalse(authorize("execute", ("execute",)))
        self.assertTrue(authorize("read", ("read",)))
    def test_restore(self):
        self.assertEqual(restore(checkpoint({"step":1})), {"step":1})
    def test_checkpoint_tamper(self):
        entry = checkpoint({"step":1})
        entry["record"]["state"]["step"] = 2
        with self.assertRaises(ValueError):
            restore(entry)

if __name__ == "__main__":
    unittest.main()
