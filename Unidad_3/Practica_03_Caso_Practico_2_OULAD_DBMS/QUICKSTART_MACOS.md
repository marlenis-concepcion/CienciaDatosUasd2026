# QuickStart - macOS

**⏱️ 5 minutos para empezar**

---

## PASO 1: Navega a la carpeta

```bash
cd /PATH/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD
```

O en Finder:
- Cmd + Shift + G
- Pega la ruta
- Enter

---

## PASO 2: Ejecuta el script automático

```bash
chmod +x run_unix.sh
./run_unix.sh --skip-postgres
```

**¿Qué hace?**
- ✅ Crea ambiente virtual Python
- ✅ Instala todas las dependencias
- ✅ Descarga OULAD desde UCI
- ✅ Genera análisis EDA (8 gráficos PNG)
- ✅ Crea CSV con estadísticas
- ✅ Genera paper científico APA

**Tiempo:** ~15 minutos

---

## PASO 3: O ejecución manual

```bash
# Crear ambiente virtual
python3 -m venv .venv

# Activar
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pipeline
python3 etl_orchestrator.py --skip-postgres
```

---

## PASO 4: Verificar resultados

En Terminal:
```bash
# Ver gráficos
ls -lh outputs/figures/

# Ver análisis
ls -lh outputs/*.csv

# Ver documento
open docs/Articulo_Cientifico_OULAD_APA7.docx
```

O en Finder:
- Abre carpeta del proyecto
- Ve a `outputs/figures/` → verás los 8 PNG
- Ve a `docs/` → verás el documento Word APA

---

## PASO 5: Grabar video colaborativo

**Opción 1: Usar QuickTime (integrado en macOS)**
```bash
# Abre QuickTime
open /Applications/QuickTime\ Player.app

# File → New Screen Recording
# Graba 2-5 minutos
# Guarda como: video_colaboracion.mp4
```

**Opción 2: Usar Zoom**
```bash
# Si tienes Zoom instalado
open /Applications/Zoom.app

# Start meeting → Share screen
# Grabar mientras hablas con equipo
```

---

## PASO 6: Insertar en documento y enviar

```bash
# Abrir documento Word
open docs/Articulo_Cientifico_OULAD_APA7.docx
```

Entonces:
1. En Word: Insert → Link
2. Pega URL de video (Google Drive)
3. Agrega en sección "Evidencia de Colaboración"
4. Cmd + S para guardar
5. Envía en aula virtual

---

## ⚡ Comandos útiles para macOS

```bash
# Ver Python versión
python3 --version

# Abrir carpeta en Finder
open .

# Abrir archivo
open docs/Articulo_Cientifico_OULAD_APA7.docx

# Comprimir para envío
zip -r Caso_Practico_2_OULAD.zip Practica_04_Proyecto_Final_OULAD/

# Descomprimir
unzip Caso_Practico_2_OULAD.zip

# Ver tamaño de carpeta
du -sh Practica_04_Proyecto_Final_OULAD/
```

---

## 🔧 Si hay problemas

**Error: "command not found: python3"**
```bash
# Instalar Homebrew primero:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Luego:
brew install python3
```

**Error: Permiso denegado en run_unix.sh**
```bash
chmod +x run_unix.sh
```

**Error: pip no funciona**
```bash
python3 -m pip install --upgrade pip
```

**PostgreSQL no conecta (normal, usamos --skip-postgres)**
```bash
# Es esperado que falle PostgreSQL
# El flag --skip-postgres lo ignora automáticamente
```

---

## 📊 Verificación visual en macOS

Después de ejecutar, deberías ver:

```
Practica_04_Proyecto_Final_OULAD/
├── outputs/
│   ├── figures/
│   │   ├── distributions_univariate.png ✓
│   │   ├── gaussian_distributions.png ✓
│   │   ├── correlation_matrix.png ✓
│   │   ├── boxplots.png ✓
│   │   ├── scatter_matrix.png ✓
│   │   ├── categorical_distributions.png ✓
│   │   ├── missing_data_heatmap.png ✓
│   │   └── confusion_matrices.png ✓
│   ├── correlation_tests.csv ✓
│   ├── anova_results.csv ✓
│   └── [más CSV]
└── docs/
    └── Articulo_Cientifico_OULAD_APA7.docx ✓
```

---

## ✅ Checklist Final

- [ ] Descargué proyecto a `/PATH/`
- [ ] Ejecuté `./run_unix.sh --skip-postgres`
- [ ] Pipeline terminó exitosamente (sin errores)
- [ ] Abrí `outputs/figures/` - veo 8 PNG
- [ ] Abrí `docs/` - veo el documento Word
- [ ] Grabé video de 2-5 min en QuickTime o Zoom
- [ ] Inserté enlace de video en documento
- [ ] Guardé documento (Cmd+S)
- [ ] Comprimí con `zip -r Caso_Practico_2_OULAD.zip ...`
- [ ] Subí en aula virtual ANTES del 20 junio 23:59

---

## 🎯 Archivos importantes

**Para enviar en aula virtual:**
1. `docs/Articulo_Cientifico_OULAD_APA7.docx` ← PRINCIPAL
2. `Caso_Practico_2_OULAD.zip` ← Respaldo con todo el código

---

**¡Listo! El documento APA está en:** 
```
/PATH/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD/docs/Articulo_Cientifico_OULAD_APA7.docx
```

O simplemente escribe en Terminal:
```bash
open docs/Articulo_Cientifico_OULAD_APA7.docx
```
