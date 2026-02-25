import pytest

from contextlib import nullcontext as does_not_raise

from xlea.core.bound_schema import BoundSchema
from xlea.core.column import Column
from xlea.core.schema import Schema
from xlea.exc import HeaderNotFound


def test_resolve():
    class Person(Schema):
        name = Column("Name")
        email = Column("Email")

    rows = (("Name", "Email"), ("Alice", "a@example.com"))

    _ = BoundSchema(rows, Person).resolve()

    assert Person.name.index == 0
    assert Person.email.index == 1
