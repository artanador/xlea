import enum
from typing import Iterable, Union
from xlea.core.column import _Column
from xlea.exc import HeaderNotFound, MissingRequiredColumnError


def _flatten_pretendents(pretendents, carry_indices=(0,), delimiter=";"):
    last_not_none = {}

    out = []
    for p in pretendents:
        parts = []
        for i, v in enumerate(p):
            if str(v).casefold() in ("none", ""):
                if i in carry_indices and i in last_not_none:
                    v = last_not_none[i]
                else:
                    continue
            elif i in carry_indices:
                last_not_none[i] = v

            parts.append(str(v))

        out.append(delimiter.join(parts))
    return out


class BoundSchema:
    def __init__(self, rows: tuple[Iterable, ...], schema):
        self._rows = rows
        self._schema = schema
        self._data_row = -1
        self._config = getattr(schema, "__schema_config__", {})
        self._columns: dict[str, _Column] = {
            attr: col
            for attr, col in schema.__dict__.items()
            if isinstance(col, _Column)
        }

    def resolve(self):
        required = tuple(c for c in self._columns.values() if c._required)

        delimiter = self._config.get("delimiter", ";")
        header_rows = self._config.get("header_rows", 1)
        header = None
        for i, r in enumerate(self._rows):
            current_row = tuple(str(v) for v in r)
            pretendents = [current_row]
            if header_rows == 1:
                header = tuple(str(val) for val in current_row)
            else:
                for hr in range(1, header_rows):
                    if i + hr >= len(self._rows):
                        break
                    r_next = tuple(str(v) for v in self._rows[i + hr])
                    pretendents.append(r_next)
                header = _flatten_pretendents(
                    list(zip(*pretendents)),
                    delimiter=delimiter,
                )

            if self._is_header(required, header):
                self._data_row = i + header_rows
                break
            header = None

        if header is None:
            raise HeaderNotFound("Header not found")

        for col in self._columns.values():
            for idx, val in enumerate(header):
                if not col.matching(val):
                    continue
                col._set_index(idx)
                col._set_name(val)

            if col._required and col.index == -1:
                raise MissingRequiredColumnError(
                    f"Cant find required column '{col._pattern}'"
                )

        return self

    def _is_header(
        self,
        required: tuple[_Column, ...],
        row: Union[tuple[str, ...], list],
    ) -> bool:
        for val in row:
            if not any(c.matching(val) for c in required):
                return False

        return True
