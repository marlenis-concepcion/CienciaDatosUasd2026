from src.structures import EntityCache, QueryHistory


def test_query_history_keeps_recent_items():
    history = QueryHistory(max_items=2)
    history.push("create", "actor", {"id": 1})
    history.push("update", "actor", {"id": 1})
    history.push("delete", "actor", {"id": 1})

    items = history.list_recent()

    assert len(items) == 2
    assert items[0]["operation"] == "update"
    assert items[1]["operation"] == "delete"


def test_entity_cache_stores_and_removes_by_table_and_id():
    cache = EntityCache()
    cache.set("actor", 1, {"first_name": "ADA"})

    assert cache.get("actor", 1) == {"first_name": "ADA"}

    cache.remove("actor", 1)

    assert cache.get("actor", 1) is None

