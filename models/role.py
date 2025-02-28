from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = "Role"

    ID = Column(String(50), primary_key=True)
    Password = Column(String(255), nullable=False)  # Plaintext password storage
    Role = Column(String(20), nullable=False)
