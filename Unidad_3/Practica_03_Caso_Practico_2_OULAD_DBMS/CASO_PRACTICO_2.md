# Caso Práctico 2: Análisis OULAD en Base de Datos (20 puntos)

**Asignatura:** INF-8237-C2 Ciencia de Datos I  
**Facilitador:** Dr. Silverio del Orbe Abad  
**Equipo:** McCarthy Team  
**Fecha de Entrega:** 20 de junio de 2026

## Descripción General

Exportación e integración del dataset OULAD (Open University Learning Analytics Dataset) a una base de datos relacional, seguido de un análisis exploratorio extendido, modelado estadístico y redacción de un artículo científico con hallazgos.

## Componentes Evaluados

### 1. Montar OULAD en un DBMS (2 puntos)

#### Entregables:
- ✓ **Script DDL (SQL):** `sql/01_schema_oulad.sql`
  - Tablas dimensionales: courses, modules, assessments, vle
  - Tablas de hechos: student_info, student_assessment, student_vle
  - Restricciones de integridad: PK y FK
  - Campos ordinales para categorías (gender_ordinal, education_ordinal, etc.)
  - Índices para optimización

- ✓ **FullDomain Tables:**
  - `fulldomaine_assessment`: Agregación detallada de evaluaciones por estudiante
  - `fulldomaine_vle`: Agregación detallada de actividades VLE
  - `student_progress_weekly`: Seguimiento semanal de progreso

- ✓ **Vistas SQL:** v_student_summary, v_assessment_statistics, v_vle_engagement

#### Base de Datos Soportada:
- PostgreSQL (recomendado por robustez)
- MySQL
- MS SQL Server

---

### 2. ETL Bien Orquestado y Encapsulación (2 puntos)

#### Estructura ETL:

```
etl_orchestrator.py
├── Step 1: Download OULAD from UCI
├── Step 2: Initialize PostgreSQL schema
├── Step 3: Load data with ordinal encoding
├── Step 4: Create FullDomain aggregations
└── Step 5-6: EDA and reporting
```

#### Módulos Principales:

**`src/db_loader.py`** - PostgreSQL ETL
- `PostgreSQLLoader`: Clase encapsuladora con pool de conexiones
- Métodos: `load_courses()`, `load_student_info()`, `load_assessments()`, etc.
- Ordinal encoding automático
- Logging de cada operación
- Manejo de errores y rollback

**`etl_orchestrator.py`** - Orquestación
- Pipeline paso a paso
- Manejo de dependencias
- Reportes de ejecución

#### Ejecución:
```bash
python etl_orchestrator.py
```

---

### 3. EDA Extendido (10 puntos)

#### Visualizaciones Generadas:

| # | Tipo | Archivo | Descripción |
|---|------|---------|-------------|
| 1 | Histograma | `distributions_univariate.png` | Distribuciones univariadas de variables numéricas |
| 2 | Gaussian | `gaussian_distributions.png` | Ajuste normal (campana de Gauss) |
| 3 | Boxplot | `boxplots.png` | Comparación por grupos (caja y bigotes) |
| 4 | Correlación | `correlation_matrix.png` | Heatmap de correlaciones de Pearson |
| 5 | Dispersión | `scatter_matrix.png` | Gráficos de dispersión pairwise |
| 6 | Categorías | `categorical_distributions.png` | Distribuciones de variables categóricas |
| 7 | Faltantes | `missing_data_heatmap.png` | Patrones de datos faltantes |
| 8 | Confusión | `confusion_matrices.png` | Matrices de confusión (si aplica) |

#### Análisis Estadísticos:

**CSV Generados:**
- `summary_statistics.csv` - Descriptiva: count, mean, std, min, max, median, skew, kurtosis
- `descriptive_statistics.csv` - Estadísticas extendidas por variable
- `correlation_matrix.csv` - Matriz de correlaciones
- `correlation_tests.csv` - Pruebas de significancia (r, p-value)
- `anova_results.csv` - ANOVA F-statistic y p-values

#### Métricas Calculadas:
- Media, mediana, moda, desviación estándar
- Asimetría (skewness) y curtosis (kurtosis)
- Rango intercuartílico (IQR)
- Coeficiente de variación (CV)
- Correlaciones de Pearson y Spearman

