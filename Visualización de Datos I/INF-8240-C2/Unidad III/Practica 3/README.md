# Unidad III · Prácticas Power BI, Tableau y Python

**Materia:** Visualización de Datos I · INF-8240-C2 · UASD
**Estudiante:** Marlenis Judith Concepción Cuevas
**Empresa:** Industrias Caribe S.A.

La consigna está en [Consigna_Unidad_III.pdf](Consigna_Unidad_III.pdf). Permite resolver las prácticas con una sola herramienta. Esta entrega usa **Python** (pandas, matplotlib y seaborn).

**GitHub:** [CienciaDatosUasd2026 / Unidad III / Practica 3](https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Visualizaci%C3%B3n%20de%20Datos%20I/INF-8240-C2/Unidad%20III/Practica%203)

## Entregables

| Archivo | Contenido |
|---|---|
| [Informe_Ejecutivo_Unidad_III.docx](Informe_Ejecutivo_Unidad_III.docx) / [.pdf](Informe_Ejecutivo_Unidad_III.pdf) | Informe ejecutivo de dos páginas: indicadores, dashboard, hallazgos, conclusiones y recomendaciones |
| [Practica_Reclamos/reclamos_dashboard.py](Practica_Reclamos/reclamos_dashboard.py) | Práctica 1, guiada: clase `AnalizadorReclamos` y dashboard |
| `Practica_Reclamos/Dashboard_Reclamos.png` | Dashboard de reclamos |
| [Practica_Produccion/produccion_dashboard.py](Practica_Produccion/produccion_dashboard.py) | Práctica 2, independiente: exploración, clase `AnalizadorProduccion`, dashboard y preguntas gerenciales |
| `Practica_Produccion/Dashboard_Produccion.png` | Dashboard de producción |
| [dashboard_web/app.py](dashboard_web/app.py), `Dockerfile`, `docker-compose.yml` | Dashboard web interactivo con filtros (Docker) |
| [Consigna_Unidad_III.pdf](Consigna_Unidad_III.pdf) | Consigna del profesor |
| [generar_informe.py](generar_informe.py) | Genera el informe Word con las cifras calculadas por las dos clases |

## Práctica 1 · Gestión de reclamos

Se siguen los pasos 1 a 6 de la guía. Además se agregan:

- Tarjetas con los cinco indicadores.
- Etiquetas de mes con año, para que enero de 2025 y enero de 2026 aparezcan por separado.
- Filtros `--region` y `--prioridad`, equivalentes a los segmentadores.

Valores de control comprobados:

| Indicador | Resultado |
|---|---|
| Total de reclamos | 450 |
| Resueltos | 318 (70.67%) |
| En proceso | 78 |
| Abiertos | 54 |
| Tiempo promedio de resolución | 8.94 días |
| Satisfacción promedio | 3.08/5 |

El tiempo promedio y la satisfacción se calculan solo sobre los reclamos resueltos. Los 132 vacíos de `DiasResolucion` y `Satisfaccion_1a5` se conservan como nulos: no se convierten en cero ni se eliminan.

### Explicación de la clase (Paso 3)

- **`__init__`** es el constructor. Python lo ejecuta automáticamente al crear el objeto con `AnalizadorReclamos(df)` y recibe el DataFrame como parámetro.
- **`self.df`** es un atributo del objeto. El constructor guarda en él los datos para que todos los métodos trabajen sobre la misma tabla sin volver a recibirla. `self` representa al propio objeto.
- **Métodos:**
  - `total_reclamos()` cuenta los `ReclamoID` únicos.
  - `reclamos_resueltos()` filtra `Estado == "Resuelto"` antes de contar.
  - `porcentaje_resolucion()` divide resueltos entre total y devuelve 0 si el total es cero, para evitar una división entre cero.
  - `reclamos_por_categoria()` agrupa por `Categoria` y ordena de mayor a menor.
  - Los métodos añadidos (`reclamos_por_estado`, `reclamos_por_region`, `evolucion_mensual`, `dias_promedio_resolucion` y `satisfaccion_promedio`) siguen la misma idea.

