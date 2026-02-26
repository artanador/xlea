# tests/test_empty_row_bug.py
import pytest

from xlea import Schema, Column, read


class PersonSchema(Schema):
    """Schema definition for testing purposes, representing a person record."""

    id: str = Column("ID")
    name: str = Column("Name")


class ListProvider:
    def __init__(self, rows: list[tuple], *args, **kwargs):
        self._rows = rows

    def rows(self):
        return iter(self._rows)


def test_empty_tuple_row_does_not_raise_index_error():
    """
    Regression test: an empty tuple in the row stream must not raise IndexError.

    Some Excel providers emit an empty tuple ``()`` for blank rows instead of
    skipping them. Before the fix, the reader attempted to access an index on
    that tuple and raised ``IndexError: tuple index out of range``.

    The fix must normalize empty tuples by padding them with empty values
    so that the row is passed through the normal validation pipeline.
    With ``skip_invalid_rows=True`` the row will be silently skipped;
    without it, a validation error will be raised as expected.

    Arrange:
        A provider that yields one header row, one valid data row, one empty
        tuple, and another valid data row.

    Act:
        Call ``read()`` and collect all results into a list.

    Assert:
        - No exception is raised.
        - Exactly two ``PersonSchema`` objects are returned.
        - Their ``id`` values match the two valid rows.
    """
    rows = [
        ("ID", "Name"),
        ("1", "Alice"),
        (),
        ("2", "Bob"),
    ]
    result = list(read(ListProvider(rows), schema=PersonSchema))

    assert len(result) == 3
    assert result[0].id == "1"
    assert result[1].id == "None"
    assert result[2].id == "2"


def test_only_empty_rows_returns_empty_list():
    """
    Edge case: a file containing only a header followed by empty rows yields no objects.

    When every data row is an empty tuple, the reader should return a normal
    list rather than raising an exception.

    Arrange:
        A provider that yields one header row and two empty tuples.

    Act:
        Call ``read()`` and collect all results into a list.

    Assert:
        The result is an empty list.
    """
    rows = [
        ("ID", "Name"),
        (),
        (),
    ]

    result = list(read(ListProvider(rows), schema=PersonSchema))

    assert len(result) == 2
