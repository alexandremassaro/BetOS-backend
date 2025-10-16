import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

USER = os.getenv("USER", "root")
PASSWORD = os.getenv("PASSWORD", "betos")
DATABASE = os.getenv("DATABASE", "betos")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 3306))
DRIVER = "mariadb+mariadbconnector"

conn_url = URL.create(DRIVER, USER, PASSWORD, HOST, PORT, DATABASE)
engine = create_engine(conn_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
