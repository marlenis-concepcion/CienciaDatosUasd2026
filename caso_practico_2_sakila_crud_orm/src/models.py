from dataclasses import dataclass, fields
from datetime import datetime


class BaseModel:
    table_name = ""
    primary_key = ""
    writable_fields = ()

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls, data):
        names = {field.name for field in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in names})


@dataclass
class Country(BaseModel):
    table_name = "country"
    primary_key = "country_id"
    writable_fields = ("country",)

    country_id: int | None = None
    country: str = ""
    last_update: datetime | None = None


@dataclass
class City(BaseModel):
    table_name = "city"
    primary_key = "city_id"
    writable_fields = ("city", "country_id")

    city_id: int | None = None
    city: str = ""
    country_id: int | None = None
    last_update: datetime | None = None


@dataclass
class Film(BaseModel):
    table_name = "film"
    primary_key = "film_id"
    writable_fields = (
        "title",
        "description",
        "release_year",
        "language_id",
        "rental_duration",
        "rental_rate",
        "length",
        "replacement_cost",
        "rating",
    )

    film_id: int | None = None
    title: str = ""
    description: str | None = None
    release_year: int | None = None
    language_id: int = 1
    rental_duration: int = 3
    rental_rate: float = 4.99
    length: int | None = None
    replacement_cost: float = 19.99
    rating: str | None = "PG"
    last_update: datetime | None = None


@dataclass
class Inventory(BaseModel):
    table_name = "inventory"
    primary_key = "inventory_id"
    writable_fields = ("film_id", "store_id")

    inventory_id: int | None = None
    film_id: int | None = None
    store_id: int | None = None
    last_update: datetime | None = None


class ModelCollection:
    def __init__(self, entity_type, items=None):
        self.entity_type = entity_type
        self.items = list(items or [])

    def add(self, entity):
        if not isinstance(entity, self.entity_type):
            raise TypeError(f"Solo se aceptan objetos {self.entity_type.__name__}.")
        self.items.append(entity)

    def to_list(self):
        return list(self.items)

    def to_dicts(self):
        return [entity.to_dict() for entity in self.items]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)
