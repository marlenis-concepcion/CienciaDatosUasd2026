from src.db import DatabaseConnection
from src.repositories import CityRepository, CountryRepository, FilmRepository, InventoryRepository
from src.structures import EntityCache, QueryHistory


# /****
# Contexto principal del ORM nativo.
# Agrupa conexion, repositorios, cache e historial en un solo punto de acceso.
# ****/
class SakilaDbContext:
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
        self.history = QueryHistory()
        self.cache = EntityCache()
        self.countries = CountryRepository(self.db, self.history, self.cache)
        self.cities = CityRepository(self.db, self.history, self.cache)
        self.films = FilmRepository(self.db, self.history, self.cache)
        self.inventory = InventoryRepository(self.db, self.history, self.cache)

    def close(self):
        self.db.close()
