from src.metrics import covariance, descriptive_metrics


def film_metric_report(db):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT length, rental_rate, replacement_cost
            FROM film
            WHERE length IS NOT NULL
            """
        )
        rows = cursor.fetchall()

    lengths = [row["length"] for row in rows]
    rental_rates = [row["rental_rate"] for row in rows]
    replacement_costs = [row["replacement_cost"] for row in rows]

    return {
        "length": descriptive_metrics(lengths),
        "rental_rate": descriptive_metrics(rental_rates),
        "replacement_cost": descriptive_metrics(replacement_costs),
        "covariance_length_rental_rate": covariance(lengths, rental_rates),
        "covariance_length_replacement_cost": covariance(lengths, replacement_costs),
    }

