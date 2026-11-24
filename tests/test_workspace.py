import os
import tempfile
import unittest
from pathlib import Path
from workspace import read_artifact

class WorkspaceTests(unittest.TestCase):
    def test_traversal(self):
        with self.assertRaises(ValueError):
            read_artifact(".", "../escape")
    @unittest.skipUnless(hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd,"POSIX required")
    def test_read_and_limit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"task"
            p.mkdir()
            (p/"compute.py").write_bytes(b"abc")
            self.assertEqual(read_artifact(d,"task"),b"abc")
            with self.assertRaises(ValueError):
                read_artifact(d,"task",2)
    @unittest.skipUnless(hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd,"POSIX required")
    def test_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"task"
            p.mkdir()
            (Path(d)/"outside").write_bytes(b"secret")
            (p/"compute.py").symlink_to(Path(d)/"outside")
            with self.assertRaises(OSError):
                read_artifact(d,"task")
