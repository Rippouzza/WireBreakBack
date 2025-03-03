from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plant(Base):
    __tablename__ = "plant"

    Plant = Column(String(20), primary_key=True)  # Primary Key
    Region = Column(String(30), nullable=False)
    Sales_Company = Column(Integer, nullable=False)
    Inv_Company = Column(Integer, nullable=False)
    plant_Description = Column(String(50), nullable=False)
