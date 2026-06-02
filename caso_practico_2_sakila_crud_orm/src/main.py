from src.db import DatabaseConnection
from src.services import ActorService


def show_actor(actor):
    if actor is None:
        print("No se encontro el actor.")
        return
    print(f"{actor.actor_id}: {actor.first_name} {actor.last_name} | {actor.last_update}")


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


def main():
    db = DatabaseConnection()
    service = ActorService(db)

    try:
        while True:
            print("\nCRUD/ORM Nativo Sakila - Actores")
            print("1. Crear actor")
            print("2. Buscar actor por ID")
            print("3. Listar actores")
            print("4. Actualizar actor")
            print("5. Eliminar actor")
            print("6. Ver historial de consultas")
            print("0. Salir")
            option = input("Opcion: ").strip()

            if option == "1":
                actor = service.create_actor(input("Nombre: "), input("Apellido: "))
                show_actor(actor)
            elif option == "2":
                show_actor(service.find_actor(read_int("ID: ")))
            elif option == "3":
                for actor in service.list_actors(read_int("Limite: ", default=10, minimum=1)):
                    show_actor(actor)
            elif option == "4":
                actor_id = read_int("ID: ")
                actor = service.update_actor(actor_id, input("Nombre: "), input("Apellido: "))
                show_actor(actor)
            elif option == "5":
                deleted = service.delete_actor(read_int("ID: "))
                print("Registro eliminado." if deleted else "No se elimino ningun registro.")
            elif option == "6":
                for item in service.repository.history.list_recent():
                    print(item)
            elif option == "0":
                break
            else:
                print("Opcion no valida.")
    except ValueError as exc:
        print(f"Entrada invalida: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
