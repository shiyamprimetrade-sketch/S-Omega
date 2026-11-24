import os
import tempfile
import unittest
from pathlib import Path
from workspace import read_artifact

SUPPORTED=hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd

class ContainmentTests(unittest.TestCase):
    def test_invalid_limits(self):
        for limit in (True,0,-1,1048577):
            with self.assertRaises(ValueError):
                read_artifact("unused","task",limit)
    @unittest.skipUnless(SUPPORTED,"descriptor traversal unavailable")
    def test_hardlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"task").mkdir()
            (root/"other").write_bytes(b"private")
            os.link(root/"other",root/"task"/"compute.py")
            with self.assertRaises(ValueError):
                read_artifact(root,"task")
    @unittest.skipUnless(SUPPORTED and hasattr(os,"mkfifo"),"FIFO unavailable")
    def test_fifo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"task").mkdir()
            os.mkfifo(root/"task"/"compute.py")
            with self.assertRaises(ValueError):
                read_artifact(root,"task")
    @unittest.skipUnless(SUPPORTED,"descriptor traversal unavailable")
    def test_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"task"/"compute.py").mkdir(parents=True)
            with self.assertRaises(ValueError):
                read_artifact(root,"task")
    @unittest.skipIf(SUPPORTED,"descriptor traversal supported")
    def test_unsupported(self):
        with self.assertRaises(NotImplementedError):
            read_artifact("unused","task")
