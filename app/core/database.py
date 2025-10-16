from sqlalchemy import URL, create_engine
from sqlmodel import Session, SQLModel

from .config import settings

USER = "betos" if settings.user == None or settings.user == "" else settings.user
PASSWORD = (
    "betos"
    if settings.password == None or settings.password == ""
    else settings.password
)
DATABASE = (
    "betos"
    if settings.database == None or settings.database == ""
    else settings.database
)
PORT = 3306 if settings.port == None or settings.port == "" else settings.port
HOST = "0.0.0.0" if settings.host == None or settings.host == "" else settings.host
DRIVER = (
    "mariadb+mariadbconnector"
    if settings.driver == None or settings.driver == ""
    else settings.driver
)

url = URL.create(DRIVER, USER, PASSWORD, HOST, PORT, DATABASE)
engine = create_engine(url=url)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
