from pydantic import BaseModel
from typing import List, Optional


# stakeholder

class StakeholderBase(BaseModel):
    name: str

class StakeholderCreate(StakeholderBase):
    pass

class Stakeholder(StakeholderBase):
    id: int

# issue

class IssueBase(BaseModel):
    name: str

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    id: int

# minuta

class MinutaBase(BaseModel):
    author: str
    header: str
    body: str

class MinutaCreate(MinutaBase):
    stakeholders: list[int]
    issues: list[int]

class Minuta(MinutaBase):
    id: int
    stakeholders: list[Stakeholder] = []
    issues: list[Issue] = []