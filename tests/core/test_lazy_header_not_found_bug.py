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

import xlea
from xlea.exc import HeaderNotFound


def test_read_raises_header_not_found_immediately_when_no_matching_header(
    provider, person_schema
):
    """
    `read()` must raise `HeaderNotFound` at the call site, not during iteration,
    when the provider yields no row that matches the required schema columns.

    Arrange:
        A provider whose rows contain no header matching person_schema
        (columns "ID" and "Name" are absent).

    Act:
        Call `read()` with the schema — do NOT iterate.

    Assert:
        `HeaderNotFound` is raised before any iteration occurs.
    """
    provider = provider(
        [
            ("Foo", "Bar"),
            ("1", "Alice"),
        ]
    )

    with pytest.raises(HeaderNotFound):
        xlea.read(provider, schema=person_schema)


def test_read_raises_header_not_found_immediately_when_rows_are_empty(
    provider, person_schema
):
    """
    `read()` must raise `HeaderNotFound` eagerly when the provider yields
    no rows at all.

    Arrange:
        A provider that yields an empty sequence.

    Act / Assert:
        `HeaderNotFound` is raised at the `read()` call site.
    """
    provider = provider([])

    with pytest.raises(HeaderNotFound):
        xlea.read(provider, schema=person_schema)
