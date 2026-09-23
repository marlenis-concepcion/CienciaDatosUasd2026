import numpy as np
import pandas as pd
import pytest

from inf8239_u03.data import select_cold_users, temporal_split_per_user
from inf8239_u03.experiment import choose
from inf8239_u03.metrics import novelty, ranking_metrics
from inf8239_u03.recommenders import MatrixFactorization, Scorer, pareto_front


def history(n_users=10, n_items=12):
    rows = [(u, i, float(1 + (u + i) % 5), 1000 * u + i) for u in range(1, n_users + 1) for i in range(1, n_items + 1)]
    return pd.DataFrame(rows, columns=["userId", "movieId", "rating", "timestamp"])


def test_temporal_split_keeps_past_in_train_and_future_in_test():
    train, valid, test = temporal_split_per_user(history())
    for user in train["userId"].unique():
        assert train[train.userId == user].timestamp.max() < valid[valid.userId == user].timestamp.min()
        assert valid[valid.userId == user].timestamp.max() < test[test.userId == user].timestamp.min()
    assert len(train) + len(valid) + len(test) == 120
    assert not set(zip(train.userId, train.movieId)) & set(zip(test.userId, test.movieId))


def test_cold_users_are_reproducible_and_disjoint_from_training():
    ratings = history(n_users=50)
    cold = select_cold_users(ratings, fraction=0.1, seed=42)
    assert cold == select_cold_users(ratings, fraction=0.1, seed=42)
    assert len(cold) == 5
    train, _, _ = temporal_split_per_user(ratings[~ratings.userId.isin(cold)])
    assert not cold & set(train.userId)


def test_ranking_metrics_match_hand_calculation():
    recs = {1: [10, 20, 30], 2: [40, 50, 60]}
    truth = {1: {20, 99}, 2: {70}}
    table = ranking_metrics(recs, truth, k=3).set_index("userId")
    assert table.loc[1, "precision"] == pytest.approx(1 / 3)
    assert table.loc[1, "recall"] == pytest.approx(0.5)
    assert table.loc[1, "ndcg"] == pytest.approx((1 / np.log2(3)) / (1 + 1 / np.log2(3)))
    assert table.loc[2, "hit"] == 0


def test_novelty_is_higher_for_less_popular_items():
    popularity = pd.Series({1: 90, 2: 1})
    assert novelty({7: [2]}, popularity, 100) > novelty({7: [1]}, popularity, 100)


def test_recommendations_exclude_seen_items_and_cold_user_gets_popularity(sample_ratings, sample_movies):
    mf = MatrixFactorization(factors=2, seed=42).fit(sample_ratings, epochs=2)
    scorer = Scorer(sample_ratings, sample_movies, mf)
    for method in ["popularity", "content", "mf", "hybrid"]:
        recs = scorer.recommend(1, method, 0.5, k=5)
        assert not {1, 2, 3} & set(recs)
    assert scorer.recommend(999, "hybrid", 0.5, k=2) == scorer.recommend(999, "popularity", k=2)


def test_pareto_front_and_decision_rule():
    table = pd.DataFrame({"modelo": ["a", "b", "c", "d"], "ndcg@10": [0.050, 0.049, 0.030, 0.020],
                          "cobertura": [0.05, 0.10, 0.08, 0.20]})
    table["pareto"] = pareto_front(table, ["ndcg@10", "cobertura"])
    assert table["pareto"].tolist() == [True, True, False, True]
    assert choose(table)[0] == "b"
