import re
from re import Pattern
from sys import excepthook
import warnings
from typing import Any, Callable, Generic, Optional, TypeVar, Union, overload

T = TypeVar("T")


@overload
def Column(  # type: ignore[reportInconsistentOverload]
    pattern: Union[str, Pattern[str], Callable[[str], bool]],
    ignore_case: bool = False,
    required: bool = True,
    default: Optional[T] = None,
    regexp: bool = False,
    validator: Union[Callable[[str], bool], None] = None,
    skip_invalid_row=False,
) -> T: ...
def Column(
    pattern: Union[str, Pattern[str], Callable[[str], bool]],
    ignore_case: bool = False,
    required: bool = True,
    default: Optional[T] = None,
    regexp: bool = False,
    validator: Union[Callable[[str], bool], None] = None,
    skip_invalid_row=False,
) -> Any:
    """
    Declare a column mapping within a schema.

    ``Column`` is a descriptor that defines how a column is identified
    in the header, validated, converted, and exposed as an attribute
    on schema instances.

    Parameters
    ----------
    pattern : str | Pattern[str] | Callable[[str], bool]
        Header matching strategy:

        - ``str``: exact column name match
        - ``Pattern``: regular expression applied to header values
        - ``Callable``: custom predicate receiving a header cell value
          and returning ``True`` if it matches
    ignore_case : bool, default=False
        Whether string-based matching should be case-insensitive.
        Has no effect when ``pattern`` is a compiled regular expression.
    required : bool, default=True
        Whether the column must be present in the header.
    default : Any, optional
        Default value returned when the column is missing or unresolved.
    regexp : bool, default=False
        If ``True`` and ``pattern`` is a string, it is compiled into
        a regular expression.
    validator : Callable[[str], bool], optional
        Optional value-level validator. Called on the raw cell value
        before type conversion.
    skip_invalid_row : bool, default=False
        Whether rows with invalid values for this column should be skipped
        entirely during iteration.

    Returns
    -------
    Any
        A column descriptor bound to the owning schema class.

    Warnings
    --------
    UserWarning
        Raised when ``ignore_case`` is set while passing a compiled
        regular expression as ``pattern``. In this case, ``ignore_case``
        is ignored.

    Notes
    -----
    Type conversion is driven by the owning schema's type annotations.
    If an annotation is present, the raw value is converted using the
    annotated type.
    """

    if isinstance(pattern, str) and regexp:
        pattern = re.compile(pattern, flags=re.IGNORECASE if ignore_case else 0)
    if isinstance(pattern, Pattern) and ignore_case:
        warnings.warn(
            "When a Pattern object is passed to the 'pattern' argument, "
            "'ignore_case' has no effect. Its value is ignored. "
            "To hide this warning, set 'ignore_case' to False.",
            UserWarning,
            stacklevel=2,
        )
    return _Column(
        pattern=pattern,
        ignore_case=ignore_case,
        required=required,
        default=default,
        validator=validator,
        skip_invalid_row=skip_invalid_row,
    )


class _Column(Generic[T]):
    """
    Column mapping descriptor.

    Describes how a value should be extracted from the header and converted
    from raw cell data.

    Parameters
    ----------
    pattern: str | Pattern[str] | Callable[[str], bool]
        Column name (or pattern, or callable) or hierarchical path in the header.
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
        pattern: Union[str, Pattern[str], Callable[[str], bool]],
        ignore_case: bool = False,
        required: bool = True,
        default: Optional[T] = None,
        validator: Union[Callable[[str], bool], None] = None,
        skip_invalid_row=False,
    ) -> None:
        self._pattern = pattern
        self._ignore_case = ignore_case
        self._required = required
        self._default = default
        self._validator = validator
        self._skip_invalid_row = skip_invalid_row

        self._index = None
        self._name = None
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
            try:
                return self._type(value)
            except ValueError:
                raise TypeError(
                    f"invalid value {value!r} in row {self._index}: "
                    f"expected type {self._type.__name__}, got {type(value).__name__}"
                )

        return value

    def matching(self, value: str) -> bool:
        if self._ignore_case and isinstance(self._pattern, str):
            return value.casefold() == self._pattern.casefold()

        if isinstance(self._pattern, Pattern):
            return re.search(self._pattern, value) is not None

        if callable(self._pattern):
            return self._pattern(value)

        return value == self._pattern

    def validate_value(self, value: str) -> bool:
        if self._validator is None:
            return True

        return self._validator(value)

    @property
    def index(self) -> Union[int, None]:
        return self._index

    @property
    def name(self) -> Union[str, None]:
        return self._name

    @index.setter
    def index(self, value: int):
        self._index = value

    @name.setter
    def name(self, value: str):
        self._name = value
