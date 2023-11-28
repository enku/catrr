"""catrr write files to stdout in round-robin fashion"""
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import IO, Any, Iterator, Sequence, TypedDict, cast

ENCODING = "UTF-8"


class StorageValue(TypedDict):
    """The value stored in Storage (as JSON)"""

    current: int
    last_modified: str  # timestamp in ISO format


def rr_next[T](items: Sequence[T], current: int) -> tuple[T, int]:
    """Given the sequence of items and the current index, return the next item and it's index

    The next index is calculated in round-robin fashion. That is when we reach the end
    of the sequence, return 0.
    If current is less than 0, return 0.
    """
    if current < 0:
        current = 0
    else:
        current += 1
        if current >= len(items):
            current = 0

    return (items[current], current)


def save(
    path: Path, items: Sequence[str], current: int, timestamp: dt.datetime
) -> None:
    """Save the items state to storage

    A last_modified field is also stored.
    """
    data: dict[str, StorageValue] = load_json(path) or {}
    new_data = {**data, **{key(items): value(current, timestamp)}}
    path.write_text(json.dumps(new_data, indent=4), encoding=ENCODING)


def load(path: Path, items: Sequence[str]) -> int:
    """Load the items state from storage

    If the item state is not in storage, return -1
    """
    data = load_json(path) or {}

    if record := data.get(key(items)):
        return record["current"]
    return -1


def key(items: Sequence[str]) -> str:
    """Given the items return the storage key"""
    return hashlib.sha256(json.dumps(list(items)).encode(ENCODING)).hexdigest()


def value(current: int, timestamp: dt.datetime) -> StorageValue:
    """Given the RoundRobin instance return the values to store in JSON"""
    return {"current": current, "last_modified": timestamp.isoformat()}


def load_json(path: Path) -> dict[str, StorageValue] | None:
    """Load the storage JSON into a Python dict

    If the storage file doesn't yet exist, return an empty dict
    """
    try:
        data = path.read_text(encoding=ENCODING)
    except FileNotFoundError:
        return None
    return cast(dict[str, StorageValue], json.loads(data))
