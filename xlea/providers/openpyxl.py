from typing import Optional

from xlea.exc import ProviderError

try:
    import openpyxl
except ImportError:
    raise ProviderError(
        "openpyxl not found, ensure that you installed it:\npip install openpyxl"
    )

from xlea.providers.proto import ProviderProto


class OpenPyXlProvider(ProviderProto):
    def __init__(self, path, sheet: Optional[str] = None):
        self._path = path
        self._sheet = sheet

    def rows(self):
        book = openpyxl.load_workbook(self._path, read_only=True)
        sheet = book.active if self._sheet is None else book[self._sheet]
        if sheet is None:
            raise ProviderError("Sheet not found")
        return sheet.values
