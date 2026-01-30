from typing import Iterator, overload, Iterable, Type, Optional, Union
from pathlib import Path

from xlea.core.types import TSchema
from xlea.core.row import make_row_type
from xlea.core.bound_schema import BoundSchema
from xlea.providers.proto import ProviderProto
from xlea.providers import providers
from xlea.exc import UnknownFileExtensionError


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

    rows = provider.rows()

    if schema is None:
        return rows

    if not isinstance(rows, tuple):
        rows = tuple(rows)

    resolved_schema = BoundSchema(rows, schema).resolve()
    RowType = make_row_type(schema)

    for i, row in enumerate(rows[resolved_schema._data_row :]):
        row_object = RowType(row, i, resolved_schema)
        if not hasattr(row_object, "row_index"):
            continue
        yield row_object


@overload
def autoread(
    path: Union[str, Path],
    sheet: Optional[str] = None,
    *,
    schema: None = None,
) -> Iterable[Iterable]: ...
@overload
def autoread(
    path: Union[str, Path],
    sheet: Optional[str] = None,
    *,
    schema: Type[TSchema],
) -> Iterator[TSchema]: ...
def autoread(
    path: Union[str, Path],
    sheet: Optional[str] = None,
    *,
    schema: Optional[Type[TSchema]] = None,
) -> Union[Iterable[Iterable], Iterator[TSchema]]:
    if isinstance(path, str):
        path = Path(path)

    provider = providers.select_by_extension(path.suffix)
    if not provider:
        raise UnknownFileExtensionError(
            f"Cant find provider for extension {path.suffix}"
        )

    provider = provider(path, sheet)
    if schema is None:
        return read(provider)
    return read(provider, schema)


__all__ = ("read", "autoread")
