from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "supplier"

    supplierid = Column(String(20), primary_key=True)  # Changed to String(20)
