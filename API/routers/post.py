import os
from fastapi import APIRouter, Depends, Form, status, UploadFile, File
from routers.schemas import PostBase, PostBaseDisplay, PackageResponse
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_post
from typing import List, Optional
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix = '/post',
    tags = ['post']
)

@router.get('/all', response_model=List[PostBaseDisplay])
def posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_post.get_all(db, current_user)

@router.get('/package', response_model=PackageResponse)
def posts(page: int = 1, per_page: int = 10, user_id: Optional[int] = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   result = db_post.get_all_package(db, current_user, user_id, page, per_page)
   total_lines = result.get('lines')
   total_pages = result.get('pages')
   lines_per_page = result.get('per_page')
   actual_page = result.get('page')
   data = result.get('data')
   print(data)

   return PackageResponse(lines=total_lines, total_number_of_pages=total_pages, actual_page=actual_page, lines_per_page=lines_per_page, data=data)
   # return db_post.get_all_package(db, current_user, user_id, page, per_page)

@router.post("/create", response_model = PostBase)
def post(request: PostBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_post.create(db, request, current_user)

####################################################################################################################
@router.get('/{id}', response_model = PostBaseDisplay)
def get(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_post.get_one(db, id, current_user)


@router.post('/update/{id}', response_model = PostBaseDisplay)
def update_post(id:int, request: PostBaseDisplay, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db_post.update_post(db, id, current_user, request)


@router.post('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_post.delete(db, id, current_user.id)

def submit_form(
    name: str = Form(...),
    images: List[UploadFile]   = File(...), 
    current_user = Depends(get_current_user)
    ):
    return db_post.upload_image( name, current_user, images)

@router.post('/uploadImages/multi')
def submit_form(
    id: str = Form(...),
    images: List[UploadFile]   = File(...), 
    current_user = Depends(get_current_user)
    ):
    return db_post.upload_images_multi( id, current_user, images)
   