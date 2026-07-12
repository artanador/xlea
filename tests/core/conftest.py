import pytest

from xlea import Schema, Column


class PersonSchema(Schema):
    """Minimal schema used across all test cases."""

    id: str = Column("ID")
    name: str = Column("Name")


class MultiHeaderSchema(Schema):
    """Schema includes multy header in a single column."""

    id: str = Column(pattern=("id", "Num", "First"))
    name: str = Column(pattern="Name")


class ListProvider:
    """In-memory provider that wraps a plain list of tuples."""

    def __init__(self, rows: list):
        self._rows = rows

    def rows(self):
        return iter(self._rows)


@pytest.fixture
def person_schema():
    return PersonSchema


@pytest.fixture
def multi_header_schema():
    return MultiHeaderSchema


@pytest.fixture
def provider():
    return ListProvider
