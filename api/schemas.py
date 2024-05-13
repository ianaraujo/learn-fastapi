from pydantic import BaseModel
from datetime import datetime


class StakeholderID(BaseModel):
    id: int

class StakeholderInput(BaseModel):
    name: str

class StakeholderDisplay(BaseModel):
    id: int
    name: str


class IssueID(BaseModel):
    id: int

class IssueInput(BaseModel):
    name: str

class IssueDisplay(BaseModel):
    id: int
    name: str


class MinutaInput(BaseModel):
    author: str
    header: str
    body: str
    stakeholders: list[int]
    issues: list[int]

class MinutaDisplay(BaseModel):
    id: int
    author: str
    header: str
    body: str
    stakeholders: list[StakeholderDisplay]
    issues: list[IssueDisplay]