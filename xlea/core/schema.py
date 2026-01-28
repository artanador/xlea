from xlea.core.row import RowObject


def config(header_rows: int = 1, delimiter: str = ";", **options):
    """
    Configure schema-level parsing behavior.

    This decorator attaches parsing configuration to a ``Schema`` subclass.
    Configuration affects how headers are interpreted, how column paths are
    resolved and how raw rows are processed before mapping.

    Parameters
    ----------
    header_rows : int, default=1
        Number of rows used to build the header.
    delimiter : str, default=";"
        Delimiter used to split hierarchical column paths.
    **options
        Reserved for future extensions.

    Returns
    -------
    Callable[[type[Schema]], type[Schema]]
        Decorated schema class.

    Notes
    -----
    Configuration is inherited by subclasses unless overridden.

    Examples
    --------
    Multi-level headers::

        @config(header_rows=2, delimiter=";")
        class Person(Schema):
            fullname = Column("profile;fio")

    Default configuration::

        class Product(Schema):
            id = Column("ID")
    """

    def decorator(schema):
        options.update(
            {
                "header_rows": header_rows,
                "delimiter": delimiter,
            }
        )
        setattr(schema, "__schema_config__", options)
        return schema

    return decorator


class Schema(RowObject):
    """
    Base class for row-to-object mapping.

    A schema defines how a single row of tabular data is converted into a
    Python object. Each ``Column`` declared on the class corresponds to a
    field in the resulting instance.

    Notes
    -----
    - Schema instances are representations of a single row.
    - Values are accessible both as attributes and via ``asdict()``.

    Examples
    --------
    Defining a schema::

        class Person(Schema):
            id = Column("ID")
            name = Column("Name")

    Accessing data::

        person = persons[0]
        print(person.name)
        print(person.asdict())
    """

    __schema_config__: dict = {}
