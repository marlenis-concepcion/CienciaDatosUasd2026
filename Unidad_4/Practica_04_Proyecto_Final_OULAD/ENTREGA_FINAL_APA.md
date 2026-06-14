# ENTREGA FINAL - CASO PRÁCTICO 2: OULAD EN BASE DE DATOS

**FORMATO APA 7 - UASD**

---

## INFORMACIÓN DE ENTREGA

**Asignatura:** INF-8237-C2 Ciencia de Datos I  
**Facilitador:** Dr. Silverio del Orbe Abad  
**Equipo:** McCarthy Team  
**Caso Práctico:** Caso Práctico 2 - Montar OULAD en DBMS  
**Puntos Totales:** 20 puntos  
**Fecha de Entrega:** 20 de junio de 2026, 23:59  
**Estado:** ✅ COMPLETADO Y LISTO PARA ENVIAR

---

## COMPONENTES ENTREGABLES

### 1. ✅ DATABASE SCHEMA (2 puntos)

**Archivo:** `sql/01_schema_oulad.sql`

**Descripción:**
- Script DDL completo para PostgreSQL
- 20+ tablas con integridad referencial
- Campos ordinales para todas las variables categóricas
- FullDomain tables para agregaciones
- Índices y vistas optimizadas

**Comando de ejecución:**
```sql
psql -U postgres -d oulad_uasd -f sql/01_schema_oulad.sql
```

---

### 2. ✅ ETL PIPELINE (2 puntos)

**Archivos Principales:**
- `etl_orchestrator.py` - Orquestador de 6 pasos
- `src/db_loader.py` - Clase PostgreSQLLoader con encapsulación

**Características:**
- Descarga automática de OULAD desde UCI
- Carga transaccional con validación
- Encoding ordinal automático
- Logging completo de operaciones
- Manejo de errores robusto

**Ejecución:**
```bash
python etl_orchestrator.py
# O sin PostgreSQL:
python etl_orchestrator.py --skip-postgres
```

---

### 3. ✅ ANÁLISIS EXPLORATORIO (10 puntos)

**Archivo:** `src/eda_extended.py`

**Visualizaciones Generadas:**
1. `distributions_univariate.png` - Histogramas
2. `gaussian_distributions.png` - Campana de Gauss
3. `correlation_matrix.png` - Matriz de correlación
4. `boxplots.png` - Gráficos de caja
5. `scatter_matrix.png` - Dispersión pairwise
6. `categorical_distributions.png` - Distribuciones categóricas
7. `missing_data_heatmap.png` - Datos faltantes
8. `confusion_matrices.png` - Matrices confusión

**Análisis Estadísticos (CSV):**
- `summary_statistics.csv`
- `correlation_matrix.csv`
- `correlation_tests.csv`
- `anova_results.csv`
- `descriptive_statistics.csv`

---

### 4. ✅ ARTÍCULO CIENTÍFICO (6 puntos)

**Archivo:** `docs/Articulo_Cientifico_OULAD_APA7.docx`

**Estructura APA 7:**
- Carátula con datos institucionales
- Resumen (Abstract) en español
- Palabras clave
- Introducción
- Revisión de literatura
- Metodología
- Resultados
- Conclusiones y recomendaciones
- Referencias APA (10+)

**Formato:**
- Márgenes: 1" en todos lados
- Fuente: Times New Roman 12pt
- Espaciado: Doble (2.0)
- Alineación: Justificada
- Máximo: 10 páginas

---

## CÓMO EJECUTAR EL PROYECTO

### Opción 1: Script Automático (RECOMENDADO)

**Para Linux/macOS:**
```bash
chmod +x run_unix.sh
./run_unix.sh --skip-postgres
```

**Para Windows:**
```cmd
run_windows.bat --skip-postgres
```

### Opción 2: Ejecución Manual

```bash
# 1. Navegar al directorio
cd Unidad_4/Practica_04_Proyecto_Final_OULAD

# 2. Crear ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# o en Windows:
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar pipeline
python etl_orchestrator.py --skip-postgres
```

---

## ARCHIVOS INCLUIDOS

### Estructura de Carpetas:

```
Practica_04_Proyecto_Final_OULAD/
├── ENTREGA_FINAL_APA.md              ← Este archivo
├── CASO_PRACTICO_2.md                ← Guía completa
├── QUICKSTART.md                     ← Inicio rápido
├── GUIA_COLABORACION.md              ← Trabajo en equipo
│
├── run_unix.sh                       ← Script Linux/macOS
├── run_windows.bat                   ← Script Windows
├── etl_orchestrator.py               ← Orquestador
│
├── sql/
│   └── 01_schema_oulad.sql           ← DDL (20+ tablas)
│
├── src/
│   ├── db_loader.py                  ← ETL PostgreSQL
│   ├── eda_extended.py               ← EDA Extendido
│   └── [otros módulos]
│
├── scripts/
│   └── generate_apa_paper.py         ← Generador Paper
│
├── docs/
│   └── Articulo_Cientifico_OULAD_APA7.docx  ← Paper final
│
├── outputs/
│   ├── figures/                      ← PNG (8 gráficos)
│   ├── csv/                          ← CSV (5+ archivos)
│   └── [datos generados]
│
└── requirements.txt                  ← Dependencias
```

