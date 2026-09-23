from math import isclose

from src.domain import ModelResult, ResultRegistry, TaskType
from src.metrics import manual_binary_metrics, multiclass_mse_r2


def test_manual_f1_from_confusion_counts():
    result = manual_binary_metrics(
        [1, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0],
    )
    assert result["tp"] == 2
    assert result["fp"] == 1
    assert result["tn"] == 2
    assert result["fn"] == 1
    assert isclose(result["precision_manual"], 2 / 3)
    assert isclose(result["recall_manual"], 2 / 3)
    assert isclose(result["f1_manual"], 2 / 3)


def test_result_registry_groups_by_task():
    registry = ResultRegistry()
    registry.add(ModelResult(TaskType.BINARY, "modelo_a", {"f1": 0.8}, [1]))
    registry.add(ModelResult(TaskType.REGRESSION, "modelo_b", {"r2": 0.5}, [10]))
    assert len(registry.by_task(TaskType.BINARY)) == 1
    assert registry.by_task(TaskType.BINARY)[0].model == "modelo_a"


def test_manual_metrics_when_there_are_no_positive_predictions():
    result = manual_binary_metrics([0, 0, 1, 1], [0, 0, 0, 0])
    assert result["tp"] == 0
    assert result["fp"] == 0
    assert result["fn"] == 2
    assert result["precision_manual"] == 0
    assert result["recall_manual"] == 0
    assert result["f1_manual"] == 0
    assert result["accuracy_manual"] == 0.5


def test_multiclass_mse_r2_for_perfect_prediction():
    mse, r2 = multiclass_mse_r2([0, 1, 2, 3], [0, 1, 2, 3])
    assert mse == 0
    assert r2 == 1


def test_multiclass_r2_handles_constant_target():
    mse, r2 = multiclass_mse_r2([2, 2, 2], [1, 2, 3])
    assert isclose(mse, 2 / 3)
    assert r2 == 0
