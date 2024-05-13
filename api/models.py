from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# association tables

stakeholder_minuta = Table(
    'stakeholder_minuta', Base.metadata,
    Column('stakeholder_id', Integer, ForeignKey('stakeholders.id'), primary_key=True),
    Column('minuta_id', Integer, ForeignKey('minutas.id'), primary_key=True)
)

issue_minuta = Table(
    'issue_minuta', Base.metadata,
    Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=True),
    Column('minuta_id', Integer, ForeignKey('minutas.id'), primary_key=True)
)

# models

class Stakeholder(Base):
    __tablename__ = "stakeholders"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Minuta(Base):
    __tablename__ = "minutas"

    id = Column(Integer, primary_key=True)
    author = Column(Date, nullable=False)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, onupdate=func.now())
    header = Column(String, nullable=False)
    body = Column(String, nullable=False)
    stakeholders = relationship("Stakeholder", secondary=stakeholder_minuta, back_populates="minutas")
    issues = relationship("Issue", secondary=issue_minuta, back_populates="minutas")