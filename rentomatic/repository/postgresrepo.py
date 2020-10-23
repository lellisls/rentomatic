from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rentomatic.domain import room
from rentomatic.repository.postgres_objects import Base, Room


class PostgresRepo:
    def __init__(self, connection_data):
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            connection_data['user'],
            connection_data['password'],
            connection_data['host'],
            connection_data['port'],
            connection_data['dbname']
        )

        self.engine = create_engine(connection_string)
        Base.metadata.bind = self.engine

    @classmethod
    def _create_room_objects(cls, results):
        return [
            room.Room(
                code=q.code,
                size=q.size,
                price=q.price,
                latitude=q.latitude,
                longitude=q.longitude
            )
            for q in results
        ]

    def list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Room)
        if filters is None:
            return self._create_room_objects(query.all())

        for f in filters.keys():
            column, op = f.split('__')
            if op == 'eq':
                query = query.filter(getattr(Room, column) == filters[f])
            elif op == 'lt':
                query = query.filter(getattr(Room, column) < filters[f])
            elif op == 'gt':
                query = query.filter(getattr(Room, column) > filters[f])

        return self._create_room_objects(query.all())
