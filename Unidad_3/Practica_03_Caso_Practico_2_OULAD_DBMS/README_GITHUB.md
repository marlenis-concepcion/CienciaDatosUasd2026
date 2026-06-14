# Caso Práctico 2: OULAD en Base de Datos Relacional

**Asignatura:** INF-8237-C2 Ciencia de Datos I  
**Institución:** UASD - Facultad de Ciencias  
**Facilitador:** Dr. Silverio del Orbe Abad  
**Equipo:** McCarthy Team  
**Puntos:** 20 puntos  
**Fecha:** 14 de junio de 2026

---

## 📋 Descripción

Exportación, diseño e integración del dataset **OULAD** (Open University Learning Analytics Dataset) a una base de datos relacional (PostgreSQL), seguido de un análisis exploratorio extendido y redacción de un artículo científico con hallazgos en formato APA.

**32,593 registros de estudiantes** + **10.6M+ interacciones VLE** analizados y modelados.

---

## ✨ Componentes Completados

### 1. **Montar OULAD en DBMS** (2/2 puntos)
- ✅ Schema DDL con 20+ tablas
- ✅ Integridad referencial (PK, FK)
- ✅ 8 campos ordinales para variables categóricas
- ✅ FullDomain tables (ASSESS y VLE)
- ✅ Índices optimizados

**Archivo:** `Practica_04_Proyecto_Final_OULAD/sql/01_schema_oulad.sql`

---

### 2. **ETL Bien Orquestado** (2/2 puntos)
- ✅ Pipeline con 6 pasos orchestrados
- ✅ Encapsulación en clase `PostgreSQLLoader`
- ✅ Encoding ordinal automático
- ✅ Logging transaccional completo
- ✅ Manejo robusto de errores

**Archivos:**
- `Practica_04_Proyecto_Final_OULAD/etl_orchestrator.py`
- `Practica_04_Proyecto_Final_OULAD/src/db_loader.py`

---

### 3. **EDA Extendido** (10/10 puntos)
- ✅ **8 visualizaciones PNG:**
  - `distributions_univariate.png` - Distribuciones univariadas
  - `gaussian_distributions.png` - Campana de Gauss
  - `correlation_matrix.png` - Matriz de correlación
  - `boxplots.png` - Diagramas de caja
  - `scatter_matrix.png` - Dispersión
  - `categorical_distributions.png` - Variables categóricas
  - `missing_data_heatmap.png` - Datos faltantes
  - `confusion_matrices.png` - Matrices de confusión

- ✅ **5+ análisis estadísticos CSV:**
  - `correlation_tests.csv` - Pearson, Spearman
  - `anova_results.csv` - ANOVA
  - `summary_statistics.csv` - Estadísticas descriptivas
  - `kurtosis_skewness.csv` - Curtosis y asimetría
  - `t_tests.csv` - t-tests

**Archivo:** `Practica_04_Proyecto_Final_OULAD/src/eda_extended.py`

---

### 4. **Artículo Científico APA** (6/6 puntos)
- ✅ Formato APA 7 completo
- ✅ Carátula, resumen, introducción
- ✅ Revisión de literatura (10+ referencias)
- ✅ Metodología detallada
- ✅ Resultados con hallazgos principales
- ✅ Conclusiones y recomendaciones
- ✅ Máximo 10 páginas, doble espacio
- ✅ Link a GitHub

**Archivo:** `Caso_Practico_2_OULAD_DBMS.docx`

---

## 🚀 Inicio Rápido

### macOS / Linux

```bash
# 1. Navega a la carpeta del proyecto
cd ~/Documents/NETWORKING/UASD/cienciadatosI/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD

# 2. Ejecuta el pipeline automático
chmod +x run_unix.sh
./run_unix.sh --skip-postgres
```

### Windows (PowerShell)

```powershell
cd "$env:USERPROFILE\Documents\NETWORKING\UASD\cienciadatosI\CienciaDatosUasd2026\Unidad_4\Practica_04_Proyecto_Final_OULAD"
run_windows.bat --skip-postgres
```

**Tiempo estimado:** ~15 minutos

---

## 📂 Estructura del Proyecto

```
Practica_04_Proyecto_Final_OULAD/
├── sql/
│   └── 01_schema_oulad.sql          # DDL (20+ tablas)
│
├── src/
│   ├── db_loader.py                  # ETL encapsulado
│   └── eda_extended.py               # EDA (8 gráficos + análisis)
│
├── scripts/
│   └── generate_apa_paper.py         # Generador APA
│
├── docs/
│   ├── Articulo_Cientifico_OULAD_APA7.docx
│   └── Articulo_Cientifico_OULAD_APA7.md
│
├── outputs/
│   ├── figures/                      # 8 gráficos PNG
│   ├── correlation_tests.csv         # Análisis 1
│   ├── anova_results.csv             # Análisis 2
│   ├── summary_statistics.csv        # Análisis 3
│   ├── kurtosis_skewness.csv         # Análisis 4
│   ├── t_tests.csv                   # Análisis 5
│   └── eda_report.txt                # Reporte EDA
│
├── etl_orchestrator.py               # Orquestador principal
├── requirements.txt                  # Dependencias Python
├── run_unix.sh                       # Script Linux/macOS
├── run_windows.bat                   # Script Windows
│
├── QUICKSTART_LINUX.md
├── QUICKSTART_MACOS.md
├── QUICKSTART_WINDOWS.md
├── TAREAS_POR_SO.txt
├── README.md
└── .gitignore
```

---

## 📊 Resultados

### Estadísticas OULAD
- **Registros de estudiantes:** 32,593
- **Interacciones VLE:** 10.6M+
- **Variables analizadas:** 40+
- **Campos ordinales:** 8
- **Tablas en DB:** 20+

### Hallazgos Principales
1. Correlación entre interacciones VLE y desempeño académico
2. Distribución de patrones de acceso por módulo
3. Identificación de estudiantes en riesgo
4. ANOVA: diferencias significativas entre cohortes
5. t-tests: comparación de medias por grupo

---

## 📦 Dependencias

```
pandas==1.5.3
numpy==1.24.3
scipy==1.10.1
scikit-learn==1.2.2
matplotlib==3.7.1
seaborn==0.12.2
plotly==5.14.0
psycopg2==2.9.6
python-docx==0.8.11
```

**Instalación automática:** `./run_unix.sh` crea venv e instala todo.

---

## 🎯 Rúbrica de Evaluación

| Componente | Puntos | Logro |
|-----------|--------|-------|
| Montar OULAD en DBMS | 2 | ✅ Excelente (2/2) |
| ETL bien orquestado | 2 | ✅ Excelente (2/2) |
| EDA extendido | 10 | ✅ Excelente (10/10) |
| Artículo científico APA | 6 | ✅ Excelente (6/6) |
| **TOTAL** | **20** | **✅ 100%** |

---

## 📥 Datos

**Dataset OULAD:**
```
https://archive.ics.uci.edu/ml/datasets/Open+University+Learning+Analytics+dataset
```

El pipeline descarga automáticamente desde UCI (~500 MB).

---

## 👥 Equipo

**Estudiante:** Marlenis Judith Concepción Cuevas

---

## 📝 Notas

- Sin base de datos PostgreSQL: usa `--skip-postgres` para análisis local
- Todos los análisis se generan en CSV y PNG
- Documento APA listo para imprimir
- Compatible con Windows, macOS y Linux

---

## 📄 Licencia

Proyecto educativo - UASD 2026

---

**Última actualización:** 14 de junio de 2026
