# Práctica 03: Caso Práctico 2 - OULAD en Base de Datos

**Asignatura:** INF-8237-C2 Ciencia de Datos I  
**Unidad:** 3 - Análisis Exploratorio de Datos  
**Facilitador:** Dr. Silverio del Orbe Abad  
**Equipo:** McCarthy Team  
**Puntos Totales:** 20 puntos

---

## 📋 Descripción

Exportación e integración del dataset OULAD (Open University Learning Analytics Dataset) a una base de datos relacional PostgreSQL, seguido de un análisis exploratorio extendido, modelado estadístico y redacción de un artículo científico con hallazgos.

---

## 🎯 Objetivos

1. **Montar OULAD en un DBMS** (2 pts)
   - Crear schema DDL completo
   - Implementar PK y FK
   - Crear campos ordinales
   - Diseñar FullDomain tables

2. **ETL Bien Orquestado** (2 pts)
   - Encapsular lógica de carga
   - Implementar 6 pasos del pipeline
   - Logging transaccional
   - Manejo robusto de errores

3. **EDA Extendido** (10 pts)
   - 8 tipos de visualizaciones
   - 5+ análisis estadísticos
   - Pruebas de hipótesis
   - Descriptiva completa

4. **Artículo Científico APA** (6 pts)
   - Estructura APA 7
   - Máximo 10 páginas
   - 10+ referencias
   - Hallazgos principales

---

## 📁 Estructura de Carpetas

```
Practica_03_Caso_Practico_2_OULAD_DBMS/
├── README.md                          ← Este archivo
├── QUICKSTART_LINUX.md               ← Guía rápida Linux
├── QUICKSTART_MACOS.md               ← Guía rápida macOS
├── QUICKSTART_WINDOWS.md             ← Guía rápida Windows
├── TAREAS_POR_SO.txt                 ← Tareas por sistema operativo
│
├── Practica_04_Proyecto_Final_OULAD/ ← Código fuente (symlink a Unidad 4)
│   ├── sql/
│   │   └── 01_schema_oulad.sql       ← Schema DDL (20+ tablas)
│   ├── src/
│   │   ├── db_loader.py              ← ETL PostgreSQL
│   │   └── eda_extended.py           ← EDA extendido
│   ├── scripts/
│   │   └── generate_apa_paper.py    ← Generador paper APA
│   ├── docs/
│   │   └── Articulo_Cientifico_OULAD_APA7.docx
│   └── outputs/
│       ├── figures/                   ← 8 gráficos PNG
│       └── [CSV análisis]
│
└── EVIDENCIAS/
    └── [Video colaborativo]
```

---

## ⚡ Inicio Rápido

### Selecciona tu Sistema Operativo:

**🐧 LINUX**
```bash
cat QUICKSTART_LINUX.md
# O:
./run_unix.sh --skip-postgres
```

**🍎 MACOS**
```bash
cat QUICKSTART_MACOS.md
# O:
./run_unix.sh --skip-postgres
```

**🪟 WINDOWS**
```powershell
type QUICKSTART_WINDOWS.md
# O:
run_windows.bat --skip-postgres
```

---

## 📚 Documentación Disponible

