from typing import overload, Iterable, Type, Optional, Union

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
) -> list[TSchema]: ...
def read(
    provider: ProviderProto,
    schema: Optional[Type[TSchema]] = None,
) -> Union[Iterable[Iterable], list[TSchema]]:
    rows = provider.rows()

    if schema is None:
        return rows

    resolved_schema = BoundSchema(rows, schema).resolve()
    RowType = make_row_type(schema)

    bound = []
    for r in rows:
        bound.append(RowType(r, resolved_schema))

    return bound


__all__ = ("read",)
