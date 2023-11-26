"""catrr write files to stdout in round-robin fashion"""
import datetime as dt
import hashlib
import json
from typing import IO, Any, Iterator, Sequence, TypedDict

ENCODING = "UTF-8"
now = dt.datetime.now


class RoundRobin[T]:
    """Iterate over items in round-robin fashion

    Like itertools.cycle() except we store the value of the current item so it can be
    loaded and saved by Storage below.
    """

    def __init__(self, items: Sequence[T]) -> None:
        self.items = list(items)
        self.current = -1

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self.current < 0:
            self.current = 0
        else:
            self.current += 1
            if self.current >= len(self.items):
                self.current = 0

        return self.items[self.current]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.items!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False

        return self.items == other.items and self.current == other.current


class StorageValue(TypedDict):
    """The value stored in Storage (as JSON)"""

    current: int
    items: list[str]
    last_modified: str  # timestamp in ISO format


class Storage:
    """File-backed storage for RoundRobin instances"""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def save(self, rr: RoundRobin[str]) -> None:
        """Save the RoundRobin instance to storage

        A last_modified field is also stored.
        """
        data: dict[str, StorageValue]
        try:
            data = self.load_json()
        except FileNotFoundError:
            data = {}

        data[self.key(rr.items)] = self.value(rr, now(tz=dt.UTC))

        with open(self.filename, "w", encoding=ENCODING) as fp:
            json.dump(data, fp, indent=4)

    def load(self, items: Sequence[str]) -> RoundRobin[str]:
        """Load the given RoundRobin object from storage

        If the RoundRobin state doesn't exist in storage, a newly initialized one is
        returned.
        """
        data = self.load_json()
        if rr_data := data.get(self.key(items)):
            rr = RoundRobin(rr_data["items"])
            rr.current = rr_data["current"]
            return rr
        return RoundRobin(items)

    @staticmethod
    def key(items: Sequence[str]) -> str:
        """Given the items return the storage key"""
        return hashlib.sha256(json.dumps(list(items)).encode(ENCODING)).hexdigest()

    @staticmethod
    def value(rr: RoundRobin, timestamp: dt.datetime) -> StorageValue:
        """Given the RoundRobin instance return the values to store in JSON"""
        return {
            "current": rr.current,
            "items": rr.items,
            "last_modified": timestamp.isoformat(),
        }

    def load_json(self) -> dict[str, StorageValue]:
        """Load the storage JSON into a Python dict

        If the storage file doesn't yet exist, return an empty dict
        """
        with open(self.filename, "r", encoding=ENCODING) as fp:
            try:
                return json.load(fp)
            except json.JSONDecodeError:
                return {}


class StatefulRR:
    """Class that combines RoundRobin and Storage into a single unit"""

    def __init__(self, items: Sequence[str], state_file: str) -> None:
        self._iter: Iterator[str]
        self.storage = Storage(state_file)

        try:
            self.rr = self.storage.load(items)
        except FileNotFoundError:
            self.rr = RoundRobin(items)

    def __iter__(self) -> Iterator[str]:
        self._iter = iter(self.rr)

        return self

    def __next__(self) -> str:
        item = next(self._iter)

        self.storage.save(self.rr)

        return item
