from contextlib import contextmanager

import pytest

from src.repositories import InventoryRepository, StoreRepository


class FakeCursor:
    def __init__(self, films=None, stores=None):
        self.films = set(films or [])
        self.stores = set(stores or [])
        self.current_row = None
        self.rows = []
        self.lastrowid = 99
        self.rowcount = 1
        self.inserted = False

    def execute(self, sql, values=None):
        if "FROM film" in sql:
            self.current_row = {"exists": 1} if values[0] in self.films else None
        elif "FROM store" in sql and "WHERE" in sql:
            self.current_row = {"exists": 1} if values[0] in self.stores else None
        elif "FROM store" in sql:
            self.rows = [{"store_id": value} for value in sorted(self.stores)]
        elif sql.startswith("INSERT INTO inventory"):
            self.inserted = True
        elif "FROM inventory" in sql:
            self.current_row = {
                "inventory_id": 99,
                "film_id": 1,
                "store_id": 1,
                "last_update": None,
            }

    def fetchone(self):
        return self.current_row

    def fetchall(self):
        return self.rows


class FakeDatabase:
    def __init__(self, films=None, stores=None):
        self.fake_cursor = FakeCursor(films, stores)

    @contextmanager
    def cursor(self):
        yield self.fake_cursor


def test_inventory_rejects_unknown_film_before_insert():
    db = FakeDatabase(films={1}, stores={1})
    repository = InventoryRepository(db)

    with pytest.raises(ValueError, match="film_id=999"):
        repository.create({"film_id": 999, "store_id": 1})

    assert db.fake_cursor.inserted is False


def test_inventory_rejects_unknown_store_before_insert():
    db = FakeDatabase(films={1}, stores={1})
    repository = InventoryRepository(db)

    with pytest.raises(ValueError, match="store_id=999"):
        repository.create({"film_id": 1, "store_id": 999})

    assert db.fake_cursor.inserted is False


def test_store_repository_lists_valid_stores():
    repository = StoreRepository(FakeDatabase(stores={2, 1}))

    stores = repository.find_all()

    assert [store.store_id for store in stores] == [1, 2]
