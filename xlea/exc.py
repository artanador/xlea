class XLEAError(Exception):
    pass


class ProviderError(XLEAError):
    pass


class HeaderNotFound(XLEAError):
    pass


class RequiredColumnMissingError(XLEAError):
    pass
