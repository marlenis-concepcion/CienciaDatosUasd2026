from src.models import City, Country, Film, Inventory, ModelCollection
from src.structures import EntityCache, QueryHistory


# /****
# Repositorio base del ORM nativo.
# Encapsula las operaciones CRUD genericas y evita repetir SQL por entidad.
# ****/
class BaseRepository:
    def __init__(self, db, model_cls, history=None, cache=None):
        self.db = db
        self.model_cls = model_cls
        self.history = history or QueryHistory()
        self.cache = cache or EntityCache()

    @property
    def table(self):
        return self.model_cls.table_name

    @property
    def primary_key(self):
        return self.model_cls.primary_key

    def create(self, data):
        payload = self._filter_writable_fields(data)
        columns = list(payload.keys()) + ["last_update"]
        placeholders = ["%s"] * len(payload) + ["NOW()"]
        values = tuple(payload.values())
        sql = f"INSERT INTO {self.table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

        with self.db.cursor() as cursor:
            cursor.execute(sql, values)
            new_id = cursor.lastrowid

        self.history.push("create", self.table, payload)
        return self.find_by_id(new_id)

    def find_by_id(self, entity_id):
        cached = self.cache.get(self.table, entity_id)
        if cached is not None:
            return cached

        sql = f"SELECT * FROM {self.table} WHERE {self.primary_key} = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (entity_id,))
            row = cursor.fetchone()

        self.history.push("find_by_id", self.table, {self.primary_key: entity_id})
        entity = self.model_cls.from_dict(row) if row else None
        if entity is not None:
            self.cache.set(self.table, entity_id, entity)
        return entity

    def find_all(self, limit=10):
        sql = f"SELECT * FROM {self.table} ORDER BY {self.primary_key} DESC LIMIT %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()

        self.history.push("find_all", self.table, {"limit": limit})
        return [self.model_cls.from_dict(row) for row in rows]

    def find_all_model(self, limit=10):
        return ModelCollection(self.model_cls, self.find_all(limit))

    def update(self, entity_id, data):
        payload = self._filter_writable_fields(data)
        if not payload:
            raise ValueError("No hay campos validos para actualizar.")

        assignments = [f"{column} = %s" for column in payload.keys()] + ["last_update = NOW()"]
        sql = f"UPDATE {self.table} SET {', '.join(assignments)} WHERE {self.primary_key} = %s"
        values = tuple(payload.values()) + (entity_id,)

        with self.db.cursor() as cursor:
            cursor.execute(sql, values)

        self.cache.remove(self.table, entity_id)
        self.history.push("update", self.table, {self.primary_key: entity_id, **payload})
        return self.find_by_id(entity_id)

    def delete(self, entity_id):
        sql = f"DELETE FROM {self.table} WHERE {self.primary_key} = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (entity_id,))
            affected = cursor.rowcount

        self.cache.remove(self.table, entity_id)
        self.history.push("delete", self.table, {self.primary_key: entity_id})
        return affected > 0

    def _filter_writable_fields(self, data):
        return {
            key: value
            for key, value in data.items()
            if key in self.model_cls.writable_fields and value is not None
        }


# /****
# Repositorio concreto para la entidad Country.
# Usa BaseRepository para operar sobre la tabla `country`.
# ****/
class CountryRepository(BaseRepository):
    def __init__(self, db, history=None, cache=None):
        super().__init__(db, Country, history, cache)


# /****
# Repositorio concreto para la entidad City.
# Usa BaseRepository para operar sobre la tabla `city`.
# ****/
class CityRepository(BaseRepository):
    def __init__(self, db, history=None, cache=None):
        super().__init__(db, City, history, cache)


# /****
# Repositorio concreto para la entidad Film.
# Usa BaseRepository para operar sobre la tabla `film`.
# ****/
class FilmRepository(BaseRepository):
    def __init__(self, db, history=None, cache=None):
        super().__init__(db, Film, history, cache)


# /****
# Repositorio concreto para la entidad Inventory.
# Usa BaseRepository para operar sobre la tabla `inventory`.
# ****/
class InventoryRepository(BaseRepository):
    def __init__(self, db, history=None, cache=None):
        super().__init__(db, Inventory, history, cache)
