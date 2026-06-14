# Práctica 02: Análisis Estadístico Inferencial

## Objetivos

1. Formular hipótesis estadísticas
2. Realizar pruebas paramétricas y no paramétricas
3. Evaluar correlaciones y asociaciones
4. Interpretar intervalos de confianza
5. Comunicar resultados inferenciales

## Estructura del Proyecto

```
Practica_02_Analisis_Estadistico/
├── README.md
├── notebooks/
│   └── analisis_inferencial.ipynb
├── data/
│   └── (datasets de entrada)
├── outputs/
│   ├── figuras/
│   ├── tablas/
│   └── reportes/
├── src/
│   ├── __init__.py
│   ├── hypothesis_tests.py
│   ├── correlations.py
│   └── effect_sizes.py
└── requirements.txt
```

## Pruebas Estadísticas

### Pruebas Paramétricas
- T-test (muestras independientes y pareadas)
- ANOVA
- Regresión lineal simple y múltiple

### Pruebas No Paramétricas
- Mann-Whitney U
- Kruskal-Wallis
- Spearman y Kendall

### Análisis Multivariado
- Correlación de Pearson y Spearman
- Matriz de correlación
- Análisis de componentes principales (PCA)

## Requisitos

```bash
pip install -r requirements.txt
```

Paquetes clave:
- scipy (pruebas estadísticas)
- statsmodels (modelos estadísticos)
- scikit-learn (PCA, escalado)

## Ejecución

```bash
jupyter notebook notebooks/analisis_inferencial.ipynb
```

## Entregables

- Notebook con análisis paso a paso
- Tablas de resultados en `outputs/tablas/`
- Gráficos en `outputs/figuras/`
- Reporte de hallazgos en `outputs/reportes/`

## Criterios de Evaluación

| Componente | Puntuación |
|-----------|-----------|
| Formulación de hipótesis | 2 pts |
| Selección de pruebas | 2 pts |
| Ejecución correcta | 2 pts |
| Interpretación de resultados | 2 pts |
| Documentación y presentación | 2 pts |
| **Total** | **10 pts** |

## Guía de Hipótesis

### Paso 1: Definir hipótesis nula (H₀) y alternativa (H₁)
- H₀: No hay diferencia / No hay relación
- H₁: Hay diferencia / Hay relación

### Paso 2: Establecer nivel de significancia
- α = 0.05 (estándar)
- Reportar p-valor

### Paso 3: Interpretar resultados
- Si p < α: rechazar H₀
- Si p ≥ α: no rechazar H₀

### Paso 4: Reportar tamaño del efecto
- Cohen's d, r, η² según corresponda
