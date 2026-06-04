from src.db import DatabaseConnectionError
from src.reports import film_metric_report
from src.services import SakilaService


def read_int(prompt, default=None, minimum=None):
    value = input(prompt).strip()
    if not value and default is not None:
        return default
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError("Debe introducir un numero entero.") from exc
    if minimum is not None and number < minimum:
        raise ValueError(f"El valor minimo permitido es {minimum}.")
    return number


def print_entity(entity):
    if entity is None:
        print("No se encontro el registro.")
    elif hasattr(entity, "to_dict"):
        print(entity.to_dict())
    else:
        print(entity)


def country_menu(service):
    print("\nPaises")
    print("1. Crear pais")
    print("2. Buscar pais por ID")
    print("3. Listar paises")
    print("4. Actualizar pais")
    print("5. Eliminar pais de prueba")
    option = input("Opcion: ").strip()

    if option == "1":
        print_entity(service.countries.create({"country": input("Pais: ").strip()}))
    elif option == "2":
        print_entity(service.countries.read(read_int("ID: ")))
    elif option == "3":
        for item in service.countries.list(read_int("Limite: ", default=10, minimum=1)):
            print_entity(item)
    elif option == "4":
        print_entity(service.countries.update(read_int("ID: "), {"country": input("Pais: ").strip()}))
    elif option == "5":
        print("Eliminado." if service.countries.delete(read_int("ID: ")) else "No eliminado.")


def city_menu(service):
    print("\nCiudades")
    print("1. Crear ciudad")
    print("2. Buscar ciudad por ID")
    print("3. Listar ciudades")
    print("4. Actualizar ciudad")
    print("5. Ver paises con ID")
    option = input("Opcion: ").strip()

    if option == "1":
        print("\nPaises disponibles:")
        for country in service.countries.list(30):
            print_entity(country)
        data = {"city": input("Ciudad: ").strip(), "country_id": read_int("country_id: ")}
        print_entity(service.cities.create(data))
    elif option == "2":
        print_entity(service.cities.read(read_int("ID: ")))
    elif option == "3":
        for item in service.cities.list(read_int("Limite: ", default=10, minimum=1)):
            print_entity(item)
    elif option == "4":
        print("\nPaises disponibles:")
        for country in service.countries.list(30):
            print_entity(country)
        data = {"city": input("Ciudad: ").strip(), "country_id": read_int("country_id: ")}
        print_entity(service.cities.update(read_int("ID: "), data))
    elif option == "5":
        for country in service.countries.list(read_int("Limite: ", default=30, minimum=1)):
            print_entity(country)


def film_menu(service):
    print("\nPeliculas")
    print("1. Crear pelicula de prueba")
    print("2. Buscar pelicula por ID")
    print("3. Listar peliculas")
    print("4. Actualizar pelicula")
    option = input("Opcion: ").strip()

    if option == "1":
        data = {
            "title": input("Titulo: ").strip().upper(),
            "description": input("Descripcion: ").strip(),
            "release_year": read_int("Anio: ", default=2026, minimum=1900),
            "language_id": read_int("language_id: ", default=1, minimum=1),
        }
        print_entity(service.films.create(data))
    elif option == "2":
        print_entity(service.films.read(read_int("ID: ")))
    elif option == "3":
        for item in service.films.list(read_int("Limite: ", default=10, minimum=1)):
            print_entity(item)
    elif option == "4":
        data = {"title": input("Titulo: ").strip().upper(), "description": input("Descripcion: ").strip()}
        print_entity(service.films.update(read_int("ID: "), data))


def inventory_menu(service):
    print("\nInventario")
    print("1. Crear inventario")
    print("2. Buscar inventario por ID")
    print("3. Listar inventario")
    option = input("Opcion: ").strip()

    if option == "1":
        data = {"film_id": read_int("film_id: "), "store_id": read_int("store_id: ")}
        print_entity(service.inventory.create(data))
    elif option == "2":
        print_entity(service.inventory.read(read_int("ID: ")))
    elif option == "3":
        for item in service.inventory.list(read_int("Limite: ", default=10, minimum=1)):
            print_entity(item)


def main():
    service = SakilaService()
    try:
        while True:
            print("\nCRUD/ORM Nativo Sakila - UASDVirtual")
            print("1. Paises")
            print("2. Ciudades")
            print("3. Peliculas")
            print("4. Inventario")
            print("5. Metricas descriptivas de peliculas")
            print("6. Historial de operaciones")
            print("0. Salir")
            option = input("Opcion: ").strip()

            if option == "1":
                country_menu(service)
            elif option == "2":
                city_menu(service)
            elif option == "3":
                film_menu(service)
            elif option == "4":
                inventory_menu(service)
            elif option == "5":
                print(film_metric_report(service.context.db))
            elif option == "6":
                for item in service.context.history.list_recent():
                    print(item)
            elif option == "0":
                break
            else:
                print("Opcion no valida.")
    except ValueError as exc:
        print(f"Entrada invalida: {exc}")
    except DatabaseConnectionError as exc:
        print(f"Error de conexion: {exc}")
    finally:
        service.close()


if __name__ == "__main__":
    main()
