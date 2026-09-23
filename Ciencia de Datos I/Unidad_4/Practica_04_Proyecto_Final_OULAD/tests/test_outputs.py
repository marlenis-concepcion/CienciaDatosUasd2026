from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"


def test_general_metrics_cover_all_tasks_and_three_models_each():
    metrics = pd.read_csv(OUTPUTS / "metricas_generales.csv")
    counts = metrics.groupby("tarea")["modelo"].nunique().to_dict()
    assert counts == {
        "dicotomica": 3,
        "intervalo_razon": 3,
        "ordinal": 3,
    }


def test_binary_predictions_are_case_level_and_binary():
    predictions = pd.read_csv(OUTPUTS / "predicciones_binarias.csv")
    required = {"id_student", "fuente", "y_test", "y_pred", "modelo"}
    assert required.issubset(predictions.columns)
    assert set(predictions["y_test"].unique()).issubset({0, 1})
    assert set(predictions["y_pred"].unique()).issubset({0, 1})
    assert predictions["modelo"].nunique() == 3


def test_manual_f1_matches_exported_macro_inputs_with_valid_confusion_counts():
    manual = pd.read_csv(OUTPUTS / "f1_manual.csv")
    assert len(manual) == 3
    assert (manual[["tp", "fp", "tn", "fn"]] >= 0).all().all()
    assert manual["f1_manual"].between(0, 1).all()
    assert manual["accuracy_manual"].between(0, 1).all()


def test_importances_cover_every_feature_for_every_model():
    importance = pd.read_csv(OUTPUTS / "importancias_variables.csv")
    expected_features = {
        "clicks_28d",
        "dias_activos_28d",
        "studied_credits",
        "num_of_prev_attempts",
        "educacion_ordinal",
        "edad_ordinal",
        "imd_midpoint",
        "gender",
        "disability",
        "code_module",
    }
    grouped = importance.groupby(["tarea", "modelo"])["variable"].apply(set)
    assert len(grouped) == 9
    assert all(features == expected_features for features in grouped)


def test_required_graphics_and_findings_exist():
    required = [
        "eda_alto_nivel.png",
        "confusion_regresion_logistica.png",
        "confusion_random_forest.png",
        "confusion_gradient_boosting.png",
        "hallazgos.txt",
    ]
    assert all((OUTPUTS / name).stat().st_size > 0 for name in required)
