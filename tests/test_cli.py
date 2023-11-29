# pylint: disable=missing-docstring
import os
import tempfile
from pathlib import Path

from catrr import cli

from . import TestCase


class MainTestCase(TestCase):
    def setUp(self) -> None:
        tmp = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with
        self.state_file = tmp.name
        os.unlink(tmp.name)
        self.addCleanup(tmp.close)

        tmp = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with
        self.output_file = tmp.name
        os.unlink(tmp.name)
        self.addCleanup(tmp.close)

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
