# pylint: disable=missing-docstring
import tempfile
from pathlib import Path
from unittest import TestCase

from catrr import cli


class MainTestCase(TestCase):
    def setUp(self) -> None:
        tmpdir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(tmpdir.cleanup)

        self.state_file = str(Path(tmpdir.name) / "state_file")
        self.output_file = str(Path(tmpdir.name) / "output_file")

    def test(self) -> None:
        tf = tempfile.NamedTemporaryFile
        with tf(buffering=0) as file1, tf(buffering=0) as file2:
            file1.write(b"foo\n")
            file2.write(b"bar\n")
            files = [file1.name, file2.name]

            cli.main(["-s", self.state_file, "-o", self.output_file, *files])
            self.assertEqual(Path(self.output_file).read_bytes(), b"foo\n")

            cli.main(["-s", self.state_file, "-o", self.output_file, *files])
            self.assertEqual(Path(self.output_file).read_bytes(), b"bar\n")
