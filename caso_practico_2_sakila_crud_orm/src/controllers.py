# /****
# Controlador base del flujo CRUD.
# Expone metodos estandar para que la capa de menu no dependa del repositorio.
# ****/
class BaseController:
    def __init__(self, repository):
        self.repository = repository

    def create(self, data):
        return self.repository.create(data)

    def read(self, entity_id):
        return self.repository.find_by_id(entity_id)

    def list(self, limit=10):
        return self.repository.find_all_model(limit)

    def update(self, entity_id, data):
        return self.repository.update(entity_id, data)

    def delete(self, entity_id):
        return self.repository.delete(entity_id)


# /****
# Controlador de paises.
# Delega las acciones CRUD al repositorio de Country.
# ****/
class CountryController(BaseController):
    pass


# /****
# Controlador de ciudades.
# Delega las acciones CRUD al repositorio de City.
# ****/
class CityController(BaseController):
    pass


# /****
# Controlador de peliculas.
# Delega las acciones CRUD al repositorio de Film.
# ****/
class FilmController(BaseController):
    pass


# /****
# Controlador de inventario.
# Delega las acciones CRUD al repositorio de Inventory.
# ****/
class InventoryController(BaseController):
    pass
