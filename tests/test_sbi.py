import json
import unittest
from sbi import parse,translate

class SBITests(unittest.TestCase):
    def setUp(self):
        self.obj={"schema_version":"1.0","operation_id":"demo","capability":"workspace.synthesize","deadline_ms":1000,"payload":{"spec":{"parameters":["a"],"expression":"a"}}}
    def read(self):
        return parse(json.dumps(self.obj).encode())
    def test_valid(self):
        self.assertEqual(translate(self.read())["operation"],"synthesize")
    def test_extra(self):
        self.obj["extra"]=1
        with self.assertRaises(ValueError): self.read()
    def test_deadline(self):
        for v in (True,0,300001):
            self.obj["deadline_ms"]=v
            with self.assertRaises(ValueError): self.read()
    def test_duplicate(self):
        with self.assertRaises(ValueError): parse(b'{"a":1,"a":2}')
    def test_size(self):
        with self.assertRaises(ValueError): parse(b" "*65537)
    def test_unsupported(self):
        self.obj["capability"]="network"
        with self.assertRaises(ValueError): translate(self.read())
    def test_alpha_id_limit(self):
        self.obj["operation_id"]="a"*65
        with self.assertRaises(ValueError): translate(self.read())
    def test_payload_override(self):
        self.obj["payload"]["id"]="other"
        with self.assertRaises(ValueError): translate(self.read())