| Archivo | Propósito |
|---------|-----------|
| **QUICKSTART_LINUX.md** | Guía paso a paso para Linux |
| **QUICKSTART_MACOS.md** | Guía paso a paso para macOS |
| **QUICKSTART_WINDOWS.md** | Guía paso a paso para Windows |
| **TAREAS_POR_SO.txt** | Checklist de tareas por SO |
| **Practica_04_Proyecto_Final_OULAD/** | Código fuente completo |

---

## 📊 Componentes Entregables

### 1. Database Schema (2 puntos)
- ✅ `sql/01_schema_oulad.sql` - 20+ tablas
- ✅ Restricciones PK y FK
- ✅ Campos ordinales (8 variables)
- ✅ FullDomain tables
- ✅ Índices optimizados

### 2. ETL Pipeline (2 puntos)
- ✅ `src/db_loader.py` - Encapsulado
- ✅ `etl_orchestrator.py` - 6 pasos
- ✅ Encoding ordinal automático
- ✅ Logging transaccional
- ✅ Manejo robusto de errores

### 3. EDA Extendido (10 puntos)
- ✅ `src/eda_extended.py` - 12+ métodos
- ✅ 8 visualizaciones PNG
- ✅ 5+ análisis CSV
- ✅ Pruebas ANOVA y correlación
- ✅ Estadísticas descriptivas

### 4. Paper Científico APA (6 puntos)
- ✅ `docs/Articulo_Cientifico_OULAD_APA7.docx`
- ✅ Formato APA 7 UASD
- ✅ Estructura completa
- ✅ 10+ referencias
- ✅ Hallazgos principales

---

## 🚀 Ejecución del Proyecto

### Paso 1: Leer QuickStart
```bash
# Selecciona tu SO:
cat QUICKSTART_LINUX.md     # Linux
cat QUICKSTART_MACOS.md     # macOS
type QUICKSTART_WINDOWS.md  # Windows
```

### Paso 2: Ejecutar Pipeline
```bash
# Linux/macOS:
./run_unix.sh --skip-postgres

# Windows:
run_windows.bat --skip-postgres
```

### Paso 3: Verificar Outputs
```bash
ls outputs/figures/   # Debería haber 8 PNG
ls outputs/*.csv      # Debería haber 5+ CSV
```

### Paso 4: Abrir Documento APA
```bash
# Linux:
libreoffice docs/Articulo_Cientifico_OULAD_APA7.docx

# macOS:
open docs/Articulo_Cientifico_OULAD_APA7.docx

# Windows:
start docs\Articulo_Cientifico_OULAD_APA7.docx
```

### Paso 5: Grabar Video Colaborativo
- Grabar reunión de equipo (2-5 minutos)
- Mostrar pantalla compartida
- Guardar como MP4

### Paso 6: Insertar en Documento
- Abrir documento Word
- Insert → Link
- Pegar URL de video
- Guardar documento

### Paso 7: Empaquetar y Enviar
```bash
# Crear ZIP:
zip -r Caso_Practico_2_OULAD.zip Practica_04_Proyecto_Final_OULAD/

# Enviar en Aula Virtual UASD
# Archivos:
# 1. Articulo_Cientifico_OULAD_APA7.docx
# 2. Caso_Practico_2_OULAD.zip
```

---

## 📋 Rúbrica de Evaluación

| Componente | Excelente | Cumple | Parcial | No Cumple |
|-----------|-----------|--------|---------|-----------|
| DBMS (2 pts) | DER + DDL | Schema OK | Incompleto | No |
| ETL (2 pts) | Encapsulado | Funcional | Parcial | No |
| EDA (10 pts) | 8+ gráficos | 5-7 gráficos | 3-4 | 0-2 |
| Paper (6 pts) | Completo | Estructura OK | Falta sec. | Incompleto |

---

## ⏰ Timeline de Entrega

- **14 junio:** ✅ Proyecto completado
- **15-19 junio:** ⏳ Grabar video colaborativo
- **19 junio 23:59:** ⏰ Último ajuste
- **20 junio 23:59:** 📤 **DEADLINE FINAL**

---

## 🔗 Links Importantes

**Repositorio GitHub:**
```
https://github.com/marlenis-concepcion/CienciaDatosUasd2026
└─ tree/main/Unidad_3/Practica_03_Caso_Practico_2_OULAD_DBMS
```

**Dataset OULAD:**
```
https://archive.ics.uci.edu/ml/datasets/Open+University+Learning+Analytics+dataset
```

**Aula Virtual UASD:**
```
https://aula.uasd.edu.do
```

---

## 📞 Soporte

- **Facilitador:** Dr. Silverio del Orbe Abad
- **Asignatura:** INF-8237-C2 Ciencia de Datos I
- **Institución:** UASD - Facultad de Ciencias

---

## ✅ Verificación Final

Antes de enviar, verifica:

- [ ] Ejecuté pipeline exitosamente
- [ ] Todos los PNG se generaron (8)
- [ ] Todos los CSV se generaron (5+)
- [ ] Abrí documento APA sin errores
- [ ] Inserté enlace de video en documento
- [ ] Guardé documento (Ctrl/Cmd+S)
- [ ] Comprimí con ZIP
- [ ] Subí archivos en aula virtual
- [ ] Confirmé entrega antes 20 junio 23:59

---

**Documento APA listo en:** 
```
Practica_04_Proyecto_Final_OULAD/docs/Articulo_Cientifico_OULAD_APA7.docx
```

¡**LISTO PARA ENTREGAR!**
