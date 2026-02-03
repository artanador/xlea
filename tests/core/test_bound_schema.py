import pytest

from contextlib import nullcontext as does_not_raise

from xlea.core.bound_schema import BoundSchema
from xlea.core.column import Column
from xlea.core.schema import Schema
from xlea.exc import HeaderNotFoundError


@pytest.fixture
def PersonSchema():
    class Person(Schema):
        id: int = Column("ID")
        age: int = Column("Age")
        name: str = Column("Name", required=False)

    return Person


@pytest.mark.parametrize(
    "rows, expected",
    [
        (
            (("ID", "Age", "Column2"),),
            3,
        ),
        (
            (("ID", "Name", "Age"),),
            3,
        ),
    ],
)
def test_resolve_count(PersonSchema, rows, expected):
    schema = BoundSchema(rows, schema=PersonSchema).resolve()

    assert len(schema._columns) == expected


@pytest.mark.parametrize(
    "rows, expected",
    [
        (
            (("ID", "Age", "Column2"),),
            1,
        ),
        (
            (("",), ("ID", "Age", "Name")),
            2,
        ),
        (
            ((None,), ("",), ("ID", "Age", "Name")),
            3,
        ),
        (
            (tuple(), ("",), ("ID", "Age", "Name")),
            3,
        ),
    ],
)
def test_data_row(PersonSchema, rows, expected):
    schema = BoundSchema(rows, schema=PersonSchema).resolve()

    assert schema._data_row == expected


@pytest.mark.parametrize(
    "rows",
    [
        (("ID", "Age", "Column2"),),
        (("",), ("ID", "Age", "Name")),
        ((None,), ("",), ("ID", "Age", "Name")),
        (tuple(), ("",), ("ID", "Age", "Name")),
    ],
)
def test_required_columns(PersonSchema, rows):
    schema = BoundSchema(rows, schema=PersonSchema).resolve()

    assert len(schema._get_required_columns()) == 2
    assert schema._get_required_columns()[0]._name == "ID"
    assert schema._get_required_columns()[1]._name == "Age"


@pytest.mark.parametrize(
    "rows, expectation",
    [
        ((("ID", "Age", "Name"),), True),
        ((("ID", "Age"),), True),
        ((("ID", "Column2", "Age"),), True),
        ((("ID", "Column2", "Name", "Age"),), True),
        ((("", "Age", "Column2", "ID"),), True),
        ((("",),), False),
        ((("Nome", 1),), False),
        ((("id", "name"),), False),
    ],
)
def test_is_header(PersonSchema, rows, expectation):
    schema = BoundSchema(rows, schema=PersonSchema)
    required = schema._get_required_columns()

    assert schema._is_header(required, rows[0]) is expectation


@pytest.mark.parametrize(
    "rows, expectation",
    [
        (
            (("ID", "Age", "Name"),),
            does_not_raise(),
        ),
        (
            (("ID", "Age"),),
            does_not_raise(),
        ),
        (
            (("id", "Name"),),
            pytest.raises(HeaderNotFoundError),
        ),
        (
            (("id", "Age", "Name"),),
            pytest.raises(HeaderNotFoundError),
        ),
    ],
)
def test_incorrect_header(PersonSchema, rows, expectation):
    with expectation:
        BoundSchema(rows, schema=PersonSchema).resolve()
