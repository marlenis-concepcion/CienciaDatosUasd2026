USE sakila;

-- Consultas que tambien se ejecutan desde Python en `basic_crud.py`.

SELECT country_id, country, last_update
FROM country
ORDER BY country
LIMIT 10;

SELECT c.city_id, c.city, co.country
FROM city c
INNER JOIN country co ON c.country_id = co.country_id
ORDER BY c.city
LIMIT 10;

SELECT f.film_id, f.title, COUNT(i.inventory_id) AS copies
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id, f.title
ORDER BY copies DESC, f.title
LIMIT 10;

