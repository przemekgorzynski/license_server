from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
import os


url = URL.create(
    drivername="postgresql",
    username=os.getenv("POSTGRESQL_USER"),
    password=os.getenv("POSTGRESQL_PASSWORD"),
    host=os.getenv("POSTGRESQL_HOST"),
    database=os.getenv("POSTGRESQL_DATABASE"),
    port=os.getenv("POSTGRESQL_PORT"),
)

engine = create_engine(url)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
