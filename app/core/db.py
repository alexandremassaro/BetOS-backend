import os

from dotenv import load_dotenv
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

USER = os.getenv("USER", "root")
PASSWORD = os.getenv("PASSWORD", "betos")
DATABASE = os.getenv("DATABASE", "betos")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 3306))
DRIVER = "mariadb+mariadbconnector"


# def get_conn_url(
#     driver_name: str, user: str, password: str, host: str, port: int, database: str
# ):
#     return URL.create(driver_name, user, password, host, port, database)


def get_conn_url():
    return URL.create(DRIVER, USER, PASSWORD, HOST, PORT, DATABASE)


def get_engine(connection_url: URL):
    return create_engine(connection_url)


def get_session(engine: Engine):
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


conn_url = get_conn_url()
engine = get_engine(conn_url)
session = get_session(engine)
