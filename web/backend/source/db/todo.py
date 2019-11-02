from . import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import json

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key = True)
    desc = Column(String)
    done = Column(Boolean)

    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship("Patient")
    caretaker_id = Column(Integer, ForeignKey('caretaker.id'))
    caretaker = relationship("Caretaker")

    def __repr__(self):
        return json.dumps({'id':self.id,'desc':self.desc,'done':self.done,'patient_id':self.patient_id,'caretaker_id':self.caretaker_id})

Base.metadata.create_all(engine)
