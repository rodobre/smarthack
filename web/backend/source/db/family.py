from . import Base, engine
from sqlalchemy import Column, Integer, String

class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key = True)

    caretakers = relationship("Caretaker", backref="family")
    patients = relationship("Patients", backref="family")

class Caretaker(Base):
    __tablename__ = "caretaker"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    desc = Column(String)
    img  = Column(String)
    phone = Column(String)

    family_id = Column(Integer, ForeignKey('family.id'))

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    img = Column(String)
    # add todo TODO

    family_id = Column(Integer, ForeignKey('family.id'))

Base.metadata.create_all(engine)
