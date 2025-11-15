"""Tests for the RoundRobin type"""

# pylint: disable=missing-docstring

from unittest import TestCase

from catrr import rr_next


class RoundRobinTestCase(TestCase):
    def test_can_iterate(self) -> None:
        items = [1, 2, 3]

        self.assertEqual(rr_next(items, -1), (1, 0))
        self.assertEqual(rr_next(items, 0), (2, 1))
        self.assertEqual(rr_next(items, 1), (3, 2))
        self.assertEqual(rr_next(items, 2), (1, 0))
