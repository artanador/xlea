from typing import Iterable, Union

from xlea.core.column import _Column
from xlea.core.constants import DEFAULT_DELIMITER
from xlea.exc import HeaderNotFound, MissingRequiredColumnError


class BoundSchema:
    def __init__(self, rows: tuple[Iterable, ...], schema):
        self._rows = rows
        self._schema = schema
        self._data_row = -1

        self._config = getattr(schema, "__schema_config__", {})
        self._delimiter = self._config.get("delimiter", DEFAULT_DELIMITER)
        self._header_rows = self._config.get("header_rows", 1)

        self._columns: dict[str, _Column] = {
            attr: col
            for attr, col in schema.__dict__.items()
            if isinstance(col, _Column)
        }

    def _is_header(
        self,
        required: tuple[_Column, ...],
        row: Union[tuple[str, ...], list],
    ) -> bool:
        for c in required:
            if not any(c.matching(val) for val in row):
                return False

        return True

    def _bind_columns(self, header):
        for col in self._columns.values():
            for idx, val in enumerate(header):
                if not col.matching(val):
                    continue
                col.index = idx
                col.name = val

            if col._required and col.index == -1:
                raise MissingRequiredColumnError(
                    f"Cant find required column '{col._pattern}'"
                )

    def _flatten_candidates(
        self,
        candidates,
        carry_indices=(0,),
    ):
        last_not_none = {}

        out = []
        for p in candidates:
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

            out.append(self._delimiter.join(parts))
        return out

    def _build_header_candidatte(self, start: int):
        rows = []

        for offset in range(self._header_rows):
            idx = start + offset
            if idx >= len(self._rows):
                return None

            rows.append(tuple(str(v) for v in self._rows[idx]))

            if self._header_rows == 1:
                return rows[0]

        return self._flatten_candidates(tuple(zip(*rows)))

    def _find_header(self, required: tuple[_Column, ...]):
        for row_index in range(len(self._rows)):
            header = self._build_header_candidatte(
                start=row_index,
            )

            if header and self._is_header(required, header):
                return header, row_index + self._header_rows
        return None, None

    def _get_required_columns(self) -> tuple[_Column, ...]:
        return tuple(c for c in self._columns.values() if c._required)

    def resolve(self):
        header, header_index = self._find_header(self._get_required_columns())
        if header is None:
            raise HeaderNotFound("Header not found")

        self._bind_columns(header)
        self._data_row = header_index

        return self
