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
    """
    Register a data provider for a file extension.

    This function associates a file extension with a provider class.
    Once registered, the provider can be automatically selected when
    reading files with the corresponding extension.

    Parameters
    ----------
    ext : str
        File extension to register (e.g. ``".csv"``, ``"xlsx"``).
        The extension is normalized internally and is case-insensitive.
    provider : ProviderProto
        Provider class responsible for reading files with the given
        extension.

    Notes
    -----
    If a provider is already registered for the given extension,
    it will be silently overwritten.
    """

    _PROVIDERS[_normalize_ext(ext)] = provider


def select_by_extension(ext: str) -> Union[type[ProviderProto], None]:
    """
    Select a provider class based on file extension.

    Parameters
    ----------
    ext : str
        File extension (e.g. ``".xlsx"``). The value is normalized
        internally and is case-insensitive.

    Returns
    -------
    type[ProviderProto] or None
        Provider class registered for the given extension, or ``None``
        if no matching provider is found.

    Notes
    -----
    This function does not instantiate the provider; it only returns
    the provider class. Instantiation is the responsibility of the caller.
    """
    return _PROVIDERS.get(_normalize_ext(ext))


def _normalize_ext(ext: str) -> str:
    ext = ext.lower()
    if not ext.startswith("."):
        ext = f".{ext}"
    return ext
