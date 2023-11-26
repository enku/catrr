# pylint: disable=missing-docstring
import datetime as dt
import os
from unittest import mock

from catrr import RoundRobin, Storage

from . import TestCase


class StorageTestCase(TestCase):
    @mock.patch("catrr.now")
    def test_can_save(self, now: mock.Mock) -> None:
        now.return_value = dt.datetime(2023, 11, 25, 7, 38, tzinfo=dt.UTC)
        storage = Storage(self.filename)
        rr = RoundRobin(["a", "b", "c"])
        next(iter(rr))
        storage.save(rr)

        with open(self.filename, "rb") as fp:
            content = fp.read()

        expected = b"""\
{
    "d33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8": {
        "current": 0,
        "items": [
            "a",
            "b",
            "c"
        ],
        "last_modified": "2023-11-25T07:38:00+00:00"
    }
}"""
        self.assertEqual(content, expected)

    def test_save_when_file_does_not_exist(self) -> None:
        os.unlink(self.filename)
        storage = Storage(self.filename)
        rr = RoundRobin(["a", "b", "c"])
        next(iter(rr))
        storage.save(rr)

        self.assertEqual(storage.load(["a", "b", "c"]), rr)

    @mock.patch("catrr.now")
    def test_can_load(self, now) -> None:
        now.return_value = dt.datetime(2023, 11, 25, 7, 38, tzinfo=dt.UTC)
        storage = Storage(self.filename)
        rr = RoundRobin(["a", "b", "c"])
        next(iter(rr))
        storage.save(rr)

        loaded_rr = storage.load(["a", "b", "c"])

        self.assertEqual(rr, loaded_rr)

    def test_load_when_does_not_exist(self) -> None:
        storage = Storage(self.filename)
        rr = RoundRobin(["a", "b", "c"])

        self.assertEqual(storage.load(["a", "b", "c"]), rr)
