def create_country(db, country):
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO country(country, last_update) VALUES (%s, NOW())", (country,))
        return cursor.lastrowid


def read_countries(db, limit=10):
    with db.cursor() as cursor:
        cursor.execute("SELECT country_id, country, last_update FROM country ORDER BY country LIMIT %s", (limit,))
        return cursor.fetchall()


def update_country(db, country_id, country):
    with db.cursor() as cursor:
        cursor.execute(
            "UPDATE country SET country = %s, last_update = NOW() WHERE country_id = %s",
            (country, country_id),
        )
        return cursor.rowcount


def delete_country(db, country_id):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM country WHERE country_id = %s", (country_id,))
        return cursor.rowcount


def read_cities(db, limit=10):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.city_id, c.city, co.country
            FROM city c
            INNER JOIN country co ON c.country_id = co.country_id
            ORDER BY c.city
            LIMIT %s
            """,
            (limit,),
        )
        return cursor.fetchall()


def read_films_inventory(db, limit=10):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT f.film_id, f.title, COUNT(i.inventory_id) AS copies
            FROM film f
            LEFT JOIN inventory i ON f.film_id = i.film_id
            GROUP BY f.film_id, f.title
            ORDER BY copies DESC, f.title
            LIMIT %s
            """,
            (limit,),
        )
        return cursor.fetchall()

