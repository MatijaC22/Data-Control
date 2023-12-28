from sqlalchemy.orm.session import Session
from db.models import DbComments, DbUsers
from routers.schemas import CommentBase
from datetime import datetime
from fastapi import HTTPException, status
from db import db_notification


def create(db: Session, request: CommentBase, current_user:DbUsers):
    new_comment = DbComments(
        text = request.text,
        name = current_user.name,
        last_name = current_user.last_name,
        email = current_user.email,
        created_at = datetime.now(),
        last_modify = datetime.now(),
        post_id = request.post_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TREBA DODATI POST OWNER U OVU PRICU I PROMJENITI DA JE REQUEST OD DB_NOTIFICATION.CREATE NOTIFICATIONbASE
    db_notification.create(db, request, current_user)
    return new_comment


def get_all(db : Session, post_id: int):
    return db.query(DbComments).filter(DbComments.post_id == post_id ).all()
    

def delete(db: Session, id: int, current_user: DbUsers):
    comment = db.query(DbComments).filter(DbComments.id == id).first()
    if not comment:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"comment with id {id} not found")
    
    if (comment.email != current_user.email):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'only comment creator can delete comment')
    
    db.delete(comment)
    db.commit()
    return 'ok'