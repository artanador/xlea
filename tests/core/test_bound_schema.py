import pytest

from xlea.core.bound_schema import BoundSchema
from xlea.core.column import Column
from xlea.core.schema import Schema


def test_resolve():
    class Person(Schema):
        name = Column("Name")
        email = Column("Email")

    rows = iter((("Name", "Email"), ("Alice", "a@example.com")))

    resolved = BoundSchema(rows, Person).resolve()

    assert resolved._column_bindings["name"][1] == 0
    assert resolved._column_bindings["email"][1] == 1
