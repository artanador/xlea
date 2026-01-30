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
    Read rows from a provider and optionally bind them to a schema.

    Parameters
    ----------
    provider : ProviderProto
        Data provider instance producing raw rows.
    schema : type, optional
        Schema class used to map rows into structured objects.

    Returns
    -------
    Iterable[Iterable]
        Raw rows if no schema is provided.
    Iterator[TSchema]
        Iterator of schema instances if a schema is provided.

    Notes
    -----
    When a schema is supplied, rows are buffered internally to allow
    header resolution before data iteration begins.
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
    """
    Automatically select a provider based on file extension and read data.

    Parameters
    ----------
    path : str | Path
        Path to the input file.
    sheet : str, optional
        Sheet name for multi-sheet formats (e.g. spreadsheets).
    schema : type, optional
        Schema class used to map rows into structured objects.

    Returns
    -------
    Iterable[Iterable]
        Raw rows if no schema is provided.
    Iterator[TSchema]
        Iterator of schema instances if a schema is provided.

    Raises
    ------
    UnknownFileExtensionError
        If no provider is registered for the given file extension.
    """

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
