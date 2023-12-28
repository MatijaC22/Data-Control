from sqlalchemy.orm.session import Session 
from db.models import DbUsers
from routers.schemas import UserBase
# from db.hashing import Hash
from fastapi import HTTPException, status, UploadFile, File
import datetime
from typing import List
import os
from utils import validate_file_extension, validate_file_size

# Event function to create a new user if none exist
def create_initial_user(db: Session):
    user = db.query(DbUsers).first()

    if user is None:
        new_user = DbUsers(
            # password = Hash.bcrypt('matija'),
            name = 'matija',
            surname = 'corak',
            password = 'matija',
            email = 'matija@gmail.com',
            date_of_birth = '07/12/1992',
            image_url = 'matija@gmail.com.jpg',
            nationality = 'croatian',
            access_level = 1,
            active = True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

def create(db: Session, inserted_user:UserBase, current_user: UserBase):
    if current_user.get('access_level') != 1:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")

    user_exist = db.query(DbUsers).filter(DbUsers.email == inserted_user.email).first()
    
    if user_exist is not None: # and user_exist.email == inserted_user.email:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
          detail = f"User with this email already exist!")

    
    
    new_user = DbUsers(
        name = inserted_user.name,
        surname = inserted_user.surname,
        password = inserted_user.password,
        email = inserted_user.email,
        date_of_birth = inserted_user.date_of_birth,
        image_url = inserted_user.image_url,
        nationality = inserted_user.nationality,
        access_level = inserted_user.access_level,
        active = inserted_user.active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_dict = new_user.__dict__
    filtered_user_dict = {key: value for key, value in user_dict.items() if not key.startswith('_')}
    return filtered_user_dict


def get_user_by_email(db: Session, email: str):
    user = db.query(DbUsers).filter(DbUsers.email == email).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f'User with email {email} not found')
    return user.to_dict()

def update_user(db:Session, id: int, current_user:DbUsers, request: UserBase):
    user = db.query(DbUsers).filter(DbUsers.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
          detail = f"User id {id} not found!")
    
    if (current_user.get('access_level') != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
        
   
    user.name = request.name
    user.surname = request.surname
    user.password = request.password
    user.email = request.email
    user.date_of_birth = request.date_of_birth
    user.image_url = request.image_url
    user.nationality = request.nationality
    user.active = request.active
    user.access_level = request.access_level
    
    user_exist = db.query(DbUsers).filter(DbUsers.email == request.email).first()

    if user_exist and user_exist.id != user.id:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
          detail = f"Inserted email already exist!")

    db.commit()
    db.refresh(user)
    return user.to_dict()

def get_user_by_id(db: Session, id: str, current_user:DbUsers):

    if (current_user.get('access_level') != 1 and not current_user.get('id')==id):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    user = db.query(DbUsers).filter(DbUsers.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    return user.to_dict()

def get_all_users(db: Session, current_user:DbUsers):
    if (current_user.get('access_level') != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    users = db.query(DbUsers).all()
    users_dict_list = [user.to_dict() for user in users]

    return users_dict_list

def delete(db: Session, id: int, current_user:DbUsers):
    user = db.query(DbUsers).filter(DbUsers.id == id).first()

    if (current_user.get('access_level') != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id {id} not found")
    
    db.delete(user)
    db.commit()
    return 'ok'

def upload_image(name: str, current_user: DbUsers, images:List[UploadFile]):#images: UploadFile = File(...)):
    
    if (current_user.get('access_level') != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")

    image_dir = f"assets/images/users/"
    os.makedirs(image_dir, exist_ok=True)
    
    for image in images:
        validate_file_extension(os.path.splitext(image.filename)[1])        
        validate_file_size(image.file, 5 * 1024 * 1024)
        
        # image.filename = name
        # file_path = os.path.join(image_dir, name + '.jpg')
        with open(name + '.jpg', "wb") as f:
            f.write(image.file.read())
  
def upload_images_multi(id: int, current_user: DbUsers, images:List[UploadFile]):
    
    if (current_user.get('access_level') != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")

    image_dir = f"assets/images/items/{id}"
    os.makedirs(image_dir, exist_ok=True)
    
    for i,image in enumerate[images]:
        validate_file_extension(os.path.splitext(image.filename)[1])        
        validate_file_size(image.file, 5 * 1024 * 1024)
        
        # image.filename = name
        # file_path = os.path.join(image_dir, name + '.jpg')
        with open(i + '.jpg', "wb") as f:
            f.write(image.file.read())