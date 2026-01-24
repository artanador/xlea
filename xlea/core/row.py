from xlea.core.schema import Schema


class Row:
    def __init__(self, row, schema: type[Schema]):
        self._row = row
        self._schema = schema

    def asdict(self):
        return self._resolved

    def __getattr__(self, name):
        if name in self._resolved:
            return self._resolved[name]
        raise AttributeError(name)

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self._col_names:
                return self._resolved[self._col_names[key]]
            raise KeyError(key)

        if isinstance(key, int):
            return tuple(self._resolved.values())[key]

    def __contains__(self, key):
        return key in self._col_names.values()

    def __dir__(self):
        return list(self._resolved.keys())

    def __len__(self):
        return len(self._resolved)

    def __eq__(self, other):
        if isinstance(other, Row):
            return self.asdict() == other.asdict()
        if isinstance(other, dict):
            return self.asdict() == other

        return False
