import json
from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID

class Agents(BaseModel):
    # agent_id: int
    agent_uuid: UUID4
    agent_name: str
    launch_secret: str
    rate: int
    max_concurrent: Optional[int] = None
    max_delay: int
    fields_order: Optional[Dict] = None
    output_type: Optional[str] = None
    active: Optional[bool] = False

class Pages(BaseModel):
    # page_id: int
    agent_id: int
    url: str
    created_at: Optional[datetime] = None
    launched_on: Optional[datetime] = None
    finalized_at: Optional[datetime] = None
    last_seen_on: Optional[datetime] = None
    data: Dict
    scrape_done: bool
    mission: str
    priority: int

class PageJobMatrix(BaseModel):
    page_id: int
    job_id: int

class Jobs(BaseModel):
    # job_id: int
    agent_id: int
    job_uuid: UUID4
    launched_at: Optional[datetime] = None
    finished_on: Optional[datetime] = None
    results: Dict

class UserBase(BaseModel):    
    access_level: int
    name: str
    surname: str
    password: str
    email: str
    date_of_birth: Optional[datetime] = None
    image_url: Optional[str] = None
    nationality: str
    access_level: int
    active: bool
    




