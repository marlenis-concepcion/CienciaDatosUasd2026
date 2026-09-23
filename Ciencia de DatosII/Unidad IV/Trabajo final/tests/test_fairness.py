import numpy as np
import pandas as pd
import pytest

from tutoria_dss.data import load, split
from tutoria_dss.dss import prioritize
from tutoria_dss.fairness import (age_band, allocate_by_group, audit_groups, by_group, choose_mitigation,
                                  gate_decision, recall_gap)

GATES = {"min_recall_at_capacity": 0.35, "max_recall_gap": 0.15, "min_group_size": 30}


def test_age_bands_cover_all_ages_without_gaps():
    bands = age_band(pd.Series([17, 20, 21, 25, 26, 70]))
    assert bands.tolist() == ["≤20", "≤20", "21-25", "21-25", ">25", ">25"]


def test_audit_groups_are_readable_and_complete():
    groups = audit_groups(split(load())["test"])
    assert set(groups["genero"]) == {"mujer", "hombre"} and set(groups["beca"]) == {"becario", "sin beca"}
    assert groups.notna().all().all()


def test_group_recall_matches_hand_calculation():
    table = by_group(np.array([1, 1, 1, 1, 0]), np.array([1, 0, 1, 1, 0], bool), pd.Series(list("aabbb")), 1)
    assert table.set_index("grupo")["recall_capacidad"].to_dict() == {"a": 0.5, "b": 1.0}
    assert recall_gap(table) == 0.5


def test_small_groups_do_not_count_in_the_gap():
    table = pd.DataFrame({"recall_capacidad": [0.9, 0.1, 0.5], "n_suficiente": [True, False, True]})
    assert recall_gap(table) == pytest.approx(0.4)


def test_quota_allocation_uses_exact_capacity_and_top_risk_within_group():
    scores = np.array([0.9, 0.8, 0.1, 0.7, 0.6, 0.5, 0.05, 0.02])
    groups = pd.Series(["a", "a", "a", "b", "b", "b", "c", "c"])
    selected = allocate_by_group(scores, groups, 0.5)
    assert selected.sum() == 4
    assert selected[0] and selected[1] and not selected[2]


def test_quota_gives_places_to_low_risk_groups_that_global_ranking_ignores():
    scores = np.array([0.9] * 10 + [0.3] * 10)
    groups = pd.Series(["alto"] * 10 + ["bajo"] * 10)
    selected = allocate_by_group(scores, groups, 0.25)
    assert selected[10:].sum() >= 1


def test_prioritized_list_with_quota_keeps_capacity():
    test = split(load())["test"]
    risk = np.linspace(0, 1, len(test))
    table = prioritize(test, risk, 0.15, quota_groups=audit_groups(test)["edad"])
    assert len(table) == int(np.ceil(0.15 * len(test)))


def test_mitigation_choice_prefers_best_recall_among_those_that_pass_gates():
    valid = pd.DataFrame({"alternativa": ["logistica", "cupos"], "recall_capacidad": [0.44, 0.42],
                          "brecha_genero": [0.05, 0.05], "brecha_edad": [0.30, 0.02], "brecha_beca": [0, 0]})
    assert choose_mitigation(valid, GATES) == "cupos"


@pytest.mark.parametrize("recall,gap,upper,expected", [
    (0.45, 0.05, 0.10, "desplegar"), (0.45, 0.05, 0.20, "limitar"),
    (0.45, 0.25, 0.30, "modificar"), (0.20, 0.05, 0.10, "no utilizar"),
])
def test_gate_decision_maps_to_four_options(recall, gap, upper, expected):
    assert gate_decision(recall, {"edad": gap}, {"edad": upper}, GATES)["decision"] == expected
