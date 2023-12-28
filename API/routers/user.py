from sqlalchemy.orm.session import Session
from db.database import get_db, SessionLocal
from fastapi import APIRouter, Depends, UploadFile, File, Form
from routers.schemas import UserBase#, UserUpdateBase, UserDisplay
from db import db_user
from typing import List, Optional
from auth.oauth2 import get_current_user


from fastapi.responses import JSONResponse
from fastapi import HTTPException

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

# Register the event function with the FastAPI app
@router.on_event('startup')
def startup_event():
    with SessionLocal() as db:
        return db_user.create_initial_user(db)

# @router.post('/', response_model = UserDisplay)
# def create_user(request: UserBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
#   return db_user.create_user(db, current_user.administrator, request)

@router.post("/create", response_model = UserBase)
def create_user(request: UserBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return db_user.create(db, request, current_user)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail)}, status_code=e.status_code)
    # return db_user.create(db, request, current_user)
   

@router.get('/all', response_model = List[UserBase])
def get_all_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_user.get_all_users(db, current_user)

@router.get('/{id}', response_model = UserBase)
def get_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_user.get_user_by_id(db, id, current_user)

@router.post('/update/{id}', response_model = UserBase)
def update_user(id:int, request: UserBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db_user.update_user(db, id, current_user, request)

@router.post('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   return db_user.delete(db, id, current_user)

@router.post('/uploadImage')
def submit_form(
    name: str = Form(...),
    images: List[UploadFile]   = File(...), 
    current_user = Depends(get_current_user)
    ):
    return db_user.upload_image( name, current_user, images)

# THIS IS HERE IN USER AS I DONT KNOW YET HOW WILL I USE IT, IDEA IS TO HAVE 
# ABILITY TO STORE MULTIPLE IAGES FOR ONE ITEM.
# IT WILL BE (FOR NOW) CONECTED WITH CONTAINERS JUST TO SEE IF IT WORKS
# IF IT WORKS IDEA IS TO MAKE NEW FOLDER FOR THIS ITEMS IN ASSETS AND TO INSERT NAMES AS ARRAY IN DB
@router.post('/uploadImages/multi')
def submit_form(
    id: int = Form(...),
    images: List[UploadFile]   = File(...), 
    current_user = Depends(get_current_user)
    ):
    return db_user.upload_images_multi( id, current_user, images)
   