from typing import Iterator, overload, Iterable, Type, Optional, Union

from xlea.core.types import TSchema
from xlea.core.row import make_row_type
from xlea.core.bound_schema import BoundSchema
from xlea.providers.proto import ProviderProto


@overload
def read(
    provider: ProviderProto,
) -> Iterable[Iterable]: ...
@overload
def read(
    provider: ProviderProto,
    schema: Type[TSchema],
) -> Iterator[TSchema]: ...
def read(
    provider: ProviderProto,
    schema: Optional[Type[TSchema]] = None,
) -> Union[Iterable[Iterable], Iterator[TSchema]]:
    """
    Read tabular data from a provider and map rows to schema instances.

    The function consumes an arbitrary data provider and converts each
    data row into an instance of the given `Schema` subclass.
    Column mapping, header resolution and value normalization are
    fully driven by schema configuration.

    Parameters
    ----------
    provider : ProviderProto
        Data source provider. Must implement the ``ProviderProto`` protocol
        and yield rows as iterables of cell values.
    schema : type[Schema]
        Schema class describing how columns should be extracted and mapped.

    Returns
    -------
    list[schema]
        A list of schema instances, one per data row.

    Raises
    ------
    ProviderError
        If provider fails to read data.
    HeaderNotFound
        If header not found.
    MissingRequireColumnError
        If required columns are missing or values cannot be parsed.

    Notes
    -----
    - Header rows are determined by the schema configuration (see ``@config``).
    - Column names may be hierarchical (e.g. ``"profile;name"``).

    Examples
    --------
    Basic usage with an ``OpenPyXlProvider`` provider::

        from xlea import read, Schema, Column
        from xlea.providers.openpyxl import OpenPyXlProvider

        class Person(Schema):
            id = Column("ID")
            name = Column("Name")
            age = Column("Age")

        persons = read(
            OpenPyXlProvider("people.xlsx"),
            schema=Person
        )

        for person in persons:
            print(person.name, person.age)

    Using schema configuration and defaults::

        @config(header_rows=2)
        class Person(Schema):
            city = Column("City", required=False, default="Moscow")

        persons = read(provider, schema=Person)
    """

    rows = tuple(provider.rows())

    if schema is None:
        return rows

    resolved_schema = BoundSchema(rows, schema).resolve()
    RowType = make_row_type(schema)

    for i, row in enumerate(rows[resolved_schema._data_row :]):
        yield RowType(row, i, resolved_schema)


__all__ = ("read",)
