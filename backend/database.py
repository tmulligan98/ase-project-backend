from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "mysql_db"
PASSWORD = "root"
USER = "user"
HOST = "db"

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
