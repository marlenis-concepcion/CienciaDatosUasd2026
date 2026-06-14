from src.controllers import (
    CityController,
    CountryController,
    FilmController,
    InventoryController,
    StoreController,
)
from src.dbcontext import SakilaDbContext


# /****
# Servicio de aplicacion para Sakila.
# Conecta el DbContext con los controladores usados por el menu principal.
# ****/
class SakilaService:
    def __init__(self, context=None):
        self.context = context or SakilaDbContext()
        self.countries = CountryController(self.context.countries)
        self.cities = CityController(self.context.cities)
        self.films = FilmController(self.context.films)
        self.stores = StoreController(self.context.stores)
        self.inventory = InventoryController(self.context.inventory)

    def close(self):
        self.context.close()