#### Módulo Principal:
**`src/eda_extended.py`** - Clase `ExtendedEDA`
```python
eda = ExtendedEDA(df, output_dir)
eda.run_all_eda()  # Genera todas las visualizaciones
```

---

### 4. Artículo Científico (6 puntos)

#### Formato APA 7 - UASD Standard

**Estructura (máx 10 páginas a doble espacio):**

1. **Carátula**
   - Título, autores, institución, fecha

2. **Resumen (Abstract)** - 150-200 palabras
   - Objetivo, método, resultados principales, conclusiones
   - Palabras clave (5-7)

3. **Introducción**
   - Contexto del problema
   - Relevancia de aprendizaje en línea
   - Hipótesis y preguntas de investigación

4. **Revisión de Literatura**
   - Minería de datos educativa
   - Predictores de desempeño académico
   - Estado del arte

5. **Metodología**
   - Descripción de datos OULAD (32,593 estudiantes)
   - Limpieza y preparación (campos ordinales)
   - Técnicas de análisis (EDA, ANOVA, correlación)

6. **Resultados**
   - Estadísticas descriptivas principales
   - Hallazgos de análisis de correlación
   - Resultados de pruebas de hipótesis
   - Visualizaciones clave (3-4 gráficos)

7. **Conclusiones y Recomendaciones**
   - Respuesta a hipótesis
   - Implicaciones prácticas
   - Limitaciones
   - Investigaciones futuras

8. **Referencias** (mínimo 10 fuentes)

#### Archivo Generado:
```
docs/Articulo_Cientifico_OULAD_APA7.docx
```

**Generador:** `scripts/generate_apa_paper.py`
```bash
python scripts/generate_apa_paper.py
```

---

## Evidencia de Trabajo Colaborativo (Requerido)

El artículo debe incluir **enlace o video** demostrando trabajo en equipo:

### Opciones:
- 📹 **Video de reunión:** Captura de pantalla de video conferencia (Zoom, Google Meet) con integrantes
- 📸 **Screenshot ambiente colaborativo:** GitHub collaboration, Google Colab compartido con comentarios
- 🔗 **GitHub Collaboration Link:** Commits conjuntos, pull requests con reviews
- 📊 **Google Colab Notebook:** Compartido con permisos de edición a integrantes

### Formato en Documento:
> **Evidencia de Colaboración:**  
> [Enlace a video] o  
> [Screenshot del ambiente colaborativo]  
> 
> Integrantes: [Nombre 1], [Nombre 2], [Nombre 3]  
> Roles: [Rol de cada integrante]

---

## Estructura de Carpetas

```
Practica_04_Proyecto_Final_OULAD/
├── README.md                          # Proyecto principal
├── CASO_PRACTICO_2.md                 # Este archivo
├── etl_orchestrator.py                # Script principal de orquestación
├── sql/
│   └── 01_schema_oulad.sql            # DDL para PostgreSQL
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py                        # Carga de OULAD
│   ├── db_loader.py                   # ETL a PostgreSQL
│   ├── eda_extended.py                # Análisis exploratorio
│   ├── features.py                    # Ingeniería de características
│   └── pipeline.py                    # Pipeline general
├── scripts/
│   ├── generate_apa_paper.py          # Generador de paper APA
│   └── other scripts...
├── notebooks/
│   └── Proyecto_Final_OULAD_Colab.ipynb
├── docs/
│   ├── Articulo_Cientifico_OULAD_APA7.docx  # Paper final
│   └── other docs...
├── outputs/
│   ├── figures/                       # Gráficos PNG
│   │   ├── distributions_univariate.png
│   │   ├── gaussian_distributions.png
│   │   ├── correlation_matrix.png
│   │   ├── boxplots.png
│   │   ├── scatter_matrix.png
│   │   ├── categorical_distributions.png
│   │   ├── missing_data_heatmap.png
│   │   └── confusion_matrices.png
│   ├── csv/                           # Datos tabulares
│   │   ├── summary_statistics.csv
│   │   ├── correlation_matrix.csv
│   │   ├── correlation_tests.csv
│   │   ├── anova_results.csv
│   │   └── eda_report.txt
│   └── data/
│       └── oulad.zip                  # Descargado automáticamente
├── tests/
│   ├── test_outputs.py
│   └── test_*.py
└── requirements.txt                   # Dependencias Python
```

