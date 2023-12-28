from routers.schemas import JobBase
from sqlalchemy.orm.session import Session 
from db.models import DbJobs, DbUsers
from fastapi import HTTPException, status
import datetime



def create_job(db: Session, job:JobBase, current_user:DbUsers):

    if not current_user.get('access_level') == 1:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    job_exist = db.query(DbJobs).filter(DbJobs.reference_number == job.reference_number).first()
    if job_exist:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
          detail = f"Inserted job reference number already exist!")
    
    user_exist = db.query(DbUsers).filter(DbUsers.id == job.user_id).first()
    if not user_exist and job.user_id != 0:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
          detail = f"User with id {job['user_id']} doesn't exist exist!")
    
    new_job = DbJobs(       
        reference_number = job.reference_number,
        user_id = job.user_id,
        created_at = datetime.datetime.now(),
        last_modify = datetime.datetime.now(),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def update_job(db:Session, id: int, current_user:DbUsers, request: JobBase):
    job = db.query(DbJobs).filter(DbJobs.id == id).first()
    
    if not job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
          detail = f"job id {id} not found!")
    
    if not current_user.get('access_level') == 1:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
        
    job.reference_number = request.reference_number
    job.user_id = request.user_id
    job.last_modify = datetime.datetime.now()

    job_exist = db.query(DbJobs).filter(DbJobs.reference_number == request.reference_number).first()
    if job_exist and job_exist.id != job.id:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
          detail = f"Inserted email already exist!")

    db.commit()
    db.refresh(job)
    return job

def get_job_by_reference_number(db: Session, reference_number: str, current_user:DbUsers):

    job = db.query(DbJobs).filter(DbJobs.reference_number == reference_number).first()

    if (not current_user.get('access_level') == 1):# and not current_user['email'] ==job.responsible_email):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    if not job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f'job with reference_number {reference_number} not found')
    return job

def get_job_by_id(db: Session, id: str, current_user:DbUsers):

    if (not current_user.get('access_level') == 1 and not current_user['id']==id):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    job = db.query(DbJobs).filter(DbJobs.id == id).first()

    if not job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f'job with id {id} not found')
    return job

def get_all_jobs(db: Session, current_user:DbUsers):
    if not current_user.get('access_level') == 1:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    return db.query(DbJobs).all()

def delete(db: Session, id: int, current_user:DbUsers):
    job = db.query(DbJobs).filter(DbJobs.id == id).first()

    if not current_user.get('access_level') == 1:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    if not job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"job with id {id} not found")
    
    db.delete(job)
    db.commit()
    return 'ok'

