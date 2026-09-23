USE sakila;

-- Ejecutar despues de revisar duplicados. Si existen duplicados, limpiar primero.

SELECT country, COUNT(*) AS duplicates
FROM country
GROUP BY country
HAVING COUNT(*) > 1;

SELECT country_id, city, COUNT(*) AS duplicates
FROM city
GROUP BY country_id, city
HAVING COUNT(*) > 1;

SELECT title, release_year, language_id, COUNT(*) AS duplicates
FROM film
GROUP BY title, release_year, language_id
HAVING COUNT(*) > 1;

SELECT film_id, store_id, COUNT(*) AS copies
FROM inventory
GROUP BY film_id, store_id
HAVING COUNT(*) > 10;

ALTER TABLE country
ADD CONSTRAINT uq_country_name UNIQUE (country);

ALTER TABLE city
ADD CONSTRAINT uq_city_country UNIQUE (country_id, city);

ALTER TABLE film
ADD CONSTRAINT uq_film_title_year_language UNIQUE (title, release_year, language_id);

-- Esta restriccion es deliberadamente mas conservadora: evita duplicar el mismo
-- registro de inventario si el equipo crea datos de prueba. Sakila permite
-- multiples copias por tienda, por eso se recomienda validar antes de aplicar.
-- ALTER TABLE inventory
-- ADD CONSTRAINT uq_inventory_film_store UNIQUE (film_id, store_id);

