from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas

# stakeholder

def get_stakeholders(db: Session, search: str = None, skip: int = 0, limit: int = 5):
    query = db.query(models.Stakeholder)
    
    if search:
        search = search.lower()
        query = query.filter(models.Stakeholder.name.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

def create_stakeholder(db: Session, stakeholder: schemas.StakeholderCreate):
    db_stakeholder = db.query(models.Stakeholder).filter(models.Stakeholder.name == stakeholder.name).first()
    
    if db_stakeholder:
        raise HTTPException(status_code=400, detail="Stakeholder already exists!")
    
    new_stakeholder = models.Stakeholder(name=stakeholder.name)
    
    db.add(new_stakeholder)
    db.commit()
    db.refresh(new_stakeholder)
    
    return new_stakeholder


# issue

def get_issues(db: Session, search: str = None, skip: int = 0, limit: int = 5):
    query = db.query(models.Issue)

    if search:
        search = search.lower()
        query = query.filter(models.Issue.name.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

def create_issue(db: Session, issue: schemas.IssueCreate):
    db_issue = db.query(models.Issue).filter(models.Issue.name == issue.name).first()
    
    if db_issue:
        raise HTTPException(status_code=400, detail="Issue already exists!")
   
    new_issue = models.Issue(name=issue.name)
    
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    return new_issue


# minuta

def create_minuta(db: Session, minuta: schemas.MinutaCreate):
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

def get_minutas(db: Session, search: str = None, skip: int = 0, limit: int = 5):
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

    return query.offset(skip).limit(limit).all()

def get_minuta(db: Session, minuta_id: int):
    minuta = db.query(models.Minuta).filter(models.Minuta.id == minuta_id).first()

    if not minuta:
        raise HTTPException(status_code=404, detail=f"Minuta not found")
    
    return minuta

def update_minuta(db: Session, minuta_id: int, minuta: schemas.MinutaCreate):
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

def delete_minuta(db: Session, minuta_id: int):
    db_minuta = db.query(models.Minuta).filter(models.Minuta.id == minuta_id).first()
    
    if not db_minuta:
        raise HTTPException(status_code=404, detail="Minuta not found")
    
    db.delete(db_minuta)
    db.commit()

    return db_minuta
