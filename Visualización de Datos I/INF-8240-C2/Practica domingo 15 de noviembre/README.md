# Práctica del domingo 15 de noviembre · Storytelling de ventas y producción

**Materia:** Visualización de Datos I · INF-8240-C2 · UASD
**Estudiante:** Marlenis Judith Concepción Cuevas

Historia de datos de Industrias Caribe en 2025 sobre las ventas y las unidades producidas, construida a partir de `IndustriasCaribe_Tablas.xlsx` (hojas Ventas y Produccion).

- **Página interactiva (artifact):** https://claude.ai/artifact/JLkBDUME7SX54FiNSf1xFa
- **Contenido:**
  - Seis capítulos que avanzan con el scroll: el año en ventas, las plantas, la brecha entre producido y vendido, el ritmo mensual, la comparación por producto y el valor.
  - Una sección de turnos con mejor desempeño de unidades producidas.
  - Ocho gráficos adicionales: región, canal, descuento, mapa de calor por producto y mes, turnos, plantas, defectos e ingreso frente a costo.

## Archivos

| Archivo | Uso |
|---|---|
| `index.html`, `turnos.js`, `extra.js` | Copia de la página publicada (se ejecuta dentro del artifact, que aporta los datos y la librería d3) |
| `exportar_csv.py` | Exporta las hojas Ventas y Produccion del Excel a CSV |
| `analisis.py` | Calcula los totales usados para redactar la historia (`resumen.json`) |

Los scripts buscan `IndustriasCaribe_Tablas.xlsx` en la carpeta de la materia. Los CSV y el JSON generados no se suben al repositorio.

```sh
python3 exportar_csv.py
python3 analisis.py
```