## Práctica 2 · Control y eficiencia de producción

El script responde cada parte de la consigna:

- **A. Exploración:** 1,200 lotes de enero a diciembre de 2025, sin nulos ni lotes duplicados. Hay 419 lotes que superan su plan; se conservan porque son datos válidos.
- **B. Indicadores:** se calculan con la clase `AnalizadorProduccion`.
- **C. Visualizaciones obligatorias:** el dashboard incluye las seis.
- **D. Preguntas gerenciales:** el script imprime las respuestas.

Las tasas son razones de sumas, no promedios de las tasas de cada lote. Los filtros `--planta`, `--turno` y `--producto` funcionan como segmentadores.

| Indicador | Resultado 2025 |
|---|---|
| Producción total | 1,024,428 |
| Producción planificada | 1,081,535 |
| Cumplimiento del plan | 94.72% |
| Tasa de defectos | 3.43% |
| Costo total | RD$29,683,070.72 |
| Costo por unidad producida | RD$28.98 |

### Fórmulas equivalentes en Power BI y Tableau (referencia)

Solo se exige una herramienta. Estas fórmulas permiten reproducir los mismos indicadores en las otras dos.

```DAX
Produccion Total = SUM(IndustriasCaribe_Produccion[UnidadesProducidas])
Produccion Planificada = SUM(IndustriasCaribe_Produccion[UnidadesPlanificadas])
Cumplimiento Plan = DIVIDE([Produccion Total], [Produccion Planificada], 0)
Tasa Defectos = DIVIDE(SUM(IndustriasCaribe_Produccion[UnidadesDefectuosas]), [Produccion Total], 0)
Costo Total = SUM(IndustriasCaribe_Produccion[CostoProduccion_DOP])
Costo por Unidad = DIVIDE([Costo Total], [Produccion Total], 0)
```

```
// Tableau: campos calculados
Cumplimiento Plan = SUM([UnidadesProducidas]) / SUM([UnidadesPlanificadas])
Tasa Defectos     = SUM([UnidadesDefectuosas]) / SUM([UnidadesProducidas])
Costo por Unidad  = SUM([CostoProduccion_DOP]) / SUM([UnidadesProducidas])
```

## Reproducir

Desde esta carpeta, con Python 3.9 o posterior:

```sh
python -m pip install -r requirements.txt
cd Practica_Reclamos && python reclamos_dashboard.py && cd ..
cd Practica_Produccion && python produccion_dashboard.py && cd ..
python generar_informe.py
```

Cada carpeta incluye una copia sin cambios de su CSV, como pide la guía ("copiar el CSV"). Fuente: consigna y CSV de UASDVirtual. Escudo UASD tomado de la Unidad I (Wikimedia Commons, CC BY-SA 4.0). Trabajo preparado con apoyo de programación e IA, sujeto a la revisión de la estudiante antes de entregar.

## Dashboard web interactivo con Docker

Power BI Desktop solo existe para Windows y no se puede ejecutar en Docker sobre una Mac. Tableau Desktop tampoco tiene imagen de Docker; para Mac se instala directamente. Como alternativa, [dashboard_web/app.py](dashboard_web/app.py) publica los dos dashboards en el navegador con Streamlit y Plotly. Tiene filtros en la barra lateral que funcionan como segmentadores y reutiliza las mismas clases, por eso las cifras coinciden con las de los PNG y el informe.

Con Docker Desktop abierto, desde esta carpeta:

```sh
./abrir_dashboard.sh    # inicia Docker si hace falta, construye y abre http://localhost:8501
./cerrar_dashboard.sh   # detiene el dashboard cuando termines
```

No ejecutes los dos scripts a la vez: el segundo apaga el dashboard.
