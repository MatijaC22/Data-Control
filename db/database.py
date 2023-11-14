from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import secret_data

SQLALCHEMY_DATABASE_URL = secret_data.DB_ACCESS


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

#Base.metadata.create_all(bind=engine) -> this should work If the tables defined in your models (Pages for example) don't exist in the specified database, this call will create them. If the tables already exist, it will connect to them

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()