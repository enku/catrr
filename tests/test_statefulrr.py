"""Tests for the RoundRobin type"""
# pylint: disable=missing-docstring
import datetime as dt
import os
from pathlib import Path
from unittest import mock

from catrr import ENCODING, StatefulRR

from . import TestCase


class StatefulRRTestCase(TestCase):
    @mock.patch("catrr.now")
    def test(self, now: mock.Mock) -> None:
        now.return_value = dt.datetime(2023, 11, 26, 7, 38, tzinfo=dt.UTC)
        os.unlink(self.filename)
        stateful_rr = StatefulRR(["foo", "bar"], Path(self.filename))

        self.assertEqual(next(iter(stateful_rr)), "foo")
        expected = """\
{
    "96cd2da39a883a474f4818046d8ecbcf3df184bdd10ebb462060d2b77f304372": {
        "current": 0,
        "items": [
            "foo",
            "bar"
        ],
        "last_modified": "2023-11-26T07:38:00+00:00"
    }
}"""
        with open(self.filename, "r", encoding=ENCODING) as fp:
            self.assertEqual(fp.read(), expected)

        now.return_value = dt.datetime(2023, 11, 26, 7, 39, tzinfo=dt.UTC)
        self.assertEqual(next(iter(stateful_rr)), "bar")
        expected = """\
{
    "96cd2da39a883a474f4818046d8ecbcf3df184bdd10ebb462060d2b77f304372": {
        "current": 1,
        "items": [
            "foo",
            "bar"
        ],
        "last_modified": "2023-11-26T07:39:00+00:00"
    }
}"""
        with open(self.filename, "r", encoding=ENCODING) as fp:
            self.assertEqual(fp.read(), expected)
