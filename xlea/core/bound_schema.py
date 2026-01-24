from xlea.core.column import Column
from xlea.exc import HeaderNotFound, RequiredColumnMissingError


class BoundSchema:
    def __init__(self, rows, schema):
        self._rows = rows
        self._schema = schema
        self._columns: dict[str, Column] = {}

        for attr in dir(schema):
            col = getattr(schema, attr)
            if not isinstance(col, Column):
                continue
            self._columns[attr] = col

    def resolve(self):
        required_set = {
            c._name.casefold() for c in self._columns.values() if c._required
        }

        header = None
        for i, r in enumerate(self._rows):
            r_set = set(str(v).casefold() for v in r)
            if required_set.issubset(r_set):
                header = r
                self._header_row = i
                break

        if header is None:
            raise HeaderNotFound("Header not found")

        for col in self._columns.values():
            for idx, val in enumerate(header):
                if val != col._name:
                    continue
                col._set_index(idx)

            if col._required and col.index == -1:
                raise RequiredColumnMissingError(
                    f"Cant find required column '{col._name}'"
                )

        return self
