from fastapi import APIRouter, Depends, status
from routers.schemas import PostBaseDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_search
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix = '/search',
    tags = ['search']
)


@router.get('/post/{search_term}', response_model=List[PostBaseDisplay])
def posts(search_term:str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_search.get_search_posts(search_term, db, current_user)
