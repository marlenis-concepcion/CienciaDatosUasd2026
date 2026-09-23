import pandas as pd
import pytest

from tutoria_dss.baseline import rule_score
from tutoria_dss.data import SECOND_SEMESTER, SENSITIVE, allowed_features, load, split, validate


@pytest.fixture(scope="module")
def df():
    return load()


def test_dataset_contract_and_binary_target(df):
    assert len(df) == 4424
    assert df["student_id"].is_unique
    assert set(df["abandono"]) == {0, 1}


def test_contract_rejects_nulls_and_impossible_approvals(df):
    with pytest.raises(ValueError, match="nulos"):
        validate(df.assign(**{"Admission grade": None}))
    broken = df.copy()
    broken.loc[0, "Curricular units 1st sem (approved)"] = 99
    with pytest.raises(ValueError, match="aprobadas"):
        validate(broken)


def test_model_features_exclude_sensitive_and_second_semester():
    features = set(allowed_features())
    assert not features & set(SENSITIVE)
    assert not features & set(SECOND_SEMESTER)
    assert not any("2nd sem" in f for f in features)


def test_split_is_disjoint_complete_and_stratified(df):
    parts = split(df)
    ids = [set(p["student_id"]) for p in parts.values()]
    assert sum(len(i) for i in ids) == len(df) and len(set.union(*ids)) == len(df)
    for part in parts.values():
        assert abs(part["abandono"].mean() - df["abandono"].mean()) < 0.01


def test_rule_baseline_prioritizes_failed_units_and_unpaid_tuition():
    base = {"Curricular units 1st sem (enrolled)": 6, "Curricular units 1st sem (approved)": 6,
            "Tuition fees up to date": 1, "Debtor": 0}
    students = pd.DataFrame([base, {**base, "Curricular units 1st sem (approved)": 0},
                             {**base, "Tuition fees up to date": 0}])
    scores = rule_score(students)
    assert scores[0] < scores[1] and scores[0] < scores[2]
