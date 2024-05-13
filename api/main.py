from fastapi import FastAPI
from pydantic import BaseModel


class Stakeholder(BaseModel):
    nome: str
    cargo: str | None = None
    idade: int

class Minuta(BaseModel):
    header: str
    body: str
    stakeholders: list[Stakeholder] | None = None


app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello Second"}

@app.get("/stakeholders/", tags=['stakeholders'])
def read_stakeholders():
    return {}

@app.post("/stakeholders/", tags=['stakeholders'])
async def create_stakeholder(stakeholder: Stakeholder):
    stake_dict = stakeholder.model_dump()
    stake_dict.update({"idoso": stakeholder.idade >= 65})

    return stake_dict