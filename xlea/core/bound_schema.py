from typing import Iterable, Iterator, Union

from xlea.core.column import _Column
from xlea.core.constants import DEFAULT_DELIMITER
from xlea.exc import HeaderNotFound, MissingRequiredColumns


class BoundSchema:
    def __init__(self, rows: Iterator[Iterable], schema):
        self._rows = rows
        self._schema = schema
        self._data_row = -1

        self._config = getattr(schema, "__schema_config__", {})
        self._delimiter = self._config.get("delimiter", DEFAULT_DELIMITER)
        self._header_rows = self._config.get("header_rows", 1)

        self._column_bindings: dict[str, tuple[str, Union[int, None], _Column]] = {}
        self._columns_by_attr: dict[str, _Column] = {
            attr: col
            for attr, col in schema.__dict__.items()
            if isinstance(col, _Column)
        }

    def _bind_columns(self, header):
        for attr, col in self._columns_by_attr.items():
            for idx, val in enumerate(header):
                if not col.matching(str(val)):
                    continue
                self._column_bindings[attr] = (str(val), idx, col)
                break

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

    def _build_header_candidatte(self, row):
        rows = [tuple(str(v) for v in row)]

        for _ in range(self._header_rows - 1):
            row = next(self._rows)

            rows.append(tuple(str(v) for v in row))

            if self._header_rows == 1:
                return rows[0]

        return self._flatten_candidates(tuple(zip(*rows)))

    def _is_header(
        self,
        required: tuple[_Column, ...],
        row: Union[tuple[str, ...], list],
    ) -> bool:
        for c in required:
            if not any(c.matching(str(val)) for val in row):
                return False

        return True

    def _find_header(self, required: tuple[_Column, ...]):
        best_missing = None
        for row_index, row in enumerate(self._rows):
            header = self._build_header_candidatte(row)
            if not header:
                continue

            if self._is_header(required, header):
                return header, row_index + self._header_rows

            found = {c for c in required if any(c.matching(str(val)) for val in header)}
            if best_missing is None or len(found) > len(best_missing[0]):
                missing = [c for c in required if c not in found]
                best_missing = (found, missing)

        if best_missing:
            missing_names = ",".join(str(c._pattern) for c in best_missing[1])
            raise MissingRequiredColumns(f"Missing columns: {missing_names}")
        raise HeaderNotFound("Header not found")

    def _get_required_columns(self) -> tuple[_Column, ...]:
        return tuple(c for c in self._columns_by_attr.values() if c._required)

    def resolve(self):
        header, header_index = self._find_header(self._get_required_columns())

        self._bind_columns(header)
        self._data_row = header_index

        return self
