from typing import Optional
from xlea.core.bound_schema import BoundSchema
from xlea.exc import InvalidRowError


def make_row_type(schema):
    class Row(schema, RowObject):
        pass

    return Row


class RowObject:
    def __init__(self, row, row_idx, schema: BoundSchema):
        valid, skip, col_index = self._validate(row, schema)
        if not valid and not skip:
            raise InvalidRowError(
                f"The value in row {row_idx} failed validation: {row[col_index]}"
            )
        if not valid:
            return
        self._row = row
        self._row_idx = row_idx
        self._schema = schema
        self._col_names = tuple(c.name for c in self._schema._columns.values())
        self._indeces_by_names = {
            c.name: c.index for c in self._schema._columns.values()
        }

    def _validate(self, row, schema: BoundSchema) -> tuple[bool, bool, Optional[int]]:
        for col in schema._columns.values():
            if col.index is None:
                continue
            valid = col.validate_value(row[col.index])
            if not valid:
                return False, col._skip_invalid_row, col.index
        return True, False, None

    def __contains__(self, key):
        return key in self._col_names

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self._col_names:
                return self._row[self._indeces_by_names[key]]
            raise KeyError(key)

        if isinstance(key, int):
            index = tuple(sorted(self._indeces_by_names.values()))[key]
            return self._row[index]

    def __dir__(self):
        return list(self._schema._columns.keys())

    def __len__(self):
        return len(self._schema._columns)

    def __eq__(self, other):
        if isinstance(other, RowObject):
            return self.asdict() == other.asdict()
        if isinstance(other, dict):
            return self.asdict() == other

        return False

    def __repr__(self):
        values = ", ".join(
            [
                f"{attr} ({col.name}): {None if col.index is None else self._row[col.index]}"
                for attr, col in self._schema._columns.items()
            ]
        )
        return f"{self._schema._schema.__name__}({values})"

    @property
    def row_index(self) -> int:
        return self._row_idx

    def asdict(self):
        return {name: getattr(self, name) for name in self._schema._columns.keys()}
