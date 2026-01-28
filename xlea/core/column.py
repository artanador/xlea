from typing import Any, Generic, Optional, TypeVar, Union, overload

T = TypeVar("T")


@overload
def Column(  # type: ignore[reportInconsistentOverload]
    name: str,
    ignore_case: bool = False,
    required: bool = True,
    default: Optional[T] = None,
) -> T: ...
def Column(
    name: str,
    ignore_case: bool = False,
    required: bool = True,
    default: Optional[T] = None,
) -> Any:
    return _Column(
        name=name, ignore_case=ignore_case, required=required, default=default
    )


class _Column(Generic[T]):
    """
    Column mapping descriptor.

    Describes how a value should be extracted from the header and converted
    from raw cell data.

    Parameters
    ----------
    name : str
        Column name or hierarchical path in the header.
    required : bool, default=True
        Whether the column must be present.
    default : Any, optional
        Default value if the column is missing or empty.
    ignore_case : bool, default=False
        Whether header matching should be case-insensitive.

    Notes
    -----
    Column paths may be hierarchical and are split using the schema delimiter (see ``@config``).

    Examples
    --------
    Simple column::

        age = Column("Age")

    Optional column with default::

        city = Column("City", required=False, default="Voronezh")

    Hierarchical header::

        fullname = Column("profile;fio", ignore_case=True)
    """

    def __init__(
        self,
        name: str,
        ignore_case: bool = False,
        required: bool = True,
        default: Optional[T] = None,
    ) -> Any:
        self._name = name
        self._default = default
        self._ignore_case = ignore_case
        self._required = required
        self._index = None
        self._attr_name = None
        self._type: Optional[T] = None

    def __set_name__(self, owner, name):
        self._attr_name = name
        self._type = owner.__annotations__.get(name)

    def __get__(self, instance, _):
        if instance is None:
            return self

        if self._index is None:
            return self._default

        value = instance._row[self._index]
        if self._type is not None:
            return self._type(value)

        return value

    def matching(self, value: str) -> bool:
        if self._ignore_case:
            return value.casefold() == self._name.casefold()
        return value == self._name

    @property
    def index(self) -> Union[int, None]:
        return self._index

    def _set_index(self, value: int):
        self._index = value
