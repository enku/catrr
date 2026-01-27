# pylint: disable=missing-docstring
import datetime as dt
import io
import json
from unittest import TestCase

import catrr

TIMESTAMP = dt.datetime(2023, 11, 25, 7, 38, tzinfo=dt.UTC)


class StorageTestCase(TestCase):
    def test_save(self) -> None:
        items = ["a", "b", "c"]
        string_io = catrr.save(io.StringIO("{}"), items, 0, TIMESTAMP)

        expected = {
            "d33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8": {
                "current": 0,
                "last_modified": "2023-11-25T07:38:00+00:00",
            }
        }
        self.assertEqual(json.load(string_io), expected)

    def test_load(self) -> None:
        items = ["a", "b", "c"]
        string_io = catrr.save(io.StringIO("{}"), items, 2, TIMESTAMP)

        current = catrr.load(string_io, ["a", "b", "c"])

        self.assertEqual(current, 2)

    def test_load_when_does_not_exist(self) -> None:
        items = ["a", "b", "c"]

        self.assertEqual(catrr.load(io.StringIO("{}"), items), -1)
