from typing import Optional
from xlea.core.bound_schema import BoundSchema
from xlea.exc import InvalidRowError


def make_row_type(schema):
    class Row(schema, RowObject):
        pass

    return Row


class RowObject:
    def __init__(self, row, row_idx, schema: BoundSchema):
        self._schema = schema
        self._valid, skip, col_index = self._validate(row)

        if not self._valid and not skip:
            raise InvalidRowError(
                f"The value in row {row_idx} failed validation: {row[col_index]}"
            )

        if not self._valid:
            return

        self._row = row
        self._row_idx = row_idx
        self._col_names = frozenset(
            name for name, *_ in self._schema._column_bindings.values()
        )
        self._indeces_by_names = {
            name: idx for name, idx, _ in self._schema._column_bindings.values()
        }

    def _validate(self, row) -> tuple[bool, bool, Optional[int]]:
        for _, idx, col in self._schema._column_bindings.values():
            if idx is None:
                continue
            valid = col.validate_value(row[idx])
            if not valid:
                return False, col._skip_invalid_row, idx
        return True, False, None

    def __contains__(self, key):
        return key in self._col_names

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self._col_names:
                return self._row[self._indeces_by_names[key]]
            raise KeyError(key)

        if isinstance(key, int):
            indices = tuple(
                sorted(
                    idx for idx in self._indeces_by_names.values() if idx is not None
                )
            )
            if len(indices) > key:
                return self._row[indices[key]]
            raise IndexError(key)

        raise TypeError(key)

    def __dir__(self):
        return list(self._schema._columns_by_attr.keys())

    def __len__(self):
        return len(self._schema._columns_by_attr)

    def __eq__(self, other):
        if isinstance(other, RowObject):
            return self.asdict() == other.asdict()
        if isinstance(other, dict):
            return self.asdict() == other

        return False

    def __repr__(self):
        values = ", ".join(
            [
                f"{attr} ({name}): {None if idx is None else self._row[idx]}"
                for attr, (name, idx, _) in self._schema._column_bindings.items()
            ]
        )
        return f"{type(self).__name__}({values})"

    @property
    def row_index(self) -> int:
        return self._row_idx

    def asdict(self):
        return {
            name: getattr(self, name) for name in self._schema._columns_by_attr.keys()
        }
