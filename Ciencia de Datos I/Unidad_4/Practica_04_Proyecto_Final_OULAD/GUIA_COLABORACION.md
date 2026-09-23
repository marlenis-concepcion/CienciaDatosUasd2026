# Guía de Colaboración - Caso Práctico 2

**Objetivo:** Proporcionar instrucciones para trabajo colaborativo en equipo con evidencia documentada.

---

## 📋 Estructura de Equipo Recomendada

Para optimizar la colaboración, se sugiere la siguiente división de roles:

| Rol | Responsabilidad | Archivos Principales |
|-----|-----------------|----------------------|
| **Coordinador** | Integración, merge de cambios, git flow | CASO_PRACTICO_2.md, etl_orchestrator.py |
| **Ingeniero de Datos** | SQL, ETL, PostgreSQL | sql/01_schema_oulad.sql, src/db_loader.py |
| **Analista de Datos** | EDA, visualizaciones, estadísticas | src/eda_extended.py, notebooks/ |
| **Escritor Técnico** | Documentación, paper APA | scripts/generate_apa_paper.py, docs/ |
| **QA/Testing** | Validación, pruebas | tests/, verificación final |

---

## 🔄 Flujo de Trabajo Git

### 1. Configuración Inicial

```bash
# Clonar repositorio
git clone https://github.com/marlenis-concepcion/CienciaDatosUasd2026.git
cd CienciaDatosUasd2026

# Crear rama para este proyecto
git checkout -b feature/caso-practico-2-oulad

# Crear ambiente virtual
python3 -m venv .venv
source .venv/bin/activate
pip install -r Unidad_4/Practica_04_Proyecto_Final_OULAD/requirements.txt
```

### 2. Ciclo de Desarrollo Colaborativo

```bash
# Cada miembro en su rama
git checkout -b feature/[tu-rol]/[tarea]
# Ej: git checkout -b feature/data-engineer/ddl-schema

# Trabajar en cambios
git add [archivos modificados]
git commit -m "feat: [descripción clara del cambio]"

# Antes de push, actualizar con main
git fetch origin
git rebase origin/develop

# Enviar cambios
git push origin feature/[tu-rol]/[tarea]

# Crear Pull Request en GitHub
# → Título claro
# → Descripción detallada
# → Mencionar a otros miembros (@user)
```

### 3. Ejemplo de Commits Colaborativos

**Ingeniero de Datos:**
```
commit: sql: create OULAD schema with 20+ tables and indexes
  - Added dimension tables: courses, modules, assessments, vle
  - Added fact tables: student_info, student_assessment, student_vle
  - Created FullDomain aggregation tables
  - Added views for common queries
```

**Analista de Datos:**
```
commit: feat: implement ExtendedEDA with 8 visualization types
  - Added gaussian distributions, boxplots, scatter matrix
  - Implemented ANOVA and correlation tests
  - Export statistics to CSV
```

**Coordinador:**
```
commit: feat: create ETL orchestrator with 6-step pipeline
  - Step 1: Data download from UCI
  - Step 2-3: PostgreSQL initialization and load
  - Step 4-6: EDA and paper generation
  - Add comprehensive logging
```

---

## 💬 Comunicación del Equipo

### Canales Recomendados:

1. **GitHub Issues** - Para tareas y seguimiento
2. **GitHub Discussions** - Para debates técnicos
3. **Pull Request Comments** - Para revisión de código
4. **Video Conferencia** - Para reuniones de coordinación

### Reuniones Obligatorias:

| Cuándo | Duración | Tema |
|--------|----------|------|
| Inicio del proyecto | 30 min | Planeación y división de roles |
| Cada 2 días | 15 min | Sync rápido de avances |
| Antes de entregar | 1 hora | Revisión final y ajustes |

---

## 📹 Evidencia de Colaboración Requerida

### Opción 1: Video de Reunión ⭐ RECOMENDADO

**Requisitos:**
- Duración: 2-5 minutos
- Mostrar: Pantalla compartida + caras de integrantes
- Contenido: Discusión sobre algún aspecto técnico

**Herramientas:**
- Zoom (grabar sesión)
- Google Meet (grabar reunión)
- Teams (grabar en reunión)
- OBS Studio (grabar pantalla local)

