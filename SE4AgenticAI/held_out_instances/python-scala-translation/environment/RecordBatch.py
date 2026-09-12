"""
RecordBatch module for grouping, deduplicating, and aggregating sale records.

This module demonstrates Python's flexible collection handling with:
- Mutable default arguments (Python anti-pattern) in `top_categories`
- Optional/Union-style return values for lookups that may fail
- functools.reduce for a running total
- itertools.groupby-style aggregation done manually with dict accumulation
- Deduplication that preserves first-seen order
"""

from dataclasses import dataclass, field
from functools import reduce
from typing import Optional


@dataclass(frozen=True)
class Record:
    """An immutable sale record."""

    id: str
    category: str
    amount: float
    tags: frozenset = field(default_factory=frozenset)


def dedupe_by_id(records: list[Record]) -> list[Record]:
    """Remove duplicate records by id, keeping the first occurrence."""
    seen: set[str] = set()
    result: list[Record] = []
    for r in records:
        if r.id not in seen:
            seen.add(r.id)
            result.append(r)
    return result


def group_by_category(records: list[Record]) -> dict[str, list[Record]]:
    """Group records by category, preserving insertion order within each group."""
    groups: dict[str, list[Record]] = {}
    for r in records:
        groups.setdefault(r.category, []).append(r)
    return groups


def category_totals(records: list[Record]) -> dict[str, float]:
    """Sum amounts per category."""
    totals: dict[str, float] = {}
    for r in records:
        totals[r.category] = totals.get(r.category, 0.0) + r.amount
    return totals


def top_categories(records: list[Record], n: int = 3, exclude: list[str] = []) -> list[tuple[str, float]]:
    """
    Return the top-n categories by total amount, excluding any category
    named in `exclude`. Ties are broken alphabetically by category name.

    NOTE: `exclude: list[str] = []` is Python's classic mutable-default-argument
    pitfall -- callers must never rely on mutating this default.
    """
    totals = category_totals(records)
    filtered = [(cat, total) for cat, total in totals.items() if cat not in exclude]
    filtered.sort(key=lambda pair: (-pair[1], pair[0]))
    return filtered[:n]


def find_by_id(records: list[Record], target_id: str) -> Optional[Record]:
    """Look up a record by id, returning None if not found."""
    for r in records:
        if r.id == target_id:
            return r
    return None


def overall_total(records: list[Record]) -> float:
    """Compute the overall total amount using a fold (functools.reduce)."""
    return reduce(lambda acc, r: acc + r.amount, records, 0.0)


def records_with_tag(records: list[Record], tag: str) -> list[Record]:
    """Return all records whose tag set contains `tag`."""
    return [r for r in records if tag in r.tags]
