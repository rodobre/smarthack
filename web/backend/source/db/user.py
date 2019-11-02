from . import Base, engine
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password_hash = Column(String, nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User id={} name={}>".format(self.id, self.name)

Base.metadata.create_all(engine)
