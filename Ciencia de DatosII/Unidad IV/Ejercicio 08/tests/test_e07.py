from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from inf8239_u04.data import load_data, temporal_split
from inf8239_u04.evaluation import bootstrap_gaps, choose, final_decision, flag_small_cells, rule_baseline
from inf8239_u04.impact import score_risks, validate_impact

ROOT = Path(__file__).resolve().parents[1]
GATES = {"min_recall": 0.68, "max_recall_gap": 0.16, "max_fpr_gap": 0.16}


def test_student_impact_assessment_is_complete():
    impact = yaml.safe_load((ROOT / "student_inputs/lab11_impact.yml").read_text(encoding="utf-8"))
    assert validate_impact(impact)
    assert "revisión" in impact["assisted_decision"].lower()


def test_risk_register_is_complete_and_linked_to_nist_rmf():
    risks = score_risks(pd.read_csv(ROOT / "student_inputs/risk_register.csv"))
    assert len(risks) >= 8
    assert risks["rmf_subcategory"].str.match(r"^(GOVERN|MAP|MEASURE|MANAGE) \d+\.\d+$").all()
    assert set(risks["rmf_subcategory"].str.split().str[0]) == {"GOVERN", "MAP", "MEASURE", "MANAGE"}
    assert risks["priority"].is_monotonic_decreasing


def test_stakeholders_include_affected_people_without_placeholders():
    stake = pd.read_csv(ROOT / "student_inputs/stakeholders.csv")
    assert "Affected person" in set(stake["stakeholder"])
    assert not stake.astype(str).apply(lambda s: s.str.contains("REPLACE")).any().any()


def test_normative_matrix_separates_legal_voluntary_and_ethical():
    text = (ROOT / "docs/MARCO_NORMATIVO.md").read_text(encoding="utf-8")
    for label in ["**Obligación legal**", "**Marco voluntario**", "**Recomendación ética**"]:
        assert label in text
    assert "172-13" in text and "NIST AI 100-1" in text


def test_protected_attribute_is_not_a_model_or_rule_input():
    df = load_data()
    changed = df.assign(protected_group=np.where(df.protected_group == "G1", "G2", "G1"))
    np.testing.assert_array_equal(rule_baseline(df), rule_baseline(changed))


def test_bootstrap_interval_contains_the_observed_gap():
    y = np.array([1, 1, 0, 0] * 25)
    pred = np.array([1, 0, 0, 1] * 25)
    groups = np.array(["G1"] * 50 + ["G2"] * 50)
    ci = bootstrap_gaps(y, pred, groups, n=200)
    assert ci["recall_gap"][0] <= ci["recall_gap"][1]
    assert 0 <= ci["recall_gap"][0] and ci["fpr_gap"][1] <= 1


def test_small_intersectional_cells_are_flagged():
    table = pd.DataFrame({"count": [8, 35]}, index=["G2 | 45-59", "G1 | 45-59"])
    assert flag_small_cells(table)["n_suficiente"].tolist() == [False, True]


def test_choice_excludes_threshold_optimizer_that_uses_protected_group():
    table = pd.DataFrame({"etapa": ["validacion"] * 2, "candidato": ["threshold_optimizer_eo", "logistica_0.50"],
                          "recall": [0.99, 0.80], "recall_gap": [0.0, 0.1], "fpr_gap": [0.0, 0.1]})
    assert choose(table, GATES)[0] == "logistica_0.50"


@pytest.mark.parametrize("row,ci,small,expected", [
    ({"recall": 0.80, "recall_gap": 0.05, "fpr_gap": 0.05}, {"recall_gap": [0, 0.1], "fpr_gap": [0, 0.1]}, 0, "desplegar"),
    ({"recall": 0.80, "recall_gap": 0.05, "fpr_gap": 0.05}, {"recall_gap": [0, 0.3], "fpr_gap": [0, 0.1]}, 0, "limitar"),
    ({"recall": 0.80, "recall_gap": 0.30, "fpr_gap": 0.05}, {"recall_gap": [0, 0.4], "fpr_gap": [0, 0.1]}, 0, "modificar"),
    ({"recall": 0.50, "recall_gap": 0.05, "fpr_gap": 0.05}, {"recall_gap": [0, 0.1], "fpr_gap": [0, 0.1]}, 0, "no utilizar"),
])
def test_final_decision_maps_evidence_to_four_options(row, ci, small, expected):
    assert final_decision(pd.Series(row), ci, GATES, small)["decision"] == expected


def test_temporal_split_keeps_future_cases_in_test():
    train, test = temporal_split(load_data())
    assert train.received_date.max() <= test.received_date.min()
