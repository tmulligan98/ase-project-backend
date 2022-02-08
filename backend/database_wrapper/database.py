from backend.utils import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Globals
SQLALCHEMY_DATABASE_URL = SETTINGS.database_url
ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = declarative_base()


def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    try:
        yield db
    finally:
        db.close()
