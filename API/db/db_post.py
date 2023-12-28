import math
from routers.schemas import PostBase, UserBase
from sqlalchemy.orm.session import Session
from db.models import DbPosts, DbJobs, DbUsers
import datetime
from fastapi import HTTPException, status, UploadFile
from utils import validate_file_extension, validate_file_size
from typing import List
import os


# TO DO 
# AKO NISI OVLASTEN DA RADIS POST O NEKOM POSLU NE MOZES

def create(db: Session, inserted_post: PostBase, current_user: UserBase):
    job_exist = db.query(DbJobs).filter(DbJobs.id == inserted_post.job_id).first()
    
    if job_exist is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
          detail = f"Inserted job id doesn't exist!")
    
    post_exist = db.query(DbPosts).filter(DbPosts.job_id == inserted_post.job_id).first()
    
    if post_exist is not None and job_exist.id == post_exist.job_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
          detail = f"Post for this container reference already exist")
    
    if job_exist.user_id != current_user['id']:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
          detail = f"This user is not assigned for this job!")

    new_post = DbPosts(
        description = inserted_post.description,
        user_id = current_user['id'],
        created_at = datetime.datetime.now(),
        last_modify = datetime.datetime.now(),
        job_id = inserted_post.job_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post.to_dict()

def get_all(db: Session, current_user:DbUsers):
    if not current_user.access_level:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    return db.query(DbPosts).all()

def get_all_package(db: Session, current_user:DbUsers, user_id=None, page: int = 1, per_page: int = 10):
    
    offset = (page - 1) * per_page

    # IF ADMIN
    if current_user['access_level']:
        query = db.query(DbPosts)
        if user_id:
            query = query.filter(DbPosts.user_id == user_id)
        
        total_lines = query.count()  # Get the total number of lines

        query = query.order_by(DbPosts.last_modify.desc()).offset(offset).limit(per_page).all()
        total_pages = math.ceil(total_lines / per_page)  # Calculate the total number of pages
        return {
            "lines": total_lines,
            "pages": total_pages,
            "page": page,
            "per_page": per_page,
            "data": query,
        }
        # return query

    # IF NOT ADMIN
    if not current_user['access_level']:
        query = db.query(DbPosts).filter(DbPosts.user_id == current_user['id'])
        total_lines = query.count()  # Get the total number of lines
        query = query.order_by(DbPosts.last_modify.desc()).offset(offset).limit(per_page).all()
        
        total_pages = math.ceil(total_lines / per_page)  # Calculate the total number of pages
        return {
            "lines": total_lines,
            "pages": total_pages,
            "page": page,
            "per_page": per_page,
            "data": query,
        }
        # return query

def get_one(db: Session, id: int, current_user:DbUsers):
    
    post = db.query(DbPosts).filter(DbPosts.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} not found")
    
    if not current_user['access_level'] and post.user_id != current_user['id']:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    return post

def update_post(db:Session, id: int, current_user:DbUsers, request: PostBase):
    post = db.query(DbPosts).filter(DbPosts.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
          detail = f"Post id {id} not found!")
    
    if current_user['id'] != post.user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
       
    
    if post.job_id != request.job_id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
          detail = f"Its not possible to change job_id, reather delete it and make new one!")
       
    post.user_id = request.user_id
    post.description = request.description
    post.job_id = request.job_id
    post.last_modify: datetime.datetime.now()

    db.commit()
    db.refresh(post)
    return post

def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPosts).filter(DbPosts.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found")
    if (post.user_id != user_id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'only post creator can delete post')
    
    db.delete(post)
    db.commit()
    return 'ok'

def upload_image(name: str, current_user: DbUsers, images:List[UploadFile]):#images: UploadFile = File(...)):
    
    if (current_user['access_level'] != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")

    image_dir = f"assets/images/posts/"
    os.makedirs(image_dir, exist_ok=True)
    
    for image in images:
        validate_file_extension(os.path.splitext(image.filename)[1])        
        validate_file_size(image.file, 5 * 1024 * 1024)
        
        # image.filename = name
        # file_path = os.path.join(image_dir, name + '.jpg')
        with open(name + '.jpg', "wb") as f:
            f.write(image.file.read())
  
def upload_images_multi(id: str, current_user: DbUsers, images:List[UploadFile]):
    
    if (current_user['access_level'] != 1):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
          detail = f"User don't have authorization!")
    
    image_dir = f"assets/images/posts/{id}"
    os.makedirs(image_dir, exist_ok=True)
    
    for i,image in enumerate[images]:
        validate_file_extension(os.path.splitext(image.filename)[1])        
        validate_file_size(image.file, 5 * 1024 * 1024)
        
        # image.filename = name
        # file_path = os.path.join(image_dir, name + '.jpg')
        with open(i + '.jpg', "wb") as f:
            f.write(image.file.read())