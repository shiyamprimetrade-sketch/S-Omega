import unittest
from alpha_gateway import validate

class GatewayTests(unittest.TestCase):
    def test_knowledge(self):
        self.assertEqual(validate({"version":2,"id":"task_1","operation":"knowledge"}), ("task_1","knowledge"))
    def test_invalid_ids(self):
        for ident in ("../escape", "", "a"*65, "é", "a\n"):
            with self.subTest(ident=ident), self.assertRaises(ValueError):
                validate({"version":2,"id":ident,"operation":"knowledge"})
    def test_version(self):
        with self.assertRaises(ValueError):
            validate({"version":2.0,"id":"a","operation":"knowledge"})
    def test_missing_spec(self):
        with self.assertRaises(ValueError):
            validate({"version":2,"id":"a","operation":"synthesize"})
    def test_missing_candidate(self):
        with self.assertRaises(ValueError):
            validate({"version":2,"id":"a","operation":"repair","spec":{"parameters":[],"expression":"1"}})
