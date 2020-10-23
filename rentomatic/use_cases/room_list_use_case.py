from rentomatic.response_objects.response_objects import ResponseSuccess


class RoomListUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self) -> ResponseSuccess:
        rooms = self.repo.list()
        return ResponseSuccess(rooms)
