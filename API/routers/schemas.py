import json
from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID


class ImageBase(BaseModel):
    id: Optional[int] = None
    post_id: int

class ImageBaseDisplay(BaseModel):
    id: int
    post_id: int

class UserBase(BaseModel): 
    id: Optional[int] = None
    name: str
    surname: str
    password: str
    email: str
    date_of_birth: Optional[datetime] = None
    image_url: Optional[str] = None
    nationality: str
    access_level: int
    active: bool

class UserBaseDisplay(BaseModel): 
    id: int
    name: str
    surname: str
    password: str
    email: str
    date_of_birth: Optional[datetime] = None
    image_url: Optional[str] = None
    nationality: str
    access_level: int
    active: bool
    class Config():
        orm_mode = True

class JobBase(BaseModel):
    id: Optional[int] = None
    reference_number: str
    user_id: Optional[int] = None
    # post_id: Optional[int] = None
    created_at: Optional[datetime] = None
    last_modify: Optional[datetime] = None

class JobBaseDisplay(BaseModel):
    id: int
    reference_number: str
    user_id: Optional[int] = None
    # post_id: Optional[int] = None
    created_at: datetime
    last_modify: datetime
    class Config():
        orm_mode = True

class PostBase(BaseModel):
    id: Optional[int] = None
    # image_id: Optional[List[int]] = None
    description: str
    user_id: int
    job_id: int
    created_at: Optional[datetime] = None
    last_modify: Optional[datetime] = None

class PostBaseDisplay(BaseModel):
    id: int
    # image_id: Optional[List[int]] = None
    description: str
    user_id: int
    job_id: int
    created_at: datetime
    last_modify: datetime
    user:UserBaseDisplay
    job:JobBaseDisplay
    images: List[ImageBaseDisplay]
    class Config():
        orm_mode = True

class CommentBase(BaseModel):
    id: Optional[int]
    text: str
    post_id: int
    created_at: Optional[datetime] = None
    last_modify: Optional[datetime] = None
    class Config():
        orm_mode = True
        
class CommentBaseDisplay(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int
    created_at: datetime
    last_modify: datetime
    post: PostBaseDisplay
    user: UserBaseDisplay
    class Config():
        orm_mode = True

class NotificationBase(BaseModel):
    id: Optional[int]
    user_id: int
    post_id: int
    created_at: Optional[datetime] = None
    last_modify: Optional[datetime] = None
    is_read: bool
    message: str

class NotificationDisplay(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    last_modify: datetime
    is_read: bool
    message: str
    owner: UserBaseDisplay
    post: PostBaseDisplay
    class Config():
        orm_mode = True






class PackageResponse(BaseModel):
    lines: int
    total_number_of_pages: int
    lines_per_page: int
    actual_page: int
    data: List[PostBaseDisplay]

# NEZNAM STO CE MI TO
class UserAuth(BaseModel):
    id: int
    email: str
    class Config():
        orm_mode = True


    




