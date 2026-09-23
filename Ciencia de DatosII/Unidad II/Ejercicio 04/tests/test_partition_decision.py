import numpy as np
import pytest

from inf8239_u02_cv.data import audit_arrays, split_train_valid
from inf8239_u02_cv.evaluation import choose, per_class, top_confusions


def test_validation_split_is_disjoint_stratified_and_reproducible():
    y = np.repeat(np.arange(10), 100)
    x = np.zeros((1000, 28, 28), dtype=np.uint8)
    train, valid = split_train_valid(x, y, valid_size=200, random_state=42)
    again, _ = split_train_valid(x, y, valid_size=200, random_state=42)
    assert not set(train) & set(valid)
    assert len(train) + len(valid) == 1000
    assert np.bincount(y[valid]).tolist() == [20] * 10
    np.testing.assert_array_equal(train, again)


def test_audit_detects_train_images_repeated_in_test():
    rng = np.random.default_rng(0)
    x_train = rng.integers(0, 255, (5, 28, 28), dtype=np.uint8)
    x_test = np.concatenate([x_train[:1], rng.integers(0, 255, (2, 28, 28), dtype=np.uint8)])
    audit = audit_arrays(x_train, np.arange(5), x_test, np.array([0, 1, 2]))
    assert audit["entrenamiento_repetido_en_prueba"] == 1
    assert audit["duplicados_en_entrenamiento"] == 0


def test_choose_prefers_cheaper_model_within_tolerance():
    valid = {"dense": {"f1_macro": 0.885, "parametros": 50_000},
             "cnn_flatten": {"f1_macro": 0.890, "parametros": 400_000}}
    assert choose(valid)[0] == "dense"
    valid["cnn_flatten"]["f1_macro"] = 0.93
    assert choose(valid)[0] == "cnn_flatten"


def test_per_class_and_confusions_count_errors():
    y_true = np.array([0, 0, 6, 6, 6])
    y_pred = np.array([0, 6, 0, 0, 6])
    table = per_class(y_true, y_pred)
    assert table.loc[6, "errores"] == 2
    assert top_confusions(y_true, y_pred).iloc[0].tolist() == ["Shirt", "T-shirt/top", 2]
