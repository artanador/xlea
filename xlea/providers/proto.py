from typing import Protocol, Iterable


class ProviderProto(Protocol):
    """
    Data provider protocol.

    A provider is responsible for supplying raw tabular data as an iterable
    of rows. Each row itself must be an iterable of cell values.

    Implementations may read from Excel files, CSV, databases or any other
    source.

    Notes
    -----
    Providers should not perform schema-specific logic.

    Examples
    --------
    Minimal provider::

        class ListProvider:
            def rows(self):
                return [
                    ("ID", "Name"),
                    (1, "Alice"),
                    (2, "Bob"),
                ]

    Usage::

        persons = read(ListProvider(), schema=Person)
    """

    def __init__(*args, **kwargs): ...

    def rows(self) -> Iterable[Iterable]: ...
