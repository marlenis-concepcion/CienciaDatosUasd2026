import numpy as np
import pytest

from inf8239_u03_gen.data import split_train_valid
from inf8239_u03_gen.evaluation import (choose, class_diversity, nearest_distances, pairwise_spread,
                                        reconstruction_errors)


def test_validation_split_is_disjoint_complete_and_reproducible():
    train, valid = split_train_valid(1000, valid_size=100, seed=42)
    again, _ = split_train_valid(1000, valid_size=100, seed=42)
    assert not set(train) & set(valid)
    assert len(train) + len(valid) == 1000
    np.testing.assert_array_equal(train, again)


def test_reconstruction_error_is_zero_for_perfect_copy_and_grows_with_noise():
    images = np.random.default_rng(0).integers(0, 2, (4, 28, 28, 1)).astype("float32")
    perfect = reconstruction_errors(images, images)
    noisy = reconstruction_errors(images, np.full_like(images, 0.5))
    assert perfect["mse_pixel"] == pytest.approx(0, abs=1e-10)  # el recorte a 1e-7 evita log(0)
    assert noisy["mse_pixel"] > perfect["mse_pixel"]
    assert noisy["bce_por_imagen"] > perfect["bce_por_imagen"]


def test_nearest_distance_detects_a_memorized_copy():
    rng = np.random.default_rng(1)
    train = rng.random((50, 28, 28, 1)).astype("float32")
    generated = np.concatenate([train[:1], rng.random((1, 28, 28, 1)).astype("float32")])
    distances = nearest_distances(generated, train, batch=1)
    assert distances[0] == pytest.approx(0, abs=1e-3)
    assert distances[1] > 1


def test_class_diversity_distinguishes_collapse_from_variety():
    collapsed = np.tile(np.eye(10)[3], (100, 1))
    varied = np.eye(10)[np.arange(100) % 10]
    assert class_diversity(collapsed)["clases_cubiertas"] == 1
    assert class_diversity(collapsed)["entropia_clases"] == pytest.approx(0)
    assert class_diversity(varied)["entropia_clases"] == pytest.approx(1)


def test_pairwise_spread_is_zero_when_all_samples_are_equal():
    same = np.ones((20, 28, 28, 1), dtype="float32")
    assert pairwise_spread(same, n=20) == pytest.approx(0, abs=1e-3)


def test_choose_prefers_lower_validation_loss():
    assert choose({"vae_2": 262.9, "vae_16": 242.6})[0] == "vae_16"
