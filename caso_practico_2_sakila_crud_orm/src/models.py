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
class Actor(BaseModel):
    table_name = "actor"
    primary_key = "actor_id"
    writable_fields = ("first_name", "last_name")

    actor_id: int | None = None
    first_name: str = ""
    last_name: str = ""
    last_update: datetime | None = None


@dataclass
class Customer(BaseModel):
    table_name = "customer"
    primary_key = "customer_id"
    writable_fields = ("store_id", "first_name", "last_name", "email", "address_id", "active")

    customer_id: int | None = None
    store_id: int | None = None
    first_name: str = ""
    last_name: str = ""
    email: str | None = None
    address_id: int | None = None
    active: int = 1
    create_date: datetime | None = None
    last_update: datetime | None = None

