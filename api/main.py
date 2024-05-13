from fastapi import FastAPI, Depends, HTTPException
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


# stakeholders

@app.get("/stakeholders/", response_model=list[schemas.StakeholderDisplay], tags=['stakeholders'])
def get_stakeholders(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    query = db.query(models.Stakeholder)
    
    if search:
        search = search.lower()
        query = query.filter(models.Stakeholder.name.ilike(f"%{search}%"))
        
    stakeholders = query.offset(skip).limit(limit).all()

    return stakeholders


@app.post("/stakeholders/", response_model=schemas.StakeholderDisplay, tags=['stakeholders'])
def create_stakeholder(stakeholder: schemas.StakeholderInput, db: Session = Depends(get_db)):
    is_created = db.query(models.Stakeholder) \
        .filter(models.Stakeholder.name == stakeholder.name) \
        .first()
    
    if is_created:
        raise HTTPException(status_code=400, detail="Stakeholder already exists!")
    
    stakeholder = models.Stakeholder(name=stakeholder.name)
    
    db.add(stakeholder)
    db.commit()
    db.refresh(stakeholder)

    return stakeholder


# issues

@app.get("/issues/", response_model=list[schemas.IssueDisplay], tags=['issues'])
def get_issues(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    query = db.query(models.Issue)
    
    if search:
        search = search.lower()
        query = query.filter(models.Issue.name.ilike(f"%{search}%"))
        
    issues = query.offset(skip).limit(limit).all()

    return issues


@app.post("/issues/", response_model=schemas.IssueDisplay, tags=['issues'])
def create_issue(issue: schemas.IssueInput, db: Session = Depends(get_db)):
    is_created = db.query(models.Issue) \
        .filter(models.Issue.name == issue.name) \
        .first()
    
    if is_created:
        raise HTTPException(status_code=400, detail="Stakeholder already exists!")
    
    issue = models.Issue(name=issue.name)
    
    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue


# minutas

@app.post("/minutas/", response_model=schemas.MinutaDisplay, tags=["minutas"])
def get_minutas(minuta: schemas.MinutaInput, db: Session = Depends(get_db)):
    minuta = models.Minuta(author=minuta.author, header=minuta.header, body=minuta.body)

    for id in minuta.stakeholders:
        stakeholder = db.query(models.Stakeholder).filter(models.Stakeholder.id == id).first()

        if not stakeholder:
            raise HTTPException(status_code=404, detail=f"Stakeholder with ID {id} not found")
        
        minuta.stakeholders.append(stakeholder)

    for id in minuta.issues:
        issue = db.query(models.Issue).filter(models.Issue.id == id).first()

        if not issue:
            raise HTTPException(status_code=404, detail=f"Issue with ID {id} not found")
        
        minuta.issues.append(issue)

    db.add(minuta)
    db.commit()
    db.refresh(minuta)

    return minuta