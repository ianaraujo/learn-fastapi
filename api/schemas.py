from pydantic import BaseModel

class StakeholderIn(BaseModel):
    name: str

class StakeholderOut(BaseModel):
    id: int
    name: str

class IssueIn(BaseModel):
    name: str

class IssueOut(BaseModel):
    id: int
    name: str