---

## Requisitos Técnicos

### Software:
- **Python 3.8+**
- **PostgreSQL 12+** o MySQL 8.0+ o MS SQL Server 2019+
- **Git** para colaboración

### Dependencias Python:
```bash
pip install -r requirements.txt
```

**Paquetes principales:**
- pandas, numpy
- scikit-learn, scipy, statsmodels
- matplotlib, seaborn, plotly
- psycopg2 (PostgreSQL)
- python-docx (generación de reportes)

---

## Instrucciones de Ejecución

### 1. Preparación del Ambiente

```bash
# Clonar repositorio
git clone https://github.com/marlenis-concepcion/CienciaDatosUasd2026.git
cd CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD

# Crear ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

```bash
# Crear base de datos
createdb oulad_uasd

# Optionally, crear usuario
createuser -P datasci  # Ingresa contraseña
```

### 3. Ejecutar ETL Completo

```bash
# Modo automático (descarga, carga, EDA, paper)
python etl_orchestrator.py

# Modo sin PostgreSQL (testing)
python etl_orchestrator.py --skip-postgres
```

### 4. Ejecución Individual de Pasos

```bash
# Solo EDA (si datos ya cargados)
python -c "from src.eda_extended import ExtendedEDA; from src.data import OULADRepository; eda = ExtendedEDA(...); eda.run_all_eda()"

# Solo generar paper
python scripts/generate_apa_paper.py
```

### 5. Uso en Google Colab

```python
# En Colab notebook
!git clone https://github.com/marlenis-concepcion/CienciaDatosUasd2026.git
%cd CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD
!pip install -r requirements.txt

# Ejecutar (sin PostgreSQL en Colab)
!python etl_orchestrator.py --skip-postgres
```

---

## Rúbrica de Evaluación

| # | Componente | Excelente | Cumple | Parcial | No Cumple |
|---|-----------|-----------|---------|---------|-----------|
| 1 | **DBMS (2 pts)** | Schema DDL completo con DER | Schema con PK, FK | Schema incompleto | Sin schema |
| 2 | **ETL (2 pts)** | Encapsulado, limpieza, ordinales | Carga básica funcional | Carga parcial | Falla |
| 3 | **EDA (10 pts)** | 8+ tipos gráficos, tests estadísticos | 5-7 gráficos, análisis básico | 3-4 gráficos | 0-2 gráficos |
| 4 | **Paper (6 pts)** | Estructura APA completa, hallazgos | Estructura OK, resultados claros | Falta secciones | Incompleto |
| | **TOTAL** | **20** | **12.25** | **8** | **0** |

---

## Entrega Final

### Requisitos:
- ✓ Archivo .docx o .odt editable con paper APA
- ✓ Enlace a GitHub o archivo .zip/.rar con código
- ✓ Evidencia de colaboración (video/screenshot)
- ✓ Carpeta outputs/ con todos los archivos generados

### Links de Entrega:
- **Paper:** Documento APA en aula virtual
- **Código:** GitHub link o ZIP descargable
- **Evidencia:** Video/screenshot adjunto en documento

---

## Recomendaciones

1. **Realizar commits diarios** a GitHub para evidenciar colaboración
2. **Documentar decisiones** en comentarios y docstrings
3. **Validar datos** con test suite antes de análisis
4. **Generar múltiples visualizaciones** para cada aspecto
5. **Incluir interpretaciones** en cada resultado estadístico
6. **Revisar formato APA** antes de entregar (márgenes, espaciado, referencias)

---

## Contacto y Soporte

- **Facilitador:** Dr. Silverio del Orbe Abad
- **Repositorio:** https://github.com/marlenis-concepcion/CienciaDatosUasd2026
- **Documentación del proyecto:** README.md principal

---

**Última actualización:** 14 de junio de 2026  
**Estado:** En progreso - Deadline: 20 de junio de 2026
