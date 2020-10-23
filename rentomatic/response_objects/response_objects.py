from rentomatic.request_objects.room_list_request_object import InvalidRequestObject


class ResponseFailure:
    RESOURCE_ERROR = 'ResourceError'
    PARAMETERS_ERROR = 'ParametersError'
    SYSTEM_ERROR = 'SystemError'

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    @staticmethod
    def _format_message(message):
        if isinstance(message, Exception):
            return f"{message.__class__.__name__}: {message}"
        return message

    @property
    def value(self):
        return {
            'type': self.type,
            'message': self.message
        }

    def __bool__(self):
        return False

    @classmethod
    def build_from_invalid_request_object(cls, req: InvalidRequestObject) -> 'ResponseFailure':
        message = "\n".join([f"{err['parameter']}: {err['message']}" for err in req.errors])
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_resource_error(cls, message=None) -> 'ResponseFailure':
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message=None) -> 'ResponseFailure':
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None) -> 'ResponseFailure':
        return cls(cls.SYSTEM_ERROR, message)


class ResponseSuccess:
    SUCCESS = "Success"

    def __init__(self, value=None):
        self.type = self.SUCCESS
        self.value = value

    def __bool__(self):
        return True
