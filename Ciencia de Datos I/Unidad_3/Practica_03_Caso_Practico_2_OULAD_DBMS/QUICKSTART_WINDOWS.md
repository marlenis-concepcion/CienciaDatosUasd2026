# QuickStart - Windows

**⏱️ 5 minutos para empezar**

---

## PASO 1: Abre PowerShell o CMD

**Opción A: PowerShell (RECOMENDADO)**
- Presiona: `Win + X`
- Selecciona: "Windows PowerShell" o "Terminal"

**Opción B: CMD**
- Presiona: `Win + R`
- Escribe: `cmd`
- Enter

---

## PASO 2: Navega a la carpeta

```powershell
cd "/PATH/CienciaDatosUasd2026\Unidad_4\Practica_04_Proyecto_Final_OULAD"
```

O en Explorador de Archivos:
- Copia la ruta en la barra de dirección
- Pega después de "cd"

---

## PASO 3: Ejecuta el script automático

```powershell
run_windows.bat --skip-postgres
```

**¿Qué hace?**
- ✅ Crea ambiente virtual Python
- ✅ Instala todas las dependencias
- ✅ Descarga OULAD desde UCI (~500 MB)
- ✅ Genera EDA (8 gráficos PNG)
- ✅ Crea CSV con análisis estadísticos
- ✅ Genera paper científico en APA

**Tiempo:** ~15 minutos

---

## PASO 4: O ejecución manual (si el script falla)

```powershell
# Crear ambiente virtual
python -m venv .venv

# Activar (PowerShell)
.venv\Scripts\activate.ps1

# Activar (CMD)
.venv\Scripts\activate.bat

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python etl_orchestrator.py --skip-postgres
```

---

## PASO 5: Verificar resultados

En PowerShell/CMD:
```powershell
# Ver gráficos
dir outputs\figures\

# Ver análisis CSV
dir outputs\*.csv

# Abrir documento
start docs\Articulo_Cientifico_OULAD_APA7.docx
```

En Explorador:
- Abre la carpeta del proyecto
- Ve a `outputs\figures\` → deberías ver 8 PNG
- Ve a `docs\` → verás el documento Word

---

## PASO 6: Grabar video colaborativo

**Opción 1: Usar Zoom**
```powershell
# Si tienes Zoom instalado
zoom
```
- Start meeting
- Share screen
- Graba 2-5 minutos con el equipo

**Opción 2: Usar OBS Studio**
```powershell
# Si tienes OBS instalado
obs
```

**Opción 3: Usar herramienta integrada de Windows 11**
- Presiona: `Win + G`
- Haz clic en "Grabar"
- Graba pantalla

---

## PASO 7: Insertar en documento y enviar

```powershell
# Abrir documento Word
start docs\Articulo_Cientifico_OULAD_APA7.docx
```

Entonces:
1. En Word: Insert → Link
2. Pega URL de video (Google Drive, YouTube, etc.)
3. Agrega en sección "Evidencia de Colaboración"
4. Ctrl+S para guardar
5. Envía en aula virtual

---

## ⚡ Comandos útiles para Windows

```powershell
# Ver versión de Python
python --version

# Actualizar pip
python -m pip install --upgrade pip

# Ver contenido de carpeta
Get-ChildItem

# Ver tamaño de carpeta
(Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB

# Comprimir para envío (PowerShell 5.0+)
Compress-Archive -Path Practica_04_Proyecto_Final_OULAD -DestinationPath Caso_Practico_2_OULAD.zip

# Descomprimir
Expand-Archive Caso_Practico_2_OULAD.zip

# Abrir explorador aquí
explorer .
```

---

## 🔧 Si hay problemas

**Error: "Python no es reconocido"**
```powershell
# Instala Python desde: python.org
# Marca: "Add Python to PATH"
# Reinicia PowerShell/CMD después
```

**Error: "No se puede ejecutar scripts"**
```powershell
# Ejecuta como administrador:
# Win + X → Windows PowerShell (Admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Error: pip no funciona**
```powershell
python -m pip install --upgrade pip
```

**PostgreSQL no conecta (NORMAL)**
```powershell
# Es esperado si no tienes PostgreSQL
# El flag --skip-postgres lo ignora automáticamente
```

**El script .bat no se abre**
```powershell
# Intenta ejecutarlo así:
cmd /c run_windows.bat --skip-postgres
```

---

## 📊 Verificación visual en Windows

Después de ejecutar, deberías ver:

```
Practica_04_Proyecto_Final_OULAD\
├── outputs\
│   ├── figures\
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
└── docs\
    └── Articulo_Cientifico_OULAD_APA7.docx ✓
```

---

## ✅ Checklist Final para Windows

- [ ] Descargué el proyecto
- [ ] Abrí PowerShell/CMD en la carpeta
- [ ] Ejecuté `run_windows.bat --skip-postgres`
- [ ] Verifiqué que no hay errores (todo dice ✓)
- [ ] Abrí `outputs\figures\` - veo 8 imágenes PNG
- [ ] Abrí `outputs\` - veo archivos CSV
- [ ] Abrí `docs\Articulo_Cientifico_OULAD_APA7.docx`
- [ ] Grabé video colaborativo (2-5 min) en Zoom/OBS
- [ ] Inserté enlace de video en el documento
- [ ] Presioné Ctrl+S para guardar
- [ ] Comprimí la carpeta a ZIP (`Caso_Practico_2_OULAD.zip`)
- [ ] Subí documentos en aula virtual ANTES del 20 junio 23:59

---

## 🎯 Archivos principales para enviar

**1. Documento APA (PRINCIPAL):**
```
docs\Articulo_Cientifico_OULAD_APA7.docx
```

**2. ZIP con todo el código (RESPALDO):**
```
Caso_Practico_2_OULAD.zip
```

---

## 📍 Ruta completa del documento

```
/PATH/CienciaDatosUasd2026\Unidad_4\Practica_04_Proyecto_Final_OULAD\docs\Articulo_Cientifico_OULAD_APA7.docx
```

O simplemente en PowerShell:
```powershell
start docs\Articulo_Cientifico_OULAD_APA7.docx
```

---

**¡Listo! El documento APA está listo para enviar!** 🎉

**Próximo paso:** Inserta el video colaborativo y envía antes del 20 junio 23:59
