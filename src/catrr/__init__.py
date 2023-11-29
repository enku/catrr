"""catrr write files to stdout in round-robin fashion"""
import datetime as dt
import hashlib
import io
import json
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
    string_io: io.StringIO, items: Sequence[str], current: int, timestamp: dt.datetime
) -> io.StringIO:
    """Save the items state to storage

    A last_modified field is also stored.
    """
    data = load_json(string_io)
    new_data = {**data, **{key(items): value(current, timestamp)}}

    return io.StringIO(json.dumps(new_data, indent=4))


def load(string_io: io.StringIO, items: Sequence[str]) -> int:
    """Load the items state from storage

    If the item state is not in storage, return -1
    """
    data = load_json(string_io)

    if record := data.get(key(items)):
        return record["current"]
    return -1


def key(items: Sequence[str]) -> str:
    """Given the items return the storage key"""
    return hashlib.sha256(json.dumps(list(items)).encode(ENCODING)).hexdigest()


def value(current: int, timestamp: dt.datetime) -> StorageValue:
    """Given the RoundRobin instance return the values to store in JSON"""
    return {"current": current, "last_modified": timestamp.isoformat()}


def load_json(string_io: io.StringIO) -> dict[str, StorageValue]:
    """Load the storage JSON into a Python dict"""
    return cast(dict[str, StorageValue], json.loads(string_io.getvalue()))
