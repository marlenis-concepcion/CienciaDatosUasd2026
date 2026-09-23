USE sakila;

-- 1. Listado de paises.
SELECT country_id, country, last_update
FROM country
ORDER BY country;

-- 2. Ciudades con su pais.
SELECT c.city_id, c.city, co.country
FROM city c
INNER JOIN country co ON c.country_id = co.country_id
ORDER BY co.country, c.city;

-- 3. Peliculas con idioma.
SELECT f.film_id, f.title, l.name AS language_name, f.release_year
FROM film f
INNER JOIN language l ON f.language_id = l.language_id
ORDER BY f.title;

-- 4. Inventario por pelicula.
SELECT f.film_id, f.title, COUNT(i.inventory_id) AS inventory_count
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id, f.title
ORDER BY inventory_count DESC, f.title;

-- 5. Peliculas por categoria.
SELECT c.name AS category, COUNT(fc.film_id) AS total_films
FROM category c
INNER JOIN film_category fc ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY total_films DESC;

-- 6. Duracion promedio de peliculas por rating.
SELECT rating, AVG(length) AS avg_length, MIN(length) AS min_length, MAX(length) AS max_length
FROM film
WHERE length IS NOT NULL
GROUP BY rating
ORDER BY avg_length DESC;

-- 7. Renta e inventario por tienda.
SELECT s.store_id, COUNT(i.inventory_id) AS inventory_items
FROM store s
LEFT JOIN inventory i ON s.store_id = i.store_id
GROUP BY s.store_id;

-- 8. Clientes por ciudad y pais.
SELECT co.country, c.city, COUNT(cu.customer_id) AS customers
FROM customer cu
INNER JOIN address a ON cu.address_id = a.address_id
INNER JOIN city c ON a.city_id = c.city_id
INNER JOIN country co ON c.country_id = co.country_id
GROUP BY co.country, c.city
ORDER BY customers DESC;

-- 9. Top 10 peliculas mas rentadas.
SELECT f.title, COUNT(r.rental_id) AS rentals
FROM rental r
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY rentals DESC
LIMIT 10;

-- 10. Metricas SQL fundamentales para peliculas.
SELECT
    AVG(length) AS mean_length,
    MAX(length) - MIN(length) AS range_length,
    VAR_POP(length) AS variance_length,
    STDDEV_POP(length) AS stddev_length,
    AVG(rental_rate) AS mean_rental_rate
FROM film
WHERE length IS NOT NULL;

