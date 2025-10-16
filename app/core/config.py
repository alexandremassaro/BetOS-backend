import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


class Settings:
    def __init__(self) -> None:
        # App Config
        self.app_name = os.getenv("APP_NAME", "BetOS")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"

        # Database Config
        self.database = os.getenv("MARIADB_DATABASE", "betos")
        self.root_password = os.getenv("MARIADB_ROOT_PASSWORD", "betos")
        self.user = os.getenv("MARIADB_USER", "betos")
        self.password = os.getenv("MARIADB_PASSWORD", "betos")
        self.host = os.getenv("MARIADB_HOST", "0.0.0.0")
        self.port = int(os.getenv("MARIADB_PORT", 3306))
        self.driver = os.getenv("DB_DRIVER", "mariadb+mariadbconnector")
        self.database_url = URL.create(
            self.driver, self.user, self.password, self.host, self.port, self.database
        ).render_as_string(hide_password=False)

        # Security Config
        self.algorithm = str(os.getenv("ALGORITHM", "HS256"))
        self.access_token_expire_minutes = float(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 50)
        )
        self.secret_key = os.getenv(
            "SECRET_KEY",
            "c2867a4801c55069b46a1b54d944d0fb527738e4421c1059797ab57845113b29",
        )
        if not self.secret_key:
            raise ValueError("É preciso especificar uma chave secreta")


settings = Settings()
