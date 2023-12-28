from routers.schemas import PostBaseDisplay
from sqlalchemy.orm.session import Session 
from db.models import DbUsers, DbPosts, DbJobs
from fastapi import HTTPException, status
from sqlalchemy import or_

def get_search_posts(search_term: str, db: Session, current_user:DbUsers):

    if current_user.administrator:
      results = db.query(DbPosts).join(DbJobs).join(DbUsers).filter(
        or_(
            DbPosts.description.ilike(f'%{search_term}%'),
            DbPosts.reference_number.ilike(f'%{search_term}%'),
            DbUsers.email.ilike(f'%{search_term}%'),
            DbUsers.name.ilike(f'%{search_term}%'),
            DbUsers.last_name.ilike(f'%{search_term}%'),
            DbUsers.position.ilike(f'%{search_term}%'),
            DbJobs.location.ilike(f'%{search_term}%'),
            DbJobs.country.ilike(f'%{search_term}%'),
            DbJobs.responsible_name.ilike(f'%{search_term}%'),
            DbJobs.responsible_email.ilike(f'%{search_term}%'),
            DbJobs.client_name.ilike(f'%{search_term}%'),
            DbJobs.transport_type.ilike(f'%{search_term}%'),
            DbJobs.product_type.ilike(f'%{search_term}%'),
            # Add more columns as needed
        )
        ).all()
      return results
    
    results = db.query(DbPosts).join(DbJobs).join(DbUsers).filter(
        DbPosts.user_id == current_user.id,
        or_(
            DbPosts.description.ilike(f'%{search_term}%'),
            DbPosts.reference_number.ilike(f'%{search_term}%'),
            DbUsers.email.ilike(f'%{search_term}%'),
            DbUsers.name.ilike(f'%{search_term}%'),
            DbUsers.last_name.ilike(f'%{search_term}%'),
            DbUsers.position.ilike(f'%{search_term}%'),
            DbUsers.position.ilike(f'%{search_term}%'),
            DbJobs.location.ilike(f'%{search_term}%'),
            DbJobs.country.ilike(f'%{search_term}%'),
            DbJobs.responsible_name.ilike(f'%{search_term}%'),
            DbJobs.responsible_email.ilike(f'%{search_term}%'),
            DbJobs.client_name.ilike(f'%{search_term}%'),
            DbJobs.transport_type.ilike(f'%{search_term}%'),
            DbJobs.product_type.ilike(f'%{search_term}%'),
            # Add more columns as needed
        )
        ).all()
    return results


