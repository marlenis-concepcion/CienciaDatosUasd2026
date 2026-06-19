import numpy as np
import pandas as pd

from src.features import FeatureEngineer, imd_midpoint


def raw_frame():
    return pd.DataFrame({
        "id_student": [1, 2, 3],
        "code_module": ["AAA", "BBB", "CCC"],
        "gender": ["F", "M", "F"],
        "disability": ["N", "Y", "N"],
        "highest_education": [
            "No Formal quals",
            "HE Qualification",
            "Post Graduate Qualification",
        ],
        "age_band": ["0-35", "35-55", "55<="],
        "imd_band": ["0-10%", "50-60%", np.nan],
        "num_of_prev_attempts": [0, 1, 2],
        "studied_credits": [60, 90, 120],
        "final_result": ["Withdrawn", "Pass", "Distinction"],
        "clicks_28d": [np.nan, 25, 80],
        "dias_activos_28d": [np.nan, 4, 12],
        "promedio_evaluaciones": [np.nan, 65, 88],
        "fuente": ["prueba"] * 3,
    })


def test_imd_midpoint_parses_valid_bands():
    assert imd_midpoint("0-10%") == 5
    assert imd_midpoint("90-100%") == 95


def test_imd_midpoint_returns_nan_for_missing_or_invalid_values():
    assert np.isnan(imd_midpoint(np.nan))
    assert np.isnan(imd_midpoint("desconocido"))


def test_feature_engineer_maps_targets_and_fills_early_activity():
    result = FeatureEngineer().transform(raw_frame())
    assert result["clicks_28d"].tolist() == [0, 25, 80]
    assert result["dias_activos_28d"].tolist() == [0, 4, 12]
    assert result["aprobo"].tolist() == [0, 1, 1]
    assert result["resultado_ordinal"].tolist() == [0, 2, 3]
    assert result["educacion_ordinal"].tolist() == [0, 3, 4]
    assert result["edad_ordinal"].tolist() == [0, 1, 2]


def test_feature_engineer_drops_unknown_final_result():
    frame = raw_frame()
    frame.loc[1, "final_result"] = "Pending"
    result = FeatureEngineer().transform(frame)
    assert result["id_student"].tolist() == [1, 3]


def test_feature_engineer_preserves_missing_imd_for_pipeline_imputation():
    result = FeatureEngineer().transform(raw_frame())
    assert np.isnan(result.loc[result["id_student"] == 3, "imd_midpoint"]).all()
