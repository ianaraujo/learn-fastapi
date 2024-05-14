from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from .database import SessionLocal, engine
from . import models, schemas

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
    query = db.query(models.Stakeholder)
    
    if search:
        search = search.lower()
        query = query.filter(models.Stakeholder.name.ilike(f"%{search}%"))
    
    stakeholders = query.offset(skip).limit(limit).all()
    
    return stakeholders

@app.post("/stakeholders", response_model=schemas.Stakeholder, tags=['stakeholders'])
def create_stakeholder(stakeholder: schemas.StakeholderCreate, db: Session = Depends(get_db)):
    db_stakeholder = db.query(models.Stakeholder).filter(models.Stakeholder.name == stakeholder.name).first()
    
    if db_stakeholder:
        raise HTTPException(status_code=400, detail="Stakeholder already exists!")
    
    new_stakeholder = models.Stakeholder(name=stakeholder.name)
    
    db.add(new_stakeholder)
    db.commit()
    db.refresh(new_stakeholder)
    
    return new_stakeholder

# issue

@app.get("/issues", response_model=list[schemas.Issue], tags=['issues'])
def get_issues(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    query = db.query(models.Issue)

    if search:
        search = search.lower()
        query = query.filter(models.Issue.name.ilike(f"%{search}%"))
    
    issues = query.offset(skip).limit(limit).all()
    
    return issues

@app.post("/issues", response_model=schemas.Issue, tags=['issues'])
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    db_issue = db.query(models.Issue).filter(models.Issue.name == issue.name).first()
    
    if db_issue:
        raise HTTPException(status_code=400, detail="Issue already exists!")
   
    new_issue = models.Issue(name=issue.name)
    
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    return new_issue

# minuta

@app.post("/minutas", response_model=schemas.Minuta, tags=["minutas"])
def create_minuta(minuta: schemas.MinutaCreate, db: Session = Depends(get_db)):
    new_minuta = models.Minuta(author=minuta.author, header=minuta.header, body=minuta.body)

    for stakeholder_id in minuta.stakeholders:
        stakeholder = db.query(models.Stakeholder).filter(models.Stakeholder.id == stakeholder_id).first()
        
        if not stakeholder:
            raise HTTPException(status_code=404, detail=f"Stakeholder with ID {stakeholder_id} not found")
        
        new_minuta.stakeholders.append(stakeholder)

    for issue_id in minuta.issues:
        issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
        
        if not issue:
            raise HTTPException(status_code=404, detail=f"Issue with ID {issue_id} not found")
        
        new_minuta.issues.append(issue)

    db.add(new_minuta)
    db.commit()
    db.refresh(new_minuta)

    return new_minuta


@app.get("/minutas", response_model=list[schemas.Minuta], tags=["minutas"])
def get_minutas(search: str | None = None, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):

    query = db.query(models.Minuta)

    if search:
        search = f"%{search.lower()}%"

        query = query \
            .join(models.Minuta.stakeholders) \
            .join(models.Minuta.issues) \
            .filter(or_(
                    models.Minuta.header.ilike(search),
                    models.Minuta.body.ilike(search),
                    models.Stakeholder.name.ilike(search),
                    models.Issue.name.ilike(search),
                )
            ).distinct()

    minutas = query.offset(skip).limit(limit).all()

    return minutas


@app.get("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def read_minuta(minuta_id: int, db: Session = Depends(get_db)):
    minuta = db.query(models.Minuta).filter(models.Minuta.id == minuta_id).first()

    if not minuta:
        raise HTTPException(status_code=404, detail=f"Minuta not found")
    
    return minuta

@app.put("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def update_minuta(minuta_id: int, minuta: schemas.MinutaCreate, db: Session = Depends(get_db)):
    db_minuta = db.query(models.Minuta).filter(models.Minuta.id == minuta_id).first()

    if not db_minuta:
        raise HTTPException(status_code=404, detail=f"Minuta not found")
    
    db_minuta.author = minuta.author
    db_minuta.header = minuta.header
    db_minuta.body = minuta.body
    db_minuta.stakeholders.clear()
    db_minuta.issues.clear()

    for stakeholder_id in minuta.stakeholders:
        stakeholder = db.query(models.Stakeholder).filter(models.Stakeholder.id == stakeholder_id).first()
        
        if not stakeholder:
            raise HTTPException(status_code=404, detail=f"Stakeholder with ID {stakeholder_id} not found")
        
        db_minuta.stakeholders.append(stakeholder)

    for issue_id in minuta.issues:
        issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
        
        if not issue:
            raise HTTPException(status_code=404, detail=f"Issue with ID {issue_id} not found")
        
        db_minuta.issues.append(issue)
    
    db.commit()
    db.refresh(db_minuta)

    return db_minuta

@app.delete("/minutas/{minuta_id}", response_model=schemas.Minuta, tags=["minutas"])
def delete_minuta(minuta_id: int, db: Session = Depends(get_db)):
    db_minuta = db.query(models.Minuta).filter(models.Minuta.id == minuta_id).first()
    
    if not db_minuta:
        raise HTTPException(status_code=404, detail="Minuta not found")
    
    db.delete(db_minuta)
    db.commit()

    return db_minuta
