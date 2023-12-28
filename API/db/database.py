from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# from dotenv import load_dotenv
# load_dotenv()

from src.env import(
    DEBUG, 
    DB_ACCESS
)

SQLALCHEMY_DATABASE_URL = DB_ACCESS

# from sqlalchemy import MetaData
# metadata_obj = MetaData(schema="jobManager")
# Base = declarative_base(metadata=metadata_obj)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()