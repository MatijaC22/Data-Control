from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import APIRouter, Depends, Form
from routers.schemas import JobBaseDisplay, JobBase
from db import db_job
from auth.oauth2 import get_current_user
from typing import List, Optional


router = APIRouter(
    prefix = '/job',
    tags = ['job']
)


@router.post('/create', response_model = JobBaseDisplay)
def create_job(request: JobBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  return db_job.create_job(db, request, current_user)

@router.get('/all', response_model=List[JobBaseDisplay])
def get_all_jobs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_job.get_all_jobs(db, current_user)

@router.get('/{id}', response_model=JobBaseDisplay)
def get_job(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_job.get_job_by_id(db, id, current_user)

@router.get('/reference/{reference_number}', response_model=JobBaseDisplay)
def get_job(reference_number: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_job.get_job_by_reference_number(db, reference_number, current_user)

@router.post('/update/{id}', response_model = JobBaseDisplay)
def update_job(id:int, request: JobBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db_job.update_job (db, id, current_user, request)

@router.post('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_job.delete(db, id, current_user)
