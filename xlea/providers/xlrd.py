from typing import Iterable, Optional

from xlea.exc import ProviderError
from xlea.providers.proto import ProviderProto


class XLRDProvider(ProviderProto):
    def __init__(self, path, sheet: Optional[str] = None):
        try:
            import xlrd
        except ImportError as e:
            raise ProviderError(
                "XLRDProvider requires 'xlrd'. Install it with: pip install xlea[xlrd]"
            ) from e

        self._xlrd = xlrd
        self._path = path
        self._sheet = sheet

    def rows(self) -> Iterable[Iterable]:
        book = self._xlrd.open_workbook(self._path, on_demand=True)
        if self._sheet:
            sheet = book.sheet_by_name(self._sheet)
        else:
            sheet = book.sheet_by_index(0)
        if sheet is None:
            raise ProviderError("Sheet not found")
        return (sheet._cell_values[i] for i in range(sheet.nrows))
