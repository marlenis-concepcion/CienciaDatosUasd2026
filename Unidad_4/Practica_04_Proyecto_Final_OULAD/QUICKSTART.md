# Quick Start - Caso Práctico 2 OULAD

**⏱️ 5 minutos para empezar**

---

## Opción 1: Ejecución Rápida (Sin PostgreSQL) ⭐ RECOMENDADO

```bash
# 1. Navega al directorio
cd /PATH/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD

# 2. Activa ambiente (si no está activo)
source .venv/bin/activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta sin PostgreSQL (más rápido)
python etl_orchestrator.py --skip-postgres
```

**Tiempo:** ~10-15 minutos  
**Genera:** Todos los gráficos PNG, CSV, y paper APA

---

## Opción 2: Ejecución Completa (Con PostgreSQL)

### Prerequisitos:
- PostgreSQL instalado y corriendo en localhost:5432
- Usuario `postgres` con contraseña (o sin contraseña)

### Pasos:

```bash
# 1. Crear base de datos (en terminal PostgreSQL)
createdb oulad_uasd

# 2. Navega a la carpeta
cd /PATH/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD

# 3. Activa ambiente
source .venv/bin/activate

# 4. Instala dependencias
pip install -r requirements.txt

# 5. Ejecuta con PostgreSQL
python etl_orchestrator.py
```

**Tiempo:** ~20-30 minutos  
**Genera:** BD + gráficos + CSV + paper

---

## Archivos Generados

Después de ejecutar, encontrarás en `outputs/`:

```
outputs/
├── figures/
│   ├── distributions_univariate.png       ← Histogramas
│   ├── gaussian_distributions.png         ← Campana de Gauss
│   ├── correlation_matrix.png             ← Heatmap
│   ├── boxplots.png
│   ├── scatter_matrix.png
│   ├── categorical_distributions.png
│   ├── missing_data_heatmap.png
│   └── confusion_matrices.png
├── csv/
│   ├── summary_statistics.csv
│   ├── correlation_matrix.csv
│   ├── correlation_tests.csv
│   ├── anova_results.csv
│   ├── descriptive_statistics.csv
│   ├── eda_report.txt
└── [más archivos]

docs/
└── Articulo_Cientifico_OULAD_APA7.docx    ← Paper APA listo
```

---

## Si Hay Errores

### Error: "psycopg2 not installed"
```bash
pip install psycopg2-binary
```

### Error: "No such file or directory: oulad.zip"
- Se descargará automáticamente de UCI (~500 MB)
- Si falla: descárgalo manualmente desde https://archive.ics.uci.edu/ml/datasets/Open+University+Learning+Analytics+dataset

### Error: "Connection refused - PostgreSQL"
```bash
# Usa la opción sin PostgreSQL
python etl_orchestrator.py --skip-postgres
```

---

## Verificación Final

Después de ejecutar, verifica que existan:

```bash
# Gráficos
ls -lh outputs/figures/ | wc -l    # Debe mostrar 8+ archivos

# CSVs
ls -lh outputs/*.csv | wc -l        # Debe mostrar 5+ archivos

# Paper
ls -lh docs/Articulo_Cientifico_OULAD_APA7.docx  # Debe existir
```

---

## Próximo Paso

Abre el paper generado:
```
docs/Articulo_Cientifico_OULAD_APA7.docx
```

Inserta la evidencia de colaboración (video o screenshot) y ¡listo para entregar!

---

**¿Dudas?** Consulta:
- CASO_PRACTICO_2.md - Guía completa
- GUIA_COLABORACION.md - Colaboración en equipo
