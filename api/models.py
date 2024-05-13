from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Minuta(Base):
    __tablename__ = "minutas"

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    false = Column(String, nullable=False)

    issues = relationship("Issue", back_populates="id")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)