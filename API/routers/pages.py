import os
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from routers.schemas import Pages
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_pages
from typing import List, Optional


router = APIRouter(
    prefix = '/data',
    tags = ['data']
)

@router.post("/insert_pages")
def insert_pages(json_file: str = "input.json", db: Session = Depends(get_db)): #json_file: UploadFile = Depends()
    
    # Determine the root folder dynamically
    root_folder = os.path.dirname(os.path.abspath(__file__))

    # Combine root folder and file name to get the full file path
    file_path = os.path.join('', json_file)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(file_path)
        raise HTTPException(status_code=400, detail="File not found")

    try:
        # Insert pages from the JSON file into the database
        db_pages.insert_pages_from_json(db, file_path)

        return {"message": "Pages inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.post("/createNewLines", response_model = List[Pages])
# def post(page: Pages, db: Session = Depends(get_db)):
#    return db_pages.create(db, page)
  


