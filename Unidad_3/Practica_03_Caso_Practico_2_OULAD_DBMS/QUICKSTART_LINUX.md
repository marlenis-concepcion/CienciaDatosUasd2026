# QuickStart - Linux (Ubuntu, Debian, Fedora)

**⏱️ 5 minutos para empezar**

---

## PASO 1: Navega a la carpeta

```bash
cd /PATH/CienciaDatosUasd2026/Unidad_4/Practica_04_Proyecto_Final_OULAD
```

O si no sabes la ruta exacta:
```bash
find ~ -name "Practica_04_Proyecto_Final_OULAD" -type d
```

---

## PASO 2: Ejecuta el script automático

```bash
chmod +x run_unix.sh
./run_unix.sh --skip-postgres
```

**¿Qué hace?**
- ✅ Crea ambiente virtual
- ✅ Instala dependencias
- ✅ Descarga OULAD
- ✅ Genera EDA (gráficos + CSV)
- ✅ Crea paper APA

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

```bash
# Ver gráficos generados
ls -lh outputs/figures/

# Ver análisis CSV
ls -lh outputs/*.csv

# Ver paper APA
ls -lh docs/Articulo_Cientifico_OULAD_APA7.docx
```

---

## PASO 5: Grabar video colaborativo

```bash
# Usar cualquier herramienta:
# - Zoom: zoom (instalado)
# - OBS Studio: obs
# - SimpleScreenRecorder: simplescreenrecorder

obs  # Si tienes OBS instalado
```

Guardar como: `video_colaboracion.mp4`

---

## PASO 6: Insertar en documento y enviar

```bash
# Abrir documento
libreoffice docs/Articulo_Cientifico_OULAD_APA7.docx &

# O usar archivo manager
nautilus docs/
```

Entonces:
1. Abrir documento
2. Insertar enlace de video
3. Guardar
4. Enviar en aula virtual

---

## ⚡ Comandos útiles para Linux

```bash
# Ver espacio disponible
df -h

# Ver uso de memoria
free -h

# Descomprimir ZIP
unzip Caso_Practico_2_OULAD.zip

# Comprimir para envío
zip -r Caso_Practico_2_OULAD.zip Practica_04_Proyecto_Final_OULAD/

# Abrir archivo manager
nautilus .
```

---

## 🔧 Si hay problemas

**Error: Python no encontrado**
```bash
python3 --version
# Si no funciona: sudo apt install python3 python3-pip
```

**Error: pip no instala**
```bash
python3 -m pip install --upgrade pip
```

**Error: Permisos en script**
```bash
chmod +x run_unix.sh
```

---

## ✅ Checklist Final

- [ ] Descargué el proyecto
- [ ] Ejecuté `./run_unix.sh --skip-postgres`
- [ ] Se generaron outputs/figures/ (8 PNG)
- [ ] Se generaron CSV análisis
- [ ] El paper APA se creó
- [ ] Grabé video colaborativo
- [ ] Inserté enlace en documento
- [ ] Comprimí con ZIP
- [ ] Subí en aula virtual antes 20 junio 23:59

---

**¡Listo! Documento APA está en:** `docs/Articulo_Cientifico_OULAD_APA7.docx`
