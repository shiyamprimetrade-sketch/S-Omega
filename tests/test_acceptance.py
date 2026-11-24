import os
import unittest
from acceptance import run

@unittest.skipUnless(hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd,"POSIX required")
class AcceptanceTests(unittest.TestCase):
    def test_demo(self):
        results=run()
        self.assertEqual(len(results),8)
        self.assertTrue(all(results.values()))
