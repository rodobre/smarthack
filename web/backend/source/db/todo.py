from . import Base, engine
from sqlalchemy import Column, Integer, String, Boolean

class Todo(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key = True)
    desc = Column(String)
    done = Column(Boolean)

    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship("Patient")
    caretaker_id = Column(Integer, ForeignKey('caretaker.id'))
    caretaker = relationship("Caretaker")

Base.metadata.create_all(engine)
