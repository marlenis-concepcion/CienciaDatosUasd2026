import csv
import json


def export_to_csv(entities, path):
    rows = [entity.to_dict() for entity in entities]
    if not rows:
        return 0

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def import_from_csv(entity_type, path):
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [entity_type.from_dict(row) for row in reader]


def export_to_json(entities, path):
    rows = [entity.to_dict() for entity in entities]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2, default=str)
    return len(rows)


def import_from_json(entity_type, path):
    with open(path, encoding="utf-8") as file:
        rows = json.load(file)
    return [entity_type.from_dict(row) for row in rows]

