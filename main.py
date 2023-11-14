# uvicorn main:app --reload

from fastapi import FastAPI
from db import models
from db.database import engine
from routers import pages, user
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication

import sys
print(sys.executable)

app = FastAPI()

app.include_router(pages.router)
app.include_router(user.router)
app.include_router(authentication.router)


@app.get('/')
def root():
    return 'Matija api za Ivanu'

origins = [
    # 'http://localhost:8080',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],#origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

models.Base.metadata.create_all(engine)

