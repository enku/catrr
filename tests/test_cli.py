# pylint: disable=missing-docstring
import tempfile
from unittest import mock

from catrr import cli

from . import TestCase


class MainTestCase(TestCase):
    def setUp(self) -> None:
        tmp = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with
        self.state_file = tmp.name
        self.addCleanup(tmp.close)

    def test(self) -> None:
        tf = tempfile.NamedTemporaryFile
        with tf(buffering=0) as file1, tf(buffering=0) as file2:
            file1.write(b"foo\n")
            file2.write(b"bar\n")
            files = [file1.name, file2.name]

            with mock.patch("catrr.cli.sys.stdout") as stdout:
                cli.main(["-s", self.state_file, *files])
                cli.main(["-s", self.state_file, *files])

            self.assertEqual(
                stdout.buffer.write.call_args_list,
                [mock.call(b"foo\n"), mock.call(b"bar\n")],
            )
