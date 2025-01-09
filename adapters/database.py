from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.gameModel import Base


#DATABASE_URL = "postgresql://postgres:121212@localhost:5432/onlinestore"
DATABASE_URL = "postgresql://postgres:121212@postgres-db:5432/onlinestore"

engine = create_engine(DATABASE_URL)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield db
    except:
        raise HTTPException(status_code= 500, detail= "Unable to connect to server.")
    finally:
        db.close()