**Pasos:**
1. Grabar una reunión del equipo
2. Guardar video como: `COLABORACION_VIDEO.mp4` o `.webm`
3. Subir a carpeta Google Drive
4. Insertar enlace en documento Word

**Ejemplo:**
```markdown
## Evidencia de Colaboración

[Video de Reunión Colaborativa](https://drive.google.com/file/d/[ID]/view)

Integrantes participantes:
- Marlenis Concepción (Coordinadora)
- Juan Pérez (Ingeniero de Datos)
- María García (Analista de Datos)
- Carlos López (Escritor Técnico)

Duración: 3 minutos
Tema discutido: Validación del schema PostgreSQL y pruebas de carga ETL
Fecha: 18 de junio de 2026
```

### Opción 2: Screenshots de Entorno Colaborativo

**Alternativa si no puede grabar video:**

1. **Google Colab Compartido:**
   ```
   Screenshot mostrando:
   - Notebook compartido con múltiples editores
   - Comentarios de diferentes usuarios
   - Historial de cambios
   ```

2. **GitHub Collaboration:**
   ```
   Screenshot mostrando:
   - Pull requests con reviews
   - Commits de múltiples autores
   - Discussions o issues activos
   ```

3. **Google Drive:**
   ```
   Screenshot mostrando:
   - Documento compartido
   - Comentarios simultáneos
   - Historial de versiones con contribuyentes
   ```

**Insertar en documento Word:**
```
Inserta → Imagen → [selecciona screenshot]
Título: "Evidencia de Colaboración - [Tipo]"
```

### Opción 3: GitHub Commits Evidentes

Si el video no es posible, usar commits claros:

```bash
# Cada integrante hace commits con su email
git config user.name "Nombre Completo"
git config user.email "correo@example.com"

# Commits incluyen co-authors
git commit -m "feat: descripción

Co-authored-by: Nombre <correo@example.com>
Co-authored-by: Otro <correo@example.com>"
```

**Verificar en GitHub:**
```
Repositorio → Commits → [Ver múltiples autores en el mismo cambio]
```

---

## 📝 Insertar Evidencia en Documento APA

### En documento Word:

```
                    EVIDENCIA DE TRABAJO COLABORATIVO

Se adjunta evidencia de trabajo colaborativo realizado por el equipo McCarthy:

[OPCIÓN A] Video: Los miembros del equipo participaron en una reunión 
colaborativa donde discutieron los aspectos técnicos de la implementación 
de la base de datos PostgreSQL y la validación del pipeline ETL. El video 
se encuentra disponible en:

      URL: https://drive.google.com/file/d/[ID_VIDEO]/view
      Duración: 3:45 minutos
      Fecha: 18 de junio de 2026

[OPCIÓN B] Screenshot: Se comparte evidencia del ambiente colaborativo 
en Google Colab, donde múltiples integrantes del equipo editaron 
simultáneamente el código de análisis exploratorio de datos.

      [IMAGEN INSERTADA AQUÍ]
      Descripción: Notebook compartido con comentarios de 3 integrantes
      Fecha: 17 de junio de 2026

Integrantes del Equipo McCarthy:
1. Marlenis Concepción (Coordinadora)
2. [Integrante 2] (Ingeniero de Datos)
3. [Integrante 3] (Analista de Datos)
4. [Integrante 4] (Escritor Técnico)

Rol de cada integrante en el Caso Práctico 2:
- Coordinadora: Integración de componentes, git flow, revisión final
- Ingeniero: Implementación SQL y ETL a PostgreSQL
- Analista: EDA, visualizaciones, análisis estadístico
- Escritor: Redacción de artículo científico APA
```

---

## 🔍 Verificación de Colaboración en GitHub

Los evaluadores verificarán:

```bash
# Ver commits por autor
git log --all --pretty=format:"%H %an %ae %s" | head -20

# Ver pull requests
GitHub: repositorio → Pull Requests → (ver múltiples PRs)

# Ver colaboradores
GitHub: repositorio → Insights → Contributors
```

