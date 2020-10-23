class RoomListRequestObject:
    @classmethod
    def from_dict(cls, some_dict):
        return cls()

    def __bool__(self):
        return True
