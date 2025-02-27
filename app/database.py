import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"), echo=True)
SessionLocal = sessionmaker(autoflush=False , autocommit=False , bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
