from collections import deque


# /****
# Historial de operaciones ejecutadas en el CRUD.
# Usa una cola limitada para conservar las acciones mas recientes.
# ****/
class QueryHistory:
    def __init__(self, max_items=20):
        self.items = deque(maxlen=max_items)

    def push(self, operation, table, payload=None):
        self.items.append({"operation": operation, "table": table, "payload": payload or {}})

    def list_recent(self):
        return list(self.items)


# /****
# Cache simple de entidades consultadas por tabla e ID.
# Reduce consultas repetidas durante la ejecucion del menu.
# ****/
class EntityCache:
    def __init__(self):
        self.items = {}

    def set(self, table, entity_id, value):
        self.items[(table, entity_id)] = value

    def get(self, table, entity_id):
        return self.items.get((table, entity_id))

    def remove(self, table, entity_id):
        self.items.pop((table, entity_id), None)
