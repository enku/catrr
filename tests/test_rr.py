"""Tests for the RoundRobin type"""
# pylint: disable=missing-docstring

from catrr import RoundRobin

from . import TestCase


class RoundRobinTestCase(TestCase):
    def test_can_iterate(self) -> None:
        rr = RoundRobin([1, 2, 3])
        irr = iter(rr)

        self.assertEqual(next(irr), 1)
        self.assertEqual(next(irr), 2)
        self.assertEqual(next(irr), 3)
        self.assertEqual(next(irr), 1)

    def test_repr(self) -> None:
        rr = RoundRobin([1, 2, 3])

        self.assertEqual(repr(rr), "RoundRobin([1, 2, 3])")

    def test_eq(self) -> None:
        rr1 = RoundRobin([1, 2, 3])
        rr2 = RoundRobin([1, 2, 3])
        rr2.current = 1
        rr3 = RoundRobin(["a", "b", "c"])
        rr4 = RoundRobin([1, 2, 3])

        self.assertEqual(rr1, rr1)
        self.assertEqual(rr1, rr4)
        self.assertNotEqual(rr1, rr2)
        self.assertNotEqual(rr1, rr3)
        self.assertNotEqual(rr1, None)
