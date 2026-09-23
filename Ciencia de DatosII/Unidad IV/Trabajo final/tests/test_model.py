import numpy as np
import pandas as pd
import pytest

from tutoria_dss.data import allowed_features, load, split
from tutoria_dss.evaluation import at_capacity, choose, top_k_mask
from tutoria_dss.models import build_logistic, contributions, predict_risk


@pytest.fixture(scope="module")
def fitted():
    parts = split(load())
    model = build_logistic().fit(parts["train"][allowed_features()], parts["train"]["abandono"])
    return model, parts


def test_model_outputs_valid_probabilities(fitted):
    model, parts = fitted
    risk = predict_risk(model, parts["valid"])
    assert risk.shape == (len(parts["valid"]),) and ((risk >= 0) & (risk <= 1)).all()


def test_scaler_is_fitted_only_on_training_data(fitted):
    model, parts = fitted
    scaler = model.named_steps["prep"].named_transformers_["num"]
    column = model.named_steps["prep"].transformers_[1][2].index("Admission grade")
    assert scaler.mean_[column] == pytest.approx(parts["train"]["Admission grade"].mean())


def test_model_ignores_sensitive_columns_even_if_they_change(fitted):
    model, parts = fitted
    changed = parts["valid"].assign(Gender=1 - parts["valid"]["Gender"], **{"Age at enrollment": 70})
    np.testing.assert_allclose(predict_risk(model, parts["valid"]), predict_risk(model, changed))


def test_contributions_add_up_to_the_logit(fitted):
    model, parts = fitted
    sample = parts["valid"].head(5)
    logit = contributions(model, sample).sum(axis=1) + model.named_steps["model"].intercept_[0]
    np.testing.assert_allclose(1 / (1 + np.exp(-logit)), predict_risk(model, sample), rtol=1e-6)


def test_top_k_selects_exactly_capacity_and_highest_scores():
    mask = top_k_mask(np.array([0.1, 0.9, 0.5, 0.8]), 0.5)
    assert mask.tolist() == [False, True, False, True]


def test_capacity_metrics_match_hand_calculation():
    result = at_capacity(np.array([1, 1, 0, 0]), np.array([0.9, 0.2, 0.8, 0.1]), 0.5)
    assert result["aciertos"] == 1 and result["precision_capacidad"] == 0.5 and result["recall_capacidad"] == 0.5


def test_choice_ignores_random_reference_and_uses_recall_then_ap():
    table = pd.DataFrame({"alternativa": ["aleatorio", "reglas", "logistica"], "recall_capacidad": [0.9, 0.4, 0.4],
                          "average_precision": [0.9, 0.5, 0.7]})
    assert choose(table) == "logistica"