**Checklist para verificar:**
- [ ] Mínimo 3-4 contribuyentes con commits
- [ ] Commits en diferentes fechas (trabajo a lo largo del tiempo)
- [ ] Pull requests con descripción y reviews
- [ ] Commits con mensaje descriptivo
- [ ] Video o screenshot de reunión adjunto

---

## 🚀 Ejemplo de Sesión Colaborativa Efectiva

### Estructura de 1 hora:

**Minuto 0-5:** Bienvenida y orden del día
```
"Buenos días equipo. Hoy completaremos:
1. Validación del schema PostgreSQL
2. Pruebas de carga ETL
3. Revisión de gráficos EDA"
```

**Minuto 5-20:** Presentación de avances
```
Ingeniero de Datos: "Completé el schema con 20+ tablas.
Aquí está el diagrama entidad-relación..."
```

**Minuto 20-40:** Trabajo colaborativo
```
Todos mirando el mismo código en pantalla compartida
Haciendo sugerencias y ajustes en tiempo real
```

**Minuto 40-55:** Revisión de checklist
```
- Schema SQL: ✓
- ETL Pipeline: ✓
- EDA Visualizations: En progreso
```

**Minuto 55-60:** Tareas para siguientes 2 días
```
"Juan: termina tests ETL para mañana
María: gráficos finales para pasado
Carlos: borrador intro paper"
```

### Grabar esta sesión:
```bash
# En Zoom
1. Start Meeting
2. Click Share Screen
3. Record to Cloud
4. Al terminar: Download recording
5. Subir a Google Drive y compartir link
```

---

## 📊 Métricas de Colaboración

El evaluador verificará:

| Métrica | Mínimo | Tu Equipo |
|---------|--------|----------|
| # Contribuyentes | 2 | ? |
| # Commits | 10 | ? |
| # Pull Requests | 2 | ? |
| # Días activos | 3+ | ? |
| # Reuniones registradas | 1+ | ? |
| Documento comentado | Sí | ? |

---

## ⚠️ Errores Comunes a Evitar

❌ **NO:**
- Hacer todos los cambios un solo integrante
- Un solo commit gigante con todo
- Sin comunicación entre miembros
- GitHub con un solo contribuyente
- Evidencia falsa o inventada

✅ **SÍ:**
- Commits pequeños y frecuentes
- Múltiples ramas por rol
- Pull requests con reviews
- Video real de reunión
- GitHub con actividad visible de todos

---

## 🎬 Guion para Grabar Video (2-3 minutos)

**Tiempo:** 2:30 minutos

```
[0:00-0:15] Introducción
"Buenas, equipo McCarthy. Aquí estamos en nuestra reunión de trabajo
colaborativo para el Caso Práctico 2 de OULAD. Vamos a mostrar 
el avance del proyecto."

[0:15-0:45] Presentación del schema
"Marlenis muestra el diagrama ER: aquí están las 20+ tablas que
diseñamos: cursos, estudiantes, evaluaciones, interacciones VLE.
Cada tabla tiene campos ordinales para las categorías."

[0:45-1:15] Demo del pipeline
"Aquí está el ETL orchestrator. Se ejecuta en 6 pasos:
descarga datos, crea schema, carga a PostgreSQL, genera EDA,
y produce el paper en APA."

[1:15-1:45] Resultados EDA
"Los gráficos muestran correlaciones, distribuciones, boxplots.
Aquí el heatmap de correlación con matriz de confusión."

[1:45-2:30] Cierre
"Equipo, qué es lo importante? División clara de roles, commits
diarios, y documentación en cada paso. Listo para entregar el 20."
```

---

## 📋 Checklist Final antes de Entregar

- [ ] Video grabado (2-5 min) o screenshot de colaboración
- [ ] Video subido a Google Drive y compartido
- [ ] Enlace insertado en documento Word
- [ ] Integrantes y roles claramente identificados
- [ ] GitHub repo con múltiples commits visibles
- [ ] Todos los archivos SQL, Python, EDA generados
- [ ] outputs/ con PNG y CSV
- [ ] Paper APA con evidencia insertada
- [ ] ZIP/RAR con todo el contenido
- [ ] Enviado en aula virtual antes del 20 de junio

---

**¡Éxito en el trabajo colaborativo!**

Para preguntas: consulta al facilitador Dr. Silverio del Orbe Abad
