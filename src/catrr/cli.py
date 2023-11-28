"""catrr command-line interface"""
import argparse
import datetime as dt
import sys
from pathlib import Path
from typing import Sequence

import platformdirs

import catrr

now = dt.datetime.now

DEFAULT_STATE_FILE = Path(platformdirs.user_state_dir()) / "catrr.data"


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point"""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    current = catrr.load(args.state, args.items)
    path, current = catrr.rr_next(args.items, current)
    sys.stdout.buffer.write(Path(path).read_bytes())
    catrr.save(args.state, args.items, current, now(tz=dt.UTC))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        "-s",
        type=Path,
        default=DEFAULT_STATE_FILE,
        help=f"State file (default: {DEFAULT_STATE_FILE})",
    )
    parser.add_argument("items", metavar="ITEM", nargs="+")

    return parser.parse_args(argv)
