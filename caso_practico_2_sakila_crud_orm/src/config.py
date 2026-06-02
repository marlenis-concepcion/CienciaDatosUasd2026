from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DatabaseConfig:
    host: str = os.getenv("SAKILA_DB_HOST", "localhost")
    user: str = os.getenv("SAKILA_DB_USER", "sakila_app")
    password: str = os.getenv("SAKILA_DB_PASSWORD", "")
    database: str = os.getenv("SAKILA_DB_NAME", "sakila")
    port: int = int(os.getenv("SAKILA_DB_PORT", "3306"))


DB_CONFIG = DatabaseConfig()
