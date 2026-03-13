"""
Regression tests for the lazy HeaderNotFound bug.

Before the fix, `read()` and `autoread()` silently returned a generator
when a schema was provided, deferring `BoundSchema.resolve()` — and therefore
any `HeaderNotFound` / `MissingRequiredColumnError` — until the caller began
iterating. The fix must make schema resolution errors surface eagerly, at the
`read()` / `autoread()` call site.

See: https://github.com/artanador/xlea/issues/3
"""

import pytest

from xlea import Schema, Column, read
from xlea.exc import HeaderNotFound


class PersonSchema(Schema):
    """Minimal schema used across all test cases."""

    id: str = Column("ID")
    name: str = Column("Name")


class ListProvider:
    """In-memory provider that wraps a plain list of tuples."""

    def __init__(self, rows: list):
        self._rows = rows

    def rows(self):
        return iter(self._rows)


def test_read_raises_header_not_found_immediately_when_no_matching_header():
    """
    `read()` must raise `HeaderNotFound` at the call site, not during iteration,
    when the provider yields no row that matches the required schema columns.

    Arrange:
        A provider whose rows contain no header matching PersonSchema
        (columns "ID" and "Name" are absent).

    Act:
        Call `read()` with the schema — do NOT iterate.

    Assert:
        `HeaderNotFound` is raised before any iteration occurs.
    """
    provider = ListProvider(
        [
            ("Foo", "Bar"),
            ("1", "Alice"),
        ]
    )

    with pytest.raises(HeaderNotFound):
        read(provider, schema=PersonSchema)


def test_read_raises_header_not_found_immediately_when_rows_are_empty():
    """
    `read()` must raise `HeaderNotFound` eagerly when the provider yields
    no rows at all.

    Arrange:
        A provider that yields an empty sequence.

    Act / Assert:
        `HeaderNotFound` is raised at the `read()` call site.
    """
    provider = ListProvider([])

    with pytest.raises(HeaderNotFound):
        read(provider, schema=PersonSchema)
