# models/wire_break_detail.py

from sqlalchemy import Column, String, Integer, Date, Float, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WireBreakDetail(Base):
    __tablename__ = "wireBreakDetails"

    Plant = Column(String(20), primary_key=True)
    Supplier = Column(String(20), primary_key=True)
    Week_Number = Column(String(5), primary_key=True)
    Wire_Break_Type = Column(String(50), primary_key=True)
    Break_date = Column(Date, primary_key=True)
    num_of_break = Column(Integer, primary_key=True)
    Machine_Number = Column(String(20), primary_key=True)
    Batch_Number = Column(String(20))
    Break_Diameter = Column(Float)
    Range_ = Column(String(20))
    Finished_Wire_Diameter = Column(DECIMAL(4, 3))
