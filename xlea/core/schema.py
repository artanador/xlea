from xlea.core.row import RowObject
from xlea.core.constants import DEFAULT_DELIMITER


def config(header_rows: int = 1, delimiter: str = DEFAULT_DELIMITER, **options):
    """
    Configure a schema class with file-level parsing options.

    This decorator attaches configuration metadata to a schema class.
    The configuration is later consumed by the schema binding and parsing
    machinery to control how input data is interpreted.

    Parameters
    ----------
    header_rows : int, default=1
        Number of header rows at the beginning of the file. These rows
        are used for column resolution and are not treated as data rows.
    delimiter : str, default=DEFAULT_DELIMITER
        Field delimiter used by the underlying provider.
    **options
        Arbitrary additional configuration options. All keyword arguments
        are stored verbatim and made available to the schema resolver.

    Returns
    -------
    Callable[[type], type]
        A class decorator that mutates the target schema class in-place
        by attaching the ``__schema_config__`` attribute.

    Notes
    -----
    Configuration is stored on the schema class itself and is inherited
    by subclasses unless explicitly overridden.
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
    Base class for declarative row schemas.

    A schema defines how a raw row produced by a provider should be mapped
    to a structured Python object. Subclasses typically declare ``Column``
    descriptors and type annotations to describe expected columns and
    their target types.

    Attributes
    ----------
    __schema_config__ : dict
        Schema-level configuration populated by the ``@config`` decorator.
        Used internally during schema resolution.
    """

    __schema_config__: dict = {}
