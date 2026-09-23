# Traspaso entre roles

Cada traspaso tiene entregables, criterio de aceptación y quién firma. Ningún rol recibe un artefacto sin evidencia verificable.

| De → a | Entregables | Criterio de aceptación | Firma (A) |
|---|---|---|---|
| Data Engineer → Data Scientist | `data/territorial_risk_synthetic.csv`, `docs/data_inventory.csv`, hash en `reports/lab13/manifest.json` | El hash coincide; el esquema pasa `validate_schema`; no hay identificadores directos | Data Protection Officer |
| Data Scientist → Product Owner | `reports/lab12/` (auditoría y decisión), `docs/MODEL_CARD.md`, `docs/DATASHEET.md` | Compuertas documentadas; intervalos y celdas pequeñas reportados; decisión desplegar/modificar/limitar/no utilizar justificada | Product Owner |
| Product Owner → ML Engineer | Decisión firmada (`reports/lab11/DECISION_RECORD.md`), configuración (`configs/governance.yml`) | La configuración contiene usos prohibidos, compuertas, retención y umbrales de monitoreo | Institutional Owner |
| ML Engineer → Operators | Aplicación (`app.py`), guía de uso, canal de apelación, `docs/RUNBOOK.md` | Los operadores saben que la lista solo ordena revisiones; saben cómo registrar discrepancias y activar el runbook | Product Owner |
| Operators → Data Scientist (ciclo) | Resultados de revisión (target), discrepancias y apelaciones | Se incorporan en la ventana de desempeño y en la auditoría mensual | Product Owner |
