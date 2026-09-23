from __future__ import annotations

from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline


def build_models(random_state: int = 42) -> dict[str, Pipeline]:
    vectorizer = lambda: TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    return {
        "dummy": Pipeline([("tfidf", vectorizer()), ("model", DummyClassifier(strategy="most_frequent"))]),
        "naive_bayes": Pipeline([("tfidf", vectorizer()), ("model", ComplementNB())]),
        "logistic": Pipeline([
            ("tfidf", vectorizer()),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=random_state)),
        ]),
    }


# Misma rejilla de representación para ambos pipelines; solo cambia el clasificador.
TFIDF_GRID = {
    "tfidf__ngram_range": [(1, 1), (1, 2)],
    "tfidf__min_df": [1, 2],
}

PARAM_GRIDS = {
    "naive_bayes": {**TFIDF_GRID, "model__alpha": [0.1, 0.3, 1.0]},
    "logistic": {**TFIDF_GRID, "model__C": [1.0, 10.0, 100.0]},
}
