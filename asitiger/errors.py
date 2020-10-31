import re


class Errors:
    class AsiError(Exception):
        """Base class for errors reported from the device"""

        pass

    class UnknownCommandError(AsiError):
        pass

    class UnrecognizedAxisParameterError(AsiError):
        pass

    class MissingParametersError(AsiError):
        pass

    class ParameterOutOfRangeError(AsiError):
        pass

    class OperationFailedError(AsiError):
        pass

    class UndefinedError(AsiError):
        pass

    class InvalidCardAddressException(AsiError):
        pass

    class SerialCommandHaltedError(AsiError):
        pass

    class UnknownError(AsiError):
        """Catch-all error used when the response code doesn't match a known error"""

        pass

    ERROR_RESPONSE_REGEX = re.compile(r":N-(.*)")

    CODE_TO_ERROR_CLASS = {
        "1": UnknownCommandError,
        "2": UnrecognizedAxisParameterError,
        "3": MissingParametersError,
        "4": ParameterOutOfRangeError,
        "5": OperationFailedError,
        "6": UndefinedError,
        "7": InvalidCardAddressException,
        "21": SerialCommandHaltedError,
    }

    @classmethod
    def raise_error_if_present(cls, command: str, response: str):
        error_match = cls.ERROR_RESPONSE_REGEX.search(response)

        if error_match:
            error_code = error_match.group(1)
            ErrorClass = cls.CODE_TO_ERROR_CLASS.get(error_code, cls.UnknownError)

            raise ErrorClass(f'Command "{command}" failed with response: {response}')
