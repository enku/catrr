#!/usr/bin/env python
"""Run tests for catrr"""

import unittest


def main() -> None:
    """Program entry point"""
    loader = unittest.TestLoader()
    suite = loader.discover(".")
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == "__main__":
    main()
