from typing import Optional

import openpyxl

from xleb.providers.proto import ProviderProto
from xleb.exc import ProviderError


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
