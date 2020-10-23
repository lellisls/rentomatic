from rentomatic.request_objects.room_list_request_object import RoomListRequestObject, InvalidRequestObject
from rentomatic.response_objects.response_objects import ResponseSuccess, ResponseFailure


class RoomListUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request_object):
        if not request_object:
            return ResponseFailure.build_from_invalid_request_object(request_object)

        try:
            rooms = self.repo.list(filters=request_object.filters)
            return ResponseSuccess(rooms)
        except Exception as exc:
            return ResponseFailure.build_system_error(f"{exc.__class__.__name__}: {'{}'.format(exc)}")
