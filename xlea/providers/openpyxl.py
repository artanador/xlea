from typing import Iterable, Optional

from xlea.exc import ProviderError
from xlea.providers.proto import ProviderProto


class OpenPyXlProvider(ProviderProto):
    def __init__(self, path, sheet: Optional[str] = None):
        try:
            import openpyxl
        except ImportError as e:
            raise ProviderError(
                "OpenPyXlProvider requires 'openpyxl'. Install it with: pip install xlea[openpyxl]"
            ) from e

        self._openpyxl = openpyxl
        self._path = path
        self._sheet = sheet

    def rows(self) -> Iterable[Iterable]:
        book = self._openpyxl.load_workbook(self._path, read_only=True)
        sheet = book.active if self._sheet is None else book[self._sheet]
        if sheet is None:
            raise ProviderError("Sheet not found")
        return sheet.values
