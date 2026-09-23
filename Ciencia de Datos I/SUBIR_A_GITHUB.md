# 🚀 INSTRUCCIONES PARA SUBIR A GITHUB

**Estado:** ✅ Local Git está LISTO  
**Commit:** `Caso Práctico 2: OULAD en Base de Datos - Schema DDL, ETL, EDA extendido, Paper APA`

---

## 📋 PASO 1: Crear Repositorio en GitHub

1. Abre: https://github.com/new
2. Rellena:
   - **Repository name:** `CienciaDatosUasd2026`
   - **Description:** `Ciencia de Datos I - UASD Caso Práctico 2 OULAD`
   - **Public** ✓ (para que sea visible)
   - **NO inicialices con README** (ya tenemos)
3. Haz clic en **"Create repository"**

---

## 🔗 PASO 2: Conectar Local → GitHub

Ejecuta estos comandos en Terminal (en la carpeta del proyecto):

```bash
cd /PATH/CienciaDatosUasd2026

# Reemplaza [TU-USUARIO] con tu usuario de GitHub
git remote add origin https://github.com/[TU-USUARIO]/CienciaDatosUasd2026.git

# Cambiar rama a main
git branch -M main

# Hacer push
git push -u origin main
```

---

## ✅ PASO 3: Verificar en GitHub

Después de hacer push:

1. Ve a tu repositorio: `https://github.com/[TU-USUARIO]/CienciaDatosUasd2026`
2. Deberías ver:
   - ✅ Carpeta `Unidad_3/` con el documento APA
   - ✅ Carpeta `Unidad_4/` con código fuente
   - ✅ Archivo `.gitignore`
   - ✅ Archivos de documentación

---

## 📦 CONTENIDO QUE SE SUBE

```
CienciaDatosUasd2026/
│
├── 📄 Documento Principal (ENTREGA UASD):
│   └── Unidad_3/Practica_03_Caso_Practico_2_OULAD_DBMS/
│       └── Caso_Practico_2_OULAD_DBMS.docx    ← ⭐ ESTO
│
├── 💾 Código Fuente Completo:
│   └── Unidad_4/Practica_04_Proyecto_Final_OULAD/
│       ├── sql/01_schema_oulad.sql
│       ├── src/db_loader.py
│       ├── src/eda_extended.py
│       ├── scripts/generate_apa_paper.py
│       ├── docs/Articulo_Cientifico_OULAD_APA7.docx
│       ├── etl_orchestrator.py
│       ├── requirements.txt
│       ├── run_unix.sh
│       ├── run_windows.bat
│       └── QUICKSTART_*.md
│
├── 📚 Documentación:
│   ├── README.md (crear en GitHub)
│   ├── .gitignore (archivos a ignorar)
│   └── GUIAS/ (QUICKSTART por SO)
│
└── ⚙️ Configuración:
    └── outputs/ y *.csv (IGNORADOS - no suben)
```

---

## 🎯 LO QUE NO SE SUBE (gracias a .gitignore)

❌ `outputs/` (resultados random)  
❌ `*.csv` (datos procesados)  
❌ `*.png` (gráficos generados)  
❌ `.venv/` (ambiente virtual)  
❌ `credentials.json` (credenciales)  
❌ `*.pyc` (archivos compilados)  
❌ `.DS_Store` (archivos del SO)

---

## 🔄 COMANDO RÁPIDO (Copiar y Pegar)

```bash
cd /PATH/CienciaDatosUasd2026
git remote add origin https://github.com/REEMPLAZA_TU_USUARIO_AQUI/CienciaDatosUasd2026.git
git branch -M main
git push -u origin main
```

---

## ⚠️ SI SALE ERROR

### "fatal: The remote origin already exists"
```bash
git remote remove origin
# Luego intenta de nuevo
```

### "Permission denied (publickey)"
Configura tu SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "Updates were rejected"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## ✨ DESPUÉS DE SUBIR

1. **En GitHub:** Crea un `README.md` bonito
2. **En Aula Virtual:** Sube el documento APA + ZIP
3. **Listo:** Ambos entregables completados

---

## 📊 ESTADO ACTUAL

```
✅ Proyecto local: COMPLETADO
✅ Git inicializado: COMPLETADO
✅ Commit hecho: COMPLETADO
⏳ Push a GitHub: PENDIENTE
```

---

**Próximo paso:** Ejecuta los comandos del PASO 2 👆

---

*Documento actualizado: 14 de junio de 2026*
