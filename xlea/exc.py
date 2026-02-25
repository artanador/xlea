class XLEAError(Exception):
    pass


class ProviderError(XLEAError):
    pass


class HeaderNotFound(XLEAError):
    pass


class MissingRequiredColumns(HeaderNotFound):
    pass


class InvalidRowError(XLEAError):
    pass


class UnknownFileExtensionError(XLEAError):
    pass


class IncompatibleReturnValueTypeError(XLEAError):
    pass
