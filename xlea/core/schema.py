from xlea.core.column import Column
from xlea.exc import HeaderNotFound, RequiredColumnMissingError


class Schema:
    def __init__(self, data, header_rows=1, delimiter=";"):
        self._data = data
        self._header_rows = header_rows
        self._delimiter = delimiter
        self._header_row = -1
        self.columns = {}

    def resolve(self):
        targets_set = set()
        required_set = set()
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, Column):
                self.columns[name] = field
                if field._required:
                    required_set.add(field._name)
                targets_set.add(field._name)

        header = None
        for i, r in enumerate(self._data):
            r_set = set(r)
            if targets_set.issubset(r_set) or required_set.issubset(r_set):
                header = r
                self._header_row = i
                break

        if header is None:
            raise HeaderNotFound("Header not found")

        for col in self.columns.values():
            for idx, val in enumerate(header):
                if val != col._name:
                    continue
                col._set_index(idx)
            if col._required and col.index == -1:
                raise RequiredColumnMissingError(
                    f"Cant find required column '{col._name}'"
                )
        return self.__class__

    def __repr__(self):
        repr_text = [f"{self.__class__.__name__}("]
        for _, field in self._schema.__dict__.items():
            if isinstance(field, Column):
                if field.index == -1:
                    repr_text.append(f"{field._name}: {None}")
                    repr_text.append(", ")
                else:
                    repr_text.append(f"{field._name}: {self._row[field.index]}")
                    repr_text.append(", ")
        if len(repr_text) > 1:
            repr_text.pop()

        repr_text.append(")")
        return "".join(repr_text)
