from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WireBreakType(Base):
    __tablename__ = "wirebreaktype"

    wirebreaktype = Column(String(50), primary_key=True)
    typeB = Column(String(30))
