from rentomatic.domain import room as r


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self, filters=None):
        result = [r.Room.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if 'code__eq' in filters:
            result = [room for room in result if room.code == filters['code__eq']]

        if 'price__eq' in filters:
            result = [room for room in result if room.price == int(filters['price__eq'])]

        if 'price__lt' in filters:
            result = [room for room in result if room.price < int(filters['price__lt'])]

        if 'price__gt' in filters:
            result = [room for room in result if room.price > int(filters['price__gt'])]

        return result
