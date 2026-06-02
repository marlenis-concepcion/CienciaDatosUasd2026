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


class CountryController(BaseController):
    pass


class CityController(BaseController):
    pass


class FilmController(BaseController):
    pass


class InventoryController(BaseController):
    pass

