from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from src.config import DB_CONFIG


class DatabaseConnectionError(RuntimeError):
    pass


class DatabaseConnection:
    def __init__(self, config=DB_CONFIG):
        self.config = config
        self.connection = None

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=self.config.host,
                    user=self.config.user,
                    password=self.config.password,
                    database=self.config.database,
                    port=self.config.port,
                )
            except Error as exc:
                raise DatabaseConnectionError(
                    "No se pudo conectar a MySQL Sakila. Verifique que MySQL este activo, "
                    "que el puerto sea correcto y que las credenciales existan en variables "
                    "SAKILA_DB_HOST, SAKILA_DB_PORT, SAKILA_DB_USER, SAKILA_DB_PASSWORD y "
                    "SAKILA_DB_NAME."
                ) from exc
        return self.connection

    @contextmanager
    def cursor(self, dictionary=True):
        connection = self.connect()
        cursor = connection.cursor(dictionary=dictionary)
        try:
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
