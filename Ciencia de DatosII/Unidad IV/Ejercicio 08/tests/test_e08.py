import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from inf8239_u04.data import load_data, temporal_split
from inf8239_u04.lifecycle import (apply_retention, check_inputs, check_performance, load_inventory, minimize, psi,
                                   respond, sha256)

ROOT = Path(__file__).resolve().parents[1]
LIMITS = yaml.safe_load((ROOT / "configs/governance.yml").read_text(encoding="utf-8"))["monitoring"]


def test_inventory_covers_every_column_with_purpose_and_retention():
    inventory = load_inventory()
    assert set(inventory["column"]) == set(load_data().columns)
    assert inventory[["purpose", "retention", "sensitivity"]].notna().all().all()


def test_operational_view_excludes_sensitive_and_unneeded_columns():
    operational = minimize(load_data(), load_inventory(), "operational")
    assert set(operational.columns) == {"case_id", "received_date", "previous_incidents", "exposure"}
    assert not {"protected_group", "age_band", "zone", "target"} & set(operational.columns)


def test_minimize_rejects_columns_missing_from_inventory():
    with pytest.raises(ValueError, match="sin inventario"):
        minimize(load_data().assign(phone_hash="x"), load_inventory(), "audit")


def test_retention_deletes_only_cases_older_than_the_limit():
    df = pd.DataFrame({"received_date": pd.to_datetime(["2025-01-10", "2026-03-01", "2026-06-15"])})
    kept, deleted = apply_retention(df, "2026-12-31", months=12)
    assert deleted == 1 and kept["received_date"].min() == pd.Timestamp("2026-03-01")


def test_datasheet_and_model_card_hash_match_the_current_dataset():
    digest = sha256(ROOT / "data/territorial_risk_synthetic.csv")
    for doc in ["docs/DATASHEET.md", "docs/MODEL_CARD.md"]:
        assert digest in (ROOT / doc).read_text(encoding="utf-8")


def test_manifest_hashes_match_files_on_disk():
    manifest = json.loads((ROOT / "reports/lab13/manifest.json").read_text(encoding="utf-8"))
    for entry in manifest.values():
        assert sha256(ROOT / entry["path"]) == entry["sha256"], entry["path"]


def test_raci_has_exactly_one_accountable_and_covers_critical_activities():
    raci = pd.read_csv(ROOT / "student_inputs/raci.csv")
    assert raci["A"].str.split(" and ").str.len().eq(1).all()
    assert raci["activity"].is_unique
    text = " ".join(raci["activity"]).lower()
    for activity in ["retención", "incidentes", "apelaciones", "monitoreo", "minimización"]:
        assert activity in text


def test_input_monitor_is_quiet_on_normal_weeks_and_detects_scale_bug():
    train, test = temporal_split(load_data())
    for _, week in test.groupby(test.received_date.dt.to_period("W")):
        assert respond(check_inputs(week, train, LIMITS)) == "OK"
    broken = test.head(12).assign(exposure=lambda d: d.exposure * 0.1)
    assert respond(check_inputs(broken, train, LIMITS)) == "CONTENER"


def test_performance_monitor_does_not_alert_on_small_windows():
    window = pd.DataFrame({"target": [1, 0] * 10, "protected_group": ["G1", "G2"] * 10})
    result = check_performance(window, np.zeros(20, dtype=int), LIMITS)
    assert result["alerts"] == ["ventana insuficiente: solo informativo"]
    assert respond({"alerts": []}, result) == "OK"


def test_psi_is_zero_for_same_distribution_and_grows_with_shift():
    x = np.random.default_rng(0).random(500)
    assert psi(x, x) == pytest.approx(0, abs=1e-9)
    assert psi(x, x * 0.1) > 1


def test_runbook_and_postmortem_are_complete_with_owners_and_dates():
    runbook = (ROOT / "docs/RUNBOOK.md").read_text(encoding="utf-8")
    assert "REPLACE" not in runbook and len(re.findall(r"^\d\. \*\*", runbook, re.M)) == 6
    postmortem = (ROOT / "reports/lab13/INCIDENT_POSTMORTEM.md").read_text(encoding="utf-8")
    assert "REPLACE" not in postmortem
    assert len(re.findall(r"\| \d{4}-\d{2}-\d{2} \|", postmortem)) >= 3
