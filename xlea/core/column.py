class Column:
    def __init__(self, name: str, ignore_case: bool = False, required: bool = True):
        self._name = name
        self._ignore_case = ignore_case
        self._required = required
        self._index = -1

    def __get__(self, instance, _):
        if instance is None:
            return self
        return instance._row[self._index]

    @property
    def index(self) -> int:
        return self._index

    def _set_index(self, value: int):
        self._index = value