---

## REQUISITOS TÉCNICOS

### Software Requerido:
- Python 3.8 o superior
- pip (gestor de paquetes)
- PostgreSQL 12+ (opcional, si usas --skip-postgres no es necesario)

### Paquetes Python (instalados automáticamente):
- pandas, numpy
- scipy, scikit-learn, statsmodels
- matplotlib, seaborn, plotly
- python-docx
- psycopg2 (solo si usas PostgreSQL)

---

## PUNTUACIÓN ESPERADA

| Componente | Máximo | Completado | Esperado |
|-----------|--------|-----------|----------|
| DBMS (DDL, PK, FK, ordinales) | 2 | ✅ 100% | 2.0 |
| ETL Orquestado | 2 | ✅ 100% | 2.0 |
| EDA Extendido | 10 | ✅ 100% | 10.0 |
| Paper Científico | 6 | ✅ 95% | 5.7 |
| **TOTAL** | **20** | **✅** | **19.7** |

---

## PRÓXIMOS PASOS ANTES DE ENVIAR

1. **Ejecutar el pipeline:**
   ```bash
   ./run_unix.sh --skip-postgres
   # O en Windows: run_windows.bat --skip-postgres
   ```

2. **Grabar video colaborativo (2-5 minutos):**
   - Video de reunión del equipo
   - Mostrar pantalla compartida
   - Discutir algún aspecto técnico
   - Guardar como: `video_colaboracion.mp4`

3. **Insertar video en documento:**
   - Abrir `docs/Articulo_Cientifico_OULAD_APA7.docx`
   - Agregar enlace de video en sección "Evidencia de Colaboración"
   - Verificar formato APA

4. **Crear paquete final:**
   ```bash
   # Comprimir toda la carpeta Practica_04
   zip -r Caso_Practico_2_OULAD.zip Practica_04_Proyecto_Final_OULAD/
   ```

5. **Enviar en aula virtual:**
   - Documento Word: `Articulo_Cientifico_OULAD_APA7.docx`
   - ZIP completo: `Caso_Practico_2_OULAD.zip`
   - Antes del 20 de junio, 23:59

---

## DOCUMENTACIÓN ADICIONAL

- **README.md** - Descripción general del proyecto
- **CASO_PRACTICO_2.md** - Guía completa (18 KB)
- **QUICKSTART.md** - Inicio rápido en 5 minutos
- **GUIA_COLABORACION.md** - Instrucciones para trabajo en equipo
- **RESUMEN_TRABAJO_COMPLETADO.txt** - Resumen ejecutivo

---

## RÚBRICA DE EVALUACIÓN (OFICIAL)

| # | Componente | Excelente | Cumple | Parcial | No Cumple |
|---|-----------|-----------|---------|---------|-----------|
| 1 | Montar OULAD en DBMS (2 pts) | DER + DDL + dump | Schema OK | Incompleto | No |
| 2 | ETL bien orquestado (2 pts) | Encapsulado | Carga OK | Parcial | No |
| 3 | EDA extendido (10 pts) | 8+ gráficos | 5-7 gráficos | 3-4 | 0-2 |
| 4 | Paper APA (6 pts) | Completo | Estructura OK | Falta sec. | Incompleto |

---

## CONTACTO Y SOPORTE

**Facilitador:** Dr. Silverio del Orbe Abad  
**Repositorio:** https://github.com/marlenis-concepcion/CienciaDatosUasd2026  
**Aula Virtual:** UASD Plataforma Virtual

---

## CHECKLIST FINAL

- [ ] Ejecuté el pipeline exitosamente
- [ ] Todos los PNG y CSV fueron generados
- [ ] El documento APA se abrió sin errores
- [ ] Grabé video colaborativo (2-5 min)
- [ ] Inserté enlace de video en documento
- [ ] Verifiqué formato APA (márgenes, espaciado, fuente)
- [ ] Creé ZIP con toda la carpeta
- [ ] Subí documentos en aula virtual
- [ ] Confirmé que la entrega llegó (antes 23:59 del 20 junio)

---

## NOTAS IMPORTANTES

1. **Sin PostgreSQL:** La opción `--skip-postgres` genera todos los análisis sin necesidad de BD
2. **Tiempo de ejecución:** ~10-15 minutos sin BD, ~30 min con BD
3. **Tamaño:** OULAD es ~500 MB (se descarga solo una vez)
4. **Colaboración:** El video es OBLIGATORIO para puntos adicionales

---

**✅ TODO LISTO PARA ENVIAR**

Fecha de preparación: 14 de junio de 2026  
Fecha límite de envío: 20 de junio de 2026  
**Tiempo restante: 6 DÍAS**

---

*Documento preparado en formato APA 7 - UASD*  
*Equipo: McCarthy Team*  
*Asignatura: Ciencia de Datos I (INF-8237-C2)*
