from typing import Optional

from xlea.exc import ProviderError

try:
    import pyxlsb
except ImportError:
    raise ProviderError(
        "pyxlsb not found, ensure that you installed it:\npip install pyxlsb"
    )

from xlea.providers.proto import ProviderProto


class PyXLSBProvider(ProviderProto):
    def __init__(self, path, sheet: Optional[str] = None):
        self._path = path
        self._sheet = sheet

    def rows(self):
        with pyxlsb.open_workbook(self._path) as book:
            if self._sheet:
                idx = book.sheets.index(self._sheet)
                sheet = book.get_sheet(idx)
            else:
                sheet = book.get_sheet(1)
            if sheet is None:
                raise ProviderError("Sheet not found")
            return (tuple(c.v for c in r) for r in sheet.rows())
