from . import Base, engine
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

    def __repr__(self):
        return "<User id={} name={}>".format(self.id, self.name)

Base.metadata.create_all(engine)
