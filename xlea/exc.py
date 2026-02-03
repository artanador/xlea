class XLEAError(Exception):
    pass


class ProviderError(XLEAError):
    pass


class HeaderNotFoundError(XLEAError):
    pass


class InvalidRowError(XLEAError):
    pass


class UnknownFileExtensionError(XLEAError):
    pass


class IncompatibleReturnValueTypeError(XLEAError):
    pass
