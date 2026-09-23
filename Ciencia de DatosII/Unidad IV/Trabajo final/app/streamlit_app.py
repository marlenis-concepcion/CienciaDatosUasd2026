"""Aplicación del DSS para la coordinación de tutorías (datos públicos de Portugal; demostración académica)."""
from pathlib import Path

import joblib
import streamlit as st

from tutoria_dss.config import ROOT, load_config
from tutoria_dss.data import load, split
from tutoria_dss.dss import SUPPORTS, prioritize, record_decision
from tutoria_dss.fairness import audit_groups
from tutoria_dss.models import contributions, predict_risk

MODEL = ROOT / "models/logistica.joblib"
LOG = ROOT / "reports/decisiones_coordinacion.csv"

st.set_page_config(page_title="DSS de tutoría temprana", layout="wide")
st.title("DSS de alerta temprana para tutoría")
st.warning("Demostración académica con datos públicos (UCI 697, Portugal). La lista propone a quién contactar; "
           "la coordinación decide. No se usa para sancionar, excluir ni condicionar becas.")
if not MODEL.exists():
    st.error("Entrene el modelo: uv run python scripts/train.py")
    st.stop()
cfg = load_config()
model = joblib.load(MODEL)
cohort = split(load(), cfg["random_state"])["test"]
share = st.slider("Cupos de tutoría (proporción de la cohorte)", 0.05, 0.40, float(cfg["capacity_share"]), 0.01)
quota = st.checkbox("Repartir cupos por grupo de edad (mitigación elegida en validación; el modelo no usa la edad)",
                    value=True)
risk = predict_risk(model, cohort)
table = prioritize(cohort, risk, share, contributions(model, cohort),
                   audit_groups(cohort)["edad"] if quota else None)
st.caption(f"Cohorte de demostración: {len(cohort)} estudiantes · cupos: {len(table)} · "
           "variables sensibles fuera del modelo · punto de decisión: fin del primer semestre")
st.dataframe(table.round({"riesgo": 3}), use_container_width=True, hide_index=True)

st.subheader("Registrar decisión de la coordinación")
choice = st.selectbox("Estudiante", table["student_id"])
row = table[table.student_id == choice].iloc[0]
decision = st.radio("Decisión", ["aceptar", "modificar", "rechazar"], horizontal=True)
final = st.selectbox("Apoyo final", list(SUPPORTS.values()), index=list(SUPPORTS.values()).index(row["apoyo_sugerido"]))
reason = st.text_input("Motivo (obligatorio si modifica o rechaza)")
owner = st.text_input("Responsable")
if st.button("Guardar decisión"):
    try:
        log = record_decision(LOG, row, decision, final, reason, owner)
        st.success(f"Decisión guardada. Registros: {len(log)}")
    except ValueError as error:
        st.error(str(error))
