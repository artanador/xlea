from typing import overload, Iterable, Type, Optional, Union

from xlea.core.types import TSchema
from xlea.core.row import Row
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

    resolved_schema = schema(rows).resolve()

    bound = []
    for r in rows:
        obj = Row(r, resolved_schema)
        obj.__class__ = resolved_schema
        bound.append(obj)
    return bound


__all__ = ("read",)
