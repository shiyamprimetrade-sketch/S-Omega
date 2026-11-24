import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from journal import Journal

class JournalTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db = str(Path(tmp.name)/"journal.db")
        self.j = Journal(self.db)
    def test_completion(self):
        self.j.begin("a")
        self.j.finish("a","completed",{"ok":True})
        self.assertEqual(self.j.get("a"),("completed",{"ok":True}))
        with self.assertRaises(ValueError):
            self.j.finish("a","failed",{})
    def test_restart(self):
        self.j.begin("a")
        j = Journal(self.db)
        self.assertEqual(j.pending(),["a"])
        j.finish("a","interrupted",{})
        self.assertEqual(j.pending(),[])
    def test_serialization_failure(self):
        self.j.begin("a")
        with self.assertRaises(TypeError):
            self.j.finish("a","completed",object())
        self.assertEqual(self.j.get("a"),("running",None))
    def test_concurrent_claim(self):
        def claim(_):
            try:
                self.j.begin("a")
                return True
            except sqlite3.IntegrityError:
                return False
        with ThreadPoolExecutor(max_workers=4) as pool:
            self.assertEqual(sum(pool.map(claim,range(8))),1)
