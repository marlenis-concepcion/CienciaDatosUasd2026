import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from tutoria_dss.config import ROOT
from tutoria_dss.data import allowed_features, load, split
from tutoria_dss.dss import SUPPORTS, explain, prioritize, readable, record_decision, support_type
from tutoria_dss.models import build_logistic, contributions, predict_risk

BASE = {"Debtor": 0, "Tuition fees up to date": 1, "Curricular units 1st sem (approved)": 5}


@pytest.fixture(scope="module")
def cohort():
    parts = split(load())
    model = build_logistic().fit(parts["train"][allowed_features()], parts["train"]["abandono"])
    test = parts["test"]
    return test, predict_risk(model, test), contributions(model, test)


@pytest.mark.parametrize("change,expected", [
    ({"Debtor": 1}, SUPPORTS["financiera"]),
    ({"Tuition fees up to date": 0, "Curricular units 1st sem (approved)": 0}, SUPPORTS["financiera"]),
    ({"Curricular units 1st sem (approved)": 0}, SUPPORTS["academica"]),
    ({}, SUPPORTS["seguimiento"]),
])
def test_support_rules_are_explicit_and_ordered(change, expected):
    assert support_type(pd.Series({**BASE, **change})) == expected


def test_priority_list_respects_capacity_and_is_sorted(cohort):
    test, risk, contrib = cohort
    table = prioritize(test, risk, 0.15, contrib)
    assert len(table) == int(np.ceil(0.15 * len(test)))
    assert table["riesgo"].is_monotonic_decreasing
    assert table["prioridad"].tolist() == list(range(1, len(table) + 1))


def test_priority_list_contains_the_highest_risk_students(cohort):
    test, risk, _ = cohort
    table = prioritize(test, risk, 0.15)
    assert table["riesgo"].min() >= np.sort(risk)[::-1][len(table) - 1] - 1e-9


def test_every_prioritized_student_gets_support_and_explanation(cohort):
    test, risk, contrib = cohort
    table = prioritize(test, risk, 0.15, contrib)
    assert table["apoyo_sugerido"].isin(SUPPORTS.values()).all()
    assert table["por_que"].str.len().gt(0).all()


def test_explanations_never_mention_sensitive_attributes(cohort):
    test, risk, contrib = cohort
    text = " ".join(prioritize(test, risk, 0.40, contrib)["por_que"]).lower()
    for word in ["gender", "género", "age", "edad", "nacional", "becario", "scholarship", "marital"]:
        assert word not in text


def test_explanation_lists_only_risk_increasing_factors():
    contrib = pd.DataFrame({"num__Debtor": [0.8, -0.2], "num__Admission grade": [-0.5, -0.1]})
    rows = pd.DataFrame({"Debtor": [1, 0], "Admission grade": [120.0, 150.0]})
    assert explain(contrib, rows) == ["deuda con la institución = 1", "sin factores de riesgo destacados"]
    assert readable("cat__Course_9500") == "carrera (código) = 9500"


def test_human_decision_log_requires_reason_and_owner(tmp_path):
    row = pd.Series({"student_id": "E0001", "prioridad": 1, "apoyo_sugerido": SUPPORTS["academica"]})
    log = tmp_path / "log.csv"
    with pytest.raises(ValueError, match="motivo"):
        record_decision(log, row, "rechazar", "", "", "Coordinadora")
    with pytest.raises(ValueError, match="responsable"):
        record_decision(log, row, "aceptar", SUPPORTS["academica"], "", " ")
    record_decision(log, row, "aceptar", SUPPORTS["academica"], "", "Coordinadora")
    saved = record_decision(log, row, "modificar", SUPPORTS["financiera"], "Tiene beca en trámite", "Coordinadora")
    assert len(saved) == 2 and saved.iloc[1]["apoyo_final"] == SUPPORTS["financiera"]


def test_streamlit_app_starts_and_warns_about_human_decision():
    if not (ROOT / "models/logistica.joblib").exists():
        pytest.skip("modelo no entrenado")
    app = AppTest.from_file(str(ROOT / "app/streamlit_app.py"), default_timeout=60).run()
    assert not app.exception
    assert any("coordinación decide" in w.value for w in app.warning)
