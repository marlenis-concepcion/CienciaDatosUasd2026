# Dataset Card · MovieLens

## Fuente, fecha, versión y hash
- MovieLens `ml-latest-small`, GroupLens Research (Universidad de Minnesota): https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
- Según su README: 100 836 valoraciones y 3683 etiquetas de 610 usuarios sobre 9742 películas, entre el 29 de marzo de 1996 y el 24 de septiembre de 2018; generado el 26 de septiembre de 2018.
- SHA-256 del ZIP descargado el 23 de septiembre de 2026: `696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436` (`ratings.csv`: `aa289ca8…352646`; `movies.csv`: `5a5f32dd…11aa07`).

## Licencia y cita
Uso para investigación bajo las condiciones del README de GroupLens: no implicar respaldo de la Universidad de Minnesota, citar el dataset y no usarlo con fines comerciales sin permiso. Siguiendo el mandato, **el dataset no se redistribuye**: `data/` está excluido de Git y cada persona lo descarga con el script.

Harper, F. M. y Konstan, J. A. (2015). The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems*, 5(4), 19:1–19:19. https://doi.org/10.1145/2827872

## Archivos y diccionario
| Archivo | Columna | Tipo | Descripción |
|---|---|---|---|
| `ratings.csv` | `userId` | entero | Usuario anonimizado |
| | `movieId` | entero | Película |
| | `rating` | decimal | 0.5 a 5.0 en pasos de 0.5 |
| | `timestamp` | entero | Segundos desde 1970 (UTC) |
| `movies.csv` | `movieId` | entero | Película |
| | `title` | texto | Título con año |
| | `genres` | texto | Géneros separados por `|` |

`links.csv` y `tags.csv` no se usan.

## Procedimiento de descarga
`uv run python scripts/download_data.py` descarga el ZIP, valida que no tenga rutas inseguras, lo extrae en `data/raw/ml-latest-small/` y compara el SHA-256 con el registrado; si no coincide, termina con error.

## Población observada y exclusiones
- 610 usuarios elegidos al azar por GroupLens entre quienes valoraron al menos 20 películas (mínimo observado: 20; mediana: 70.5; máximo: 2698). No hay datos demográficos.
- 9724 de las 9742 películas tienen al menos una valoración; 3446 tienen solo una. 34 películas no tienen género.
- Densidad de la matriz usuario-película: 1.7 %.
- Sin nulos ni pares usuario-película duplicados.

## Calidad, sesgos y usos prohibidos
- Popularidad concentrada: el 10 % de películas más valoradas reúne el 60 % de las valoraciones, lo que favorece a los modelos que recomiendan lo popular.
- Escala sesgada hacia arriba: 4.0 es el valor más frecuente (26 818) y 3.0 el segundo.
- Usuarios muy activos pesan mucho más que el resto; los usuarios con menos de 20 valoraciones no están representados.
- No debe usarse para decisiones comerciales, para inferir datos personales ni para afirmar gustos de poblaciones distintas a los usuarios de MovieLens.
