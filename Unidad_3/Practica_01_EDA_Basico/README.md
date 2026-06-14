# Práctica 01: Análisis Exploratorio de Datos (EDA) Básico

## Objetivos

1. Cargar y explorar datasets
2. Limpiar datos y manejar valores faltantes
3. Generar estadísticas descriptivas
4. Crear visualizaciones exploratorias
5. Documentar hallazgos principales

## Estructura del Proyecto

```
Practica_01_EDA_Basico/
├── README.md
├── notebooks/
│   └── eda_basico.ipynb
├── data/
│   └── (datasets de entrada)
├── outputs/
│   ├── figuras/
│   └── reportes/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── cleaning.py
│   └── visualization.py
└── requirements.txt
```

## Requisitos

- Python 3.8+
- pandas, numpy, matplotlib, seaborn, plotly
- jupyter (para notebook)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Notebook interactivo

```bash
jupyter notebook notebooks/eda_basico.ipynb
```

### Opción 2: Script

```bash
python src/data_loader.py
python src/cleaning.py
python src/visualization.py
```

## Entregables

- Notebook con análisis paso a paso
- Figuras en `outputs/figuras/`
- Reporte en `outputs/reportes/analisis_eda.txt`
- Código limpio en `src/`

## Criterios de Evaluación

| Componente | Puntuación |
|-----------|-----------|
| Carga y exploración de datos | 2 pts |
| Limpieza de datos | 2 pts |
| Estadísticas descriptivas | 2 pts |
| Visualizaciones | 2 pts |
| Documentación | 2 pts |
| **Total** | **10 pts** |

## Notas Importantes

- Documentar cada paso del análisis
- Justificar decisiones de limpieza
- Usar visualizaciones claras y etiquetadas
- Incluir código reproducible
