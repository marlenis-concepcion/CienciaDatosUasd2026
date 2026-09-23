import pandas as pd
import pytest

from inf8239_u02.config import ROOT
from inf8239_u02.data import check_no_leakage, deduplicate, normalize_text, split_data
from inf8239_u02.experiment import choose
from inf8239_u02.modeling import build_models


def corpus(n=40):
    texts = [f"mensaje {chr(97 + i % 26)}{chr(97 + i // 26)} de prueba" for i in range(n)]
    return pd.DataFrame({"id": range(n), "text": texts, "label": ["spam" if i % 4 == 0 else "ham" for i in range(n)]})


def test_deduplicate_removes_normalized_copies_before_split():
    df = pd.DataFrame({"id": [0, 1, 2, 3], "text": ["Call 0800 NOW", "call  0999 now", "hola", "Hola"],
                       "label": ["spam", "spam", "ham", "ham"]})
    clean, summary = deduplicate(df, "text", "label")
    assert list(clean["id"]) == [0, 2]
    assert summary["duplicados_exactos"] == 0
    assert summary["duplicados_normalizados"] == 2


def test_deduplicate_rejects_contradictory_labels():
    df = pd.DataFrame({"id": [0, 1], "text": ["Ok", "ok"], "label": ["ham", "spam"]})
    with pytest.raises(ValueError, match="contradictorias"):
        deduplicate(df, "text", "label")


def test_splits_are_disjoint_complete_and_stratified():
    df = corpus(200)
    splits = split_data(df, "label", random_state=42)
    ids = [set(p["id"]) for p in splits.values()]
    assert set.union(*ids) == set(df["id"])
    assert sum(len(i) for i in ids) == len(df)
    for part in splits.values():
        assert abs((part["label"] == "spam").mean() - 0.25) < 0.03
    check_no_leakage(splits, "text")


def test_leakage_check_detects_normalized_duplicate_across_splits():
    splits = {"train": pd.DataFrame({"text": ["WIN 100 now"]}), "test": pd.DataFrame({"text": ["win 555 NOW"]})}
    assert normalize_text("WIN 100 now") == normalize_text("win 555 NOW")
    with pytest.raises(ValueError, match="compartidos"):
        check_no_leakage(splits, "text")


def test_vectorizer_learns_vocabulary_only_from_training_texts():
    model = build_models()["naive_bayes"]
    model.fit(["premio gratis ahora", "nos vemos luego"], ["spam", "ham"])
    model.predict(["palabraexclusivadetest"])
    assert "palabraexclusivadetest" not in model.named_steps["tfidf"].vocabulary_


def test_choose_ignores_baseline_and_breaks_ties_by_spam_recall():
    table = pd.DataFrame({"modelo": ["dummy", "naive_bayes", "logistic"], "f1_macro": [0.99, 0.95, 0.95],
                          "recall_spam": [0.0, 0.90, 0.93]})
    assert choose(table) == "logistic"


def test_every_analyzed_error_has_category_and_explanation():
    categories = pd.read_csv(ROOT / "docs/error_categories.csv")
    assert len(categories) >= 20
    assert categories["id"].is_unique
    assert categories[["categoria", "explicacion"]].notna().all().all()
