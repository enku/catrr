# pylint: disable=missing-docstring
import datetime as dt
import io

import catrr

from . import TestCase


class StorageTestCase(TestCase):
    def test_save(self) -> None:
        timestamp = dt.datetime(2023, 11, 25, 7, 38, tzinfo=dt.UTC)
        items = ["a", "b", "c"]
        string_io = catrr.save(io.StringIO("{}"), items, 0, timestamp)

        expected = """\
{
    "d33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8": {
        "current": 0,
        "last_modified": "2023-11-25T07:38:00+00:00"
    }
}"""
        self.assertEqual(string_io.getvalue(), expected)

    def test_load(self) -> None:
        timestamp = dt.datetime(2023, 11, 25, 7, 38, tzinfo=dt.UTC)
        items = ["a", "b", "c"]
        string_io = catrr.save(io.StringIO("{}"), items, 2, timestamp)

        current = catrr.load(string_io, ["a", "b", "c"])

        self.assertEqual(current, 2)

    def test_load_when_does_not_exist(self) -> None:
        items = ["a", "b", "c"]

        self.assertEqual(catrr.load(io.StringIO("{}"), items), -1)
