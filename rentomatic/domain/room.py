
class Room:
    def __init__(self, code, size, price, longitude, latitude):
        self.code = code
        self.size = size
        self.price = price
        self.longitude = longitude
        self.latitude = latitude

    @classmethod
    def from_dict(cls, some_dict) -> 'Room':
        return cls(
            code=some_dict['code'],
            size=some_dict['size'],
            price=some_dict['price'],
            longitude=some_dict['longitude'],
            latitude=some_dict['latitude']
        )

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'size': self.size,
            'price': self.price,
            'longitude': self.longitude,
            'latitude': self.latitude
        }
