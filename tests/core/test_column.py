import re
import warnings
import pytest

from contextlib import nullcontext as does_not_raise

from xlea import Column
from xlea.exc import IncompatibleReturnValueTypeError


@pytest.mark.parametrize(
    "name, header, ignore_case, expectation",
    [
        ("Email", "Email", False, True),
        ("Email", "EMAIL", False, False),
        ("Email", "Email", True, True),
        ("Email", "EMAIL", True, True),
        ("Email", "name", False, False),
        ("Email", "name", True, False),
    ],
)
def test_string_matching(name, header, ignore_case, expectation):
    col = Column(name, ignore_case=ignore_case)

    assert col.matching(header) is expectation


@pytest.mark.parametrize(
    "name, header, expectation",
    [
        ("Email", "", does_not_raise()),
        ("Email", None, pytest.raises(AssertionError)),
        ("Email", 1, pytest.raises(AssertionError)),
        ("Email", [1, "Email"], pytest.raises(AssertionError)),
    ],
)
def test_non_string_header_matching(name, header, expectation):
    col = Column(name)

    with expectation:
        col.matching(header)


@pytest.mark.filterwarnings("ignore:When a Pattern")
@pytest.mark.parametrize(
    "pattern, header,ignore_case, expectation",
    [
        ("email", "Email", False, False),
        ("email", "Email", True, False),
        (re.compile(r"email", re.I), "Email", False, True),
        (re.compile(r"email", re.I), "Email", True, True),
    ],
)
def test_pattern_matching(pattern, header, ignore_case, expectation):
    col = Column(pattern, regexp=True, ignore_case=ignore_case)

    assert col.matching(header) is expectation


@pytest.mark.parametrize(
    "required, expectation",
    [
        (True, True),
        (False, False),
    ],
)
def test_required_flag(required, expectation):
    col = Column("Column", required=required)

    assert col._required is expectation


@pytest.mark.parametrize(
    "skip, expectation",
    [
        (True, True),
        (False, False),
    ],
)
def test_skip_invalid_row(skip, expectation):
    col = Column("Column", skip_invalid_row=skip)

    assert col._skip_invalid_row is expectation


@pytest.mark.parametrize(
    "default, expectation",
    [
        ("string", "string"),
        (1, 1),
        (True, True),
        (None, None),
    ],
)
def test_default_value(default, expectation):
    col = Column("Column", default=default)

    assert col._default == expectation


@pytest.mark.parametrize(
    "validator, expectation",
    [
        (bool, bool),
        (None, None),
    ],
)
def test_validator(validator, expectation):
    col = Column("Column", validator=validator)

    assert col._validator == expectation


@pytest.mark.parametrize(
    "validator, value, expectation",
    [
        (bool, 0, False),
        (bool, 1, True),
        (lambda n: n.startswith("Col"), "col", False),
        (lambda n: n.startswith("Col"), "Col", True),
        (lambda n: not n is None, None, False),
        (lambda n: not n is None, "None", True),
    ],
)
def test_validate_value(validator, value, expectation):
    col = Column("Column", validator=validator)

    assert col.validate_value(value) is expectation


@pytest.mark.parametrize(
    "validator, expectation",
    [
        (bool, does_not_raise()),
        (str, pytest.raises(IncompatibleReturnValueTypeError)),
        (int, pytest.raises(IncompatibleReturnValueTypeError)),
        (list, pytest.raises(IncompatibleReturnValueTypeError)),
    ],
)
def test_validator_incompatible_return_type(validator, expectation):
    col = Column("Column", validator=validator)

    with expectation:
        col.validate_value("0")
