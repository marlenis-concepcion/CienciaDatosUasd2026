from src.repositories import ActorRepository


class ActorService:
    def __init__(self, db):
        self.repository = ActorRepository(db)

    def create_actor(self, first_name, last_name):
        self._validate_name(first_name, last_name)
        return self.repository.create(
            {"first_name": first_name.strip().upper(), "last_name": last_name.strip().upper()}
        )

    def update_actor(self, actor_id, first_name, last_name):
        self._validate_name(first_name, last_name)
        return self.repository.update(
            actor_id,
            {"first_name": first_name.strip().upper(), "last_name": last_name.strip().upper()},
        )

    def find_actor(self, actor_id):
        return self.repository.find_by_id(actor_id)

    def list_actors(self, limit=10):
        return self.repository.find_all(limit)

    def delete_actor(self, actor_id):
        return self.repository.delete(actor_id)

    @staticmethod
    def _validate_name(first_name, last_name):
        if not first_name or not last_name:
            raise ValueError("El nombre y el apellido son obligatorios.")
