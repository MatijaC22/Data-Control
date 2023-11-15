import math
from routers.schemas import Pages
from sqlalchemy.orm.session import Session
from db.models import DbPages
import datetime
from fastapi import HTTPException, status, UploadFile
from typing import List
import os
import json


def insert_pages_from_json(db: Session, json_file_path: str):
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        print(data)

    # Batch size for processing
    batch_size = 10

    # Split the data into batches and insert
    for i in range(0, len(data), batch_size):
        batch_data = data[i:i + batch_size]

        # Convert data to DbPages objects
        pages_to_insert = [
            DbPages(
                agent_id=44,  # Set the appropriate agent_id
                url=item.get('URL de la page'),
                data=json.dumps(item),
                mission='first'
            ) for item in batch_data
        ]

        # Add pages to the session
        db.add_all(pages_to_insert)

    # Commit the transaction
    db.commit()


# def get_all(db: Session, current_user:DbUser):
#     if not current_user.administrator:
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#           detail = f"User don't have authorization!")
    
#     return db.query(DbPost).all()

# def get_all_package(db: Session, current_user:DbUser, user_id=None, page: int = 1, per_page: int = 10):
    
#     offset = (page - 1) * per_page

#     # IF ADMINISTRATOR
#     if current_user.administrator:
#         query = db.query(DbPost)
#         if user_id:
#             query = query.filter(DbPost.user_id == user_id)
        
#         total_lines = query.count()  # Get the total number of lines

#         query = query.order_by(DbPost.last_modify.desc()).offset(offset).limit(per_page).all()
#         total_pages = math.ceil(total_lines / per_page)  # Calculate the total number of pages
#         return {
#             "lines": total_lines,
#             "pages": total_pages,
#             "page": page,
#             "per_page": per_page,
#             "data": query,
#         }
#         # return query

#     # IF NOT ADMINISTRATOR
#     if not current_user.administrator:
#         query = db.query(DbPost).filter(DbPost.user_id == current_user.id)
#         total_lines = query.count()  # Get the total number of lines
#         query = query.order_by(DbPost.last_modify.desc()).offset(offset).limit(per_page).all()
        
#         total_pages = math.ceil(total_lines / per_page)  # Calculate the total number of pages
#         return {
#             "lines": total_lines,
#             "pages": total_pages,
#             "page": page,
#             "per_page": per_page,
#             "data": query,
#         }
#         # return query

# # GORNJA FUNKCIJA RADI TAJ POSAO   
# # def get_user_posts(db: Session, current_user:DbUser, user_id=None, page: int = 1, per_page: int = 10):
# #     offset = (page - 1) * per_page

# #     if not current_user.administrator:
# #         query = db.query(DbPost).filter(DbPost.user_id == current_user.id)
# #         query = query.order_by(DbPost.last_modify.desc()).offset(offset).limit(per_page).all()
# #         return query    

# def get_one(db: Session, id: int, current_user:DbUser):
    
#     post = db.query(DbPost).filter(DbPost.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"Post with id {id} not found")
    
#     if not current_user.administrator and post.user_id != current_user.id:
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#           detail = f"User don't have authorization!")
    
#     return post

# def update_post(db:Session, id: int, current_user:DbUser, request: PostInsert):
#     post = db.query(DbPost).filter(DbPost.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#           detail = f"Post id {id} not found!")
    

#     #ZAVRSI OVO IDEJA JE OCISTITI DA SE UPDATE POST
#     if current_user.id != post.user_id:
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#           detail = f"User don't have authorization!")
       
#     post.image_url = request.reference_number
#     post.description = request.description
#     post.reference_number = request.reference_number
#     post.last_modify: datetime.datetime.now()

#     db.commit()
#     db.refresh(post)
#     return post

# def delete(db: Session, id: int, user_id: int):
#     post = db.query(DbPost).filter(DbPost.id == id).first()
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id {id} not found")
#     if (post.user_id != user_id):
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
#                             detail = 'only post creator can delete post')
    
#     db.delete(post)
#     db.commit()
#     return 'ok'