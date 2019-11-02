from . import Base, engine
from sqlalchemy import Column, Integer, ForeignKey
import json

class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key = True)
    moves = Column(Integer)
    time = Column(Integer)
    answers_wrong = Column(Integer)
    answers_right = Column(Integer)

    patient_id = Column(Integer, ForeignKey('patient.id'))

    def __repr__(self):
        return json.dumps({'id':self.id,'moves':self.moves,'time':self.time,'answers_wrong':self.answers_wrong,'answers_right':self.answers_right,'patient_id':self.patient_id})

Base.metadata.create_all(engine)
