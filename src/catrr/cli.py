"""catrr command-line interface"""
import argparse
import os
import sys
from typing import Sequence

import platformdirs

from catrr import StatefulRR

DEFAULT_STATE_FILE = os.path.join(platformdirs.user_data_dir(), "catrr.data")


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point"""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    path = next(iter(StatefulRR(args.items, args.state)))

    with open(path, "rb") as fp:
        sys.stdout.buffer.write(fp.read())


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        "-s",
        default=DEFAULT_STATE_FILE,
        help=f"State file (default: {DEFAULT_STATE_FILE})",
    )
    parser.add_argument("items", metavar="ITEM", nargs="+")

    return parser.parse_args(argv)
