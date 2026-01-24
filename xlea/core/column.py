class Column:
    def __init__(
        self,
        name: str,
        default=None,
        ignore_case: bool = False,
        required: bool = True,
    ):
        self._name = name
        self._default = default
        self._ignore_case = ignore_case
        self._required = required
        self._index = None

    def __get__(self, instance, _):
        if instance is None:
            return self
        if self._index is None:
            return self._default
        return instance._row[self._index]

    def matching(self, value: str) -> bool:
        if self._ignore_case:
            return value.casefold() == self._name.casefold()
        return value == self._name

    @property
    def index(self) -> int:
        return self._index

    def _set_index(self, value: int):
        self._index = value
