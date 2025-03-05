from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MachineType(Base):
    __tablename__ = "machinetype"

    machinetype = Column(String(20), primary_key=True)
    minBreakDiameter = Column(Float)
    maxBreakDiameter = Column(Float)
