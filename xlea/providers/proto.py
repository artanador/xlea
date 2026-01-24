from typing import Protocol, Iterable


class ProviderProto(Protocol):
    def rows(self) -> Iterable[Iterable]: ...
