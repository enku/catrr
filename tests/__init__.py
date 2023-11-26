"""catrr tests"""
import tempfile
import unittest


class TestCase(unittest.TestCase):
    """base test case"""

    def setUp(self):
        super().setUp()

        self.tempfile = (
            tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with
        )
        self.filename = self.tempfile.name
        self.addCleanup(self.tempfile.close)
