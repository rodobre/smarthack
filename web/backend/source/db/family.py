from . import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Caretaker(Base):
    __tablename__ = "caretaker"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    desc = Column(String)
    img  = Column(String)
    phone = Column(String)

    password = Column(String)

    family_id = Column(Integer, ForeignKey('family.id'))

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    img = Column(String)

    family_id = Column(Integer, ForeignKey('family.id'))

class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key = True)

    caretakers = relationship("Caretaker", backref="family")
    patients = relationship("Patient", backref="family")


Base.metadata.create_all(engine)
