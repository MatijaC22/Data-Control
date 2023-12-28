from fastapi import APIRouter, Depends, status
from routers.schemas import NotificationBase, NotificationDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db

from typing import List, Optional

from db import db_notification
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix = '/notification',
    tags = ['notification']
)


@router.post('/', response_model=NotificationDisplay | None)
def create(request: NotificationBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  return db_notification.create(db, request, current_user)


# @router.get('/all/', response_model=List[NotificationDisplay])
# def posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
#    return db_post.get_all(db, current_user)


# ID is USER_ID - get all notifications of one user
@router.get('/{id}', response_model=List[NotificationDisplay]) #, response_model = NotificationDisplay - neznam zasto mi ovo ne zeli prihvatiti
def post(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  return db_notification.get_all_from_user(db, id, current_user)

# ID is USER_ID
@router.post('/update/{id}', response_model = List[NotificationDisplay])
def update_container(id:int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  return db_notification.update_notification(db, id, current_user)
