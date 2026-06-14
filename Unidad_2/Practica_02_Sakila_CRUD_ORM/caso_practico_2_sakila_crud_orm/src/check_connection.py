from src.db import DatabaseConnection, DatabaseConnectionError


def main():
    db = DatabaseConnection()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT DATABASE() AS database_name, VERSION() AS mysql_version")
            row = cursor.fetchone()
        print("Conexion exitosa a MySQL.")
        print(f"Base de datos: {row['database_name']}")
        print(f"Version MySQL: {row['mysql_version']}")
    except DatabaseConnectionError as exc:
        print(exc)
        raise SystemExit(1) from exc
    finally:
        db.close()


if __name__ == "__main__":
    main()
