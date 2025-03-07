"""catrr command-line interface"""

import argparse
import datetime as dt
import io
import sys
from functools import partial
from pathlib import Path
from typing import Sequence

import platformdirs
from filelock import FileLock

import catrr

now = partial(dt.datetime.now, tz=dt.UTC)

DEFAULT_STATE_FILE = Path(platformdirs.user_state_dir()) / "catrr.data"


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point"""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    state: Path = args.state
    items: list[str] = args.items
    with FileLock(f"{state}.lock"):
        try:
            string_io = io.StringIO(state.read_text(encoding=catrr.ENCODING))
        except FileNotFoundError:
            string_io = io.StringIO("{}")
        path, current = catrr.rr_next(items, catrr.load(string_io, items))

        output = Path(path).read_bytes()
        if str(args.output) == "-":  # not a Path, but stdout
            sys.stdout.buffer.write(output)
        else:
            args.output.write_bytes(output)

        state.write_text(
            catrr.save(string_io, items, current, now()).getvalue(),
            encoding=catrr.ENCODING,
        )


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
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("-"),
        help="Output file (default: stdout)",
    )
    parser.add_argument("items", metavar="ITEM", nargs="+")

    return parser.parse_args(argv)
