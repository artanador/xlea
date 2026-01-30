from typing import Optional

from xlea.exc import ProviderError

try:
    import xlrd
except ImportError:
    raise ProviderError(
        "xlrd not found, ensure that you installed it:\npip install xlrd"
    )

from xlea.providers.proto import ProviderProto


class XLRDProvider(ProviderProto):
    def __init__(self, path, sheet: Optional[str] = None):
        self._path = path
        self._sheet = sheet

    def rows(self):
        book = xlrd.open_workbook(self._path, on_demand=True)
        if self._sheet:
            sheet = book.sheet_by_name(self._sheet)
        else:
            sheet = book.sheet_by_index(0)
        if sheet is None:
            raise ProviderError("Sheet not found")
        return (sheet._cell_values[i] for i in range(sheet.nrows))
