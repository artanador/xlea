from typing import Union
from xlea.providers.openpyxl import OpenPyXlProvider
from xlea.providers.proto import ProviderProto
from xlea.providers.pyxlsb import PyXLSBProvider
from xlea.providers.xlrd import XLRDProvider

_PROVIDERS = {
    ".xlsx": OpenPyXlProvider,
    ".xls": XLRDProvider,
    ".xlsb": PyXLSBProvider,
}


def register_provider(ext: str, provider: ProviderProto):
    _PROVIDERS[_normalize_ext(ext)] = provider


def select_by_extension(ext: str) -> Union[type[ProviderProto], None]:
    return _PROVIDERS.get(_normalize_ext(ext))


def _normalize_ext(ext: str) -> str:
    ext = ext.lower()
    if not ext.startswith("."):
        ext = f".{ext}"
    return ext
