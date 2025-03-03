from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Machine(Base):
    __tablename__ = "machine"

    codeMachine = Column(String(20), primary_key=True)
    typeM = Column(String(20))
