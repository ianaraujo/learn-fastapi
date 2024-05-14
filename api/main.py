from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# stakeholder

@app.get("/stakeholders", response_model=list[schemas.Stakeholder], tags=['stakeholders'])
def get_stakeholders(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_stakeholders(db, search, skip, limit)

@app.post("/stakeholders", response_model=schemas.Stakeholder, tags=['stakeholders'])
def create_stakeholder(stakeholder: schemas.StakeholderCreate, db: Session = Depends(get_db)):
    return crud.create_stakeholder(db, stakeholder)

# issue

@app.get("/issues", response_model=list[schemas.Issue], tags=['issues'])
def get_issues(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_issues(db, search, skip, limit)

@app.post("/issues", response_model=schemas.Issue, tags=['issues'])
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    return crud.create_issue(db, issue)

# minuta

@app.post("/minutas", response_model=schemas.Minuta, tags=["minutas"])
def create_minuta(minuta: schemas.MinutaCreate, db: Session = Depends(get_db)):
    return crud.create_minuta(db, minuta)

@app.get("/minutas", response_model=list[schemas.Minuta], tags=["minutas"])
def get_minutas(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_minutas(db, search, skip, limit)

@app.get("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def read_minuta(minuta_id: int, db: Session = Depends(get_db)):
    return crud.get_minuta(db, minuta_id)

@app.put("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def update_minuta(minuta_id: int, minuta: schemas.MinutaCreate, db: Session = Depends(get_db)):
    return crud.update_minuta(db, minuta_id, minuta)

@app.delete("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def delete_minuta(minuta_id: int, db: Session = Depends(get_db)):
    return crud.delete_minuta(db, minuta_id)
