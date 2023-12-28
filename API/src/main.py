# uvicorn main:app --reload

from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from db import models
from db.database import engine
from routers import user, post, comment, job, notification, search, sideFunctionalities
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication


import logging



logging.basicConfig(
        # stream=sys.stderr,
        level=logging.WARNING,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        filename="logs.log"
    )
logger = logging.getLogger(__name__)

logging.info('App start!')

import sys
print(sys.executable)



app = FastAPI()
app.include_router(user.router)
app.include_router(job.router)
app.include_router(post.router)
app.include_router(notification.router)
app.include_router(search.router)
app.include_router(sideFunctionalities.router)
app.include_router(authentication.router)
app.include_router(comment.router)

@app.get('/')
def root():
    return 'Welcome to Job Manager!'

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

app.mount('/assets', StaticFiles(directory='assets'), name='assets')