from sanic.exceptions import SanicException


class AppException(Exception):
    """
    Base exception, extended by all specific exceptions raised by the application.

    Its usage should be avoided.
    """
    pass


class ConfigException(AppException):
    """
    Raised whenever an error occurs regarding the configuration.
    """
    pass


class NonexistentModel(AppException):
    """
    Raised if a model isn't found in the models dict.
    """
    pass


class OverlappingModel(AppException):
    """
    Raised if overlapping a model is attempted.
    """
    pass


class PayloadFieldsMethodMissing(SanicException):
    """
    Raised if the view class is missing the _payload_fields() coroutine.
    """
    def __init__(self):
        super().__init__("A view class is missing the coroutine _payload_fields()", status_code=500)


class NotCallable(SanicException):
    def __init__(self, class_method: str, class_name: str):
        super().__init__("{0} in {1} must be a callable".format(class_method, class_name), status_code=500)

class MalformedJsonPayload(SanicException):
    """
    Raised if the request body couldn't be parsed by the json decoder.
    """
    def __init__(self):
        super().__init__("You sent a malformed json payload", status_code=400)


class InvalidJsonPayload(SanicException):
    """
    Raised when the predicate that verifies the json payload returns false. Happens after the payload has been
    successfully parsed.
    """
    def __init__(self):
        super().__init__("You sent a json payload that has failed the checks", status_code=400)
