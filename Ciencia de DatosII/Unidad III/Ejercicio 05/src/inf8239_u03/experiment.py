from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error

from .config import MOVIELENS_DIR, RANDOM_STATE, ROOT
from .data import load_movielens, select_cold_users, temporal_split_per_user
from .metrics import catalog_coverage, novelty, ranking_metrics
from .recommenders import MatrixFactorization, Scorer, pareto_front

K = 10
RELEVANT = 4.0
MF_GRID = [(10, 12), (20, 12), (40, 12), (20, 30)]
ALPHAS = [0.25, 0.5, 0.75]
ONBOARDING = 5
NDCG_TOLERANCE = 0.95


def relevant_items(part: pd.DataFrame) -> dict[int, set[int]]:
    liked = part[part["rating"] >= RELEVANT]
    return {int(u): set(g["movieId"].astype(int)) for u, g in liked.groupby("userId")}


def configurations() -> list[dict]:
    configs = [{"modelo": "popularidad", "method": "popularity"}, {"modelo": "contenido", "method": "content"},
               {"modelo": "factorizacion", "method": "mf"}]
    configs += [{"modelo": f"hibrido_a{alpha}", "method": "hybrid", "alpha": alpha} for alpha in ALPHAS]
    return configs


def evaluate(scorer: Scorer, truth: dict[int, set[int]], config: dict, popularity_counts: pd.Series,
             n_users: int, histories: dict | None = None) -> tuple[dict, pd.DataFrame, dict]:
    recs = {}
    for user in truth:
        history = None if histories is None else histories.get(user, pd.DataFrame(columns=["movieId", "rating"]))
        recs[user] = scorer.recommend(user, config["method"], config.get("alpha", 0.5), K, history)
    per_user = ranking_metrics(recs, truth, K)
    summary = {"modelo": config["modelo"], "usuarios": len(per_user),
               **{f"{m}@{K}": float(per_user[m].mean()) for m in ["precision", "recall", "ndcg", "hit"]},
               "cobertura": catalog_coverage(recs, len(scorer.catalog)),
               "novedad": novelty(recs, popularity_counts, n_users)}
    return summary, per_user, recs


def audit(ratings: pd.DataFrame, movies: pd.DataFrame, reports: Path) -> dict:
    per_user = ratings.groupby("userId").size()
    per_item = ratings.groupby("movieId").size()
    top_share = per_item.sort_values(ascending=False).head(int(len(per_item) * 0.1)).sum() / len(ratings)
    summary = {
        "valoraciones": int(len(ratings)), "usuarios": int(ratings["userId"].nunique()),
        "peliculas_catalogo": int(len(movies)), "peliculas_valoradas": int(ratings["movieId"].nunique()),
        "densidad": round(len(ratings) / (ratings["userId"].nunique() * ratings["movieId"].nunique()), 5),
        "desde": str(pd.to_datetime(ratings["timestamp"].min(), unit="s").date()),
        "hasta": str(pd.to_datetime(ratings["timestamp"].max(), unit="s").date()),
        "duplicados_usuario_pelicula": int(ratings.duplicated(["userId", "movieId"]).sum()),
        "nulos": int(ratings.isna().sum().sum() + movies.isna().sum().sum()),
        "valoraciones_por_usuario": {"min": int(per_user.min()), "mediana": float(per_user.median()), "max": int(per_user.max())},
        "peliculas_con_una_valoracion": int((per_item == 1).sum()),
        "porcentaje_valoraciones_en_top10pct_peliculas": round(float(top_share) * 100, 1),
        "peliculas_sin_genero": int(movies["genres"].eq("(no genres listed)").sum()),
        "distribucion_rating": {str(k): int(v) for k, v in ratings["rating"].value_counts().sort_index().items()},
    }
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    counts = ratings["rating"].value_counts().sort_index()
    axes[0].bar(counts.index.astype(str), counts.values, color="#4c78a8")
    axes[0].set_title("Distribución de ratings")
    axes[0].tick_params(axis="x", labelsize=7)
    axes[1].hist(per_user, bins=50, color="#4c78a8", log=True)
    axes[1].set_title("Valoraciones por usuario (log)")
    ranked = per_item.sort_values(ascending=False).to_numpy()
    axes[2].plot(np.arange(1, len(ranked) + 1), ranked, color="#e45756")
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_title("Cola larga: valoraciones por película")
    axes[2].set_xlabel("posición de la película")
    figure.tight_layout()
    figure.savefig(reports / "auditoria.png", dpi=160)
    plt.close(figure)
    return summary


def choose(valid_table: pd.DataFrame) -> tuple[str, str]:
    """Entre los puntos de la frontera de Pareto (NDCG y cobertura), el de mayor cobertura con NDCG >= 95 % del máximo."""
    front = valid_table[valid_table["pareto"]]
    best = front[f"ndcg@{K}"].max()
    eligible = front[front[f"ndcg@{K}"] >= NDCG_TOLERANCE * best]
    chosen = eligible.sort_values(["cobertura", f"ndcg@{K}"], ascending=False).iloc[0]["modelo"]
    return str(chosen), (f"Frontera de Pareto: {', '.join(front['modelo'])}. NDCG@{K} máximo {best:.4f}; "
                         f"con al menos {NDCG_TOLERANCE:.0%} de ese valor: {', '.join(eligible['modelo'])}. "
                         f"Se elige el de mayor cobertura: {chosen}.")


def run(reports: Path = ROOT / "reports") -> dict:
    reports.mkdir(exist_ok=True)
    ratings, movies = load_movielens(MOVIELENS_DIR)
    summary = audit(ratings, movies, reports)
    cold = select_cold_users(ratings, seed=RANDOM_STATE)
    warm = ratings[~ratings["userId"].isin(cold)]
    train, valid, test = temporal_split_per_user(warm)
    assert (train.groupby("userId")["timestamp"].max() <= test.groupby("userId")["timestamp"].min()).all()
    partition = {"usuarios_frios": len(cold), "usuarios_calidos": int(warm["userId"].nunique()),
                 "train": len(train), "valid": len(valid), "test": len(test),
                 "regla": "por usuario: 70 % más antiguo entrenamiento, 10 % siguiente validación, 20 % más reciente prueba"}
    pd.DataFrame({"userId": sorted(cold)}).to_csv(reports / "usuarios_frios.csv", index=False)

    # 1) Validación: hiperparámetros de la factorización y elección del híbrido.
    valid_truth = relevant_items(valid)
    grid_rows, best_mf = [], None
    for factors, epochs in MF_GRID:
        start = perf_counter()
        mf = MatrixFactorization(factors=factors, seed=RANDOM_STATE).fit(train, epochs=epochs)
        seconds = perf_counter() - start
        scorer = Scorer(train, movies, mf)
        counts = train.groupby("movieId").size()
        result, _, _ = evaluate(scorer, valid_truth, {"modelo": "factorizacion", "method": "mf"}, counts,
                                train["userId"].nunique())
        known = valid[valid["movieId"].isin(mf.item_index)]
        rmse = root_mean_squared_error(known["rating"], [mf.predict(r.userId, r.movieId) for r in known.itertuples()])
        grid_rows.append({"factores": factors, "epocas": epochs, f"ndcg@{K}": result[f"ndcg@{K}"], "rmse_valid": rmse,
                          "segundos": seconds})
        if best_mf is None or result[f"ndcg@{K}"] > best_mf[2]:
            best_mf = (factors, epochs, result[f"ndcg@{K}"], mf)
    pd.DataFrame(grid_rows).to_csv(reports / "busqueda_factorizacion.csv", index=False)
    factors, epochs, _, mf = best_mf
    scorer = Scorer(train, movies, mf)
    counts = train.groupby("movieId").size()
    rows = []
    for config in configurations():
        result, _, _ = evaluate(scorer, valid_truth, config, counts, train["userId"].nunique())
        rows.append(result)
    valid_table = pd.DataFrame(rows)
    valid_table["pareto"] = pareto_front(valid_table, [f"ndcg@{K}", "cobertura"])
    valid_table.to_csv(reports / "validacion.csv", index=False)
    chosen, reason = choose(valid_table)
    decision = {"modelo_elegido": chosen, "factorizacion": {"factores": factors, "epocas": epochs}, "razon": reason,
                "regla": f"Pareto en validación (NDCG@{K} y cobertura); mayor cobertura con NDCG >= {NDCG_TOLERANCE:.0%} del máximo",
                "tomada_antes_de_test": True}
    (reports / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2) Prueba: se reentrena con entrenamiento + validación y se evalúa una vez.
    history = pd.concat([train, valid], ignore_index=True)
    start = perf_counter()
    final_mf = MatrixFactorization(factors=factors, seed=RANDOM_STATE).fit(history, epochs=epochs)
    mf_seconds = perf_counter() - start
    final = Scorer(history, movies, final_mf)
    final_counts = history.groupby("movieId").size()
    test_truth = relevant_items(test)
    rows, per_user_chosen, recs_chosen = [], None, None
    for config in configurations():
        start = perf_counter()
        result, per_user, recs = evaluate(final, test_truth, config, final_counts, history["userId"].nunique())
        result["segundos_recomendar"] = perf_counter() - start
        rows.append(result)
        if config["modelo"] == chosen:
            per_user_chosen, recs_chosen = per_user, recs
    test_table = pd.DataFrame(rows)
    known = test[test["movieId"].isin(final_mf.item_index)]
    rmse = root_mean_squared_error(known["rating"], [final_mf.predict(r.userId, r.movieId) for r in known.itertuples()])
    reachable = sum(len(v & set(final.catalog)) for v in test_truth.values()) / sum(len(v) for v in test_truth.values())
    test_table.to_csv(reports / "resultados_test.csv", index=False)

    # 3) Usuarios fríos: sin historia (popularidad) y con 5 valoraciones iniciales (contenido).
    cold_ratings = ratings[ratings["userId"].isin(cold)].sort_values(["userId", "timestamp", "movieId"])
    onboarding = cold_ratings.groupby("userId").head(ONBOARDING)
    cold_truth = relevant_items(cold_ratings.drop(onboarding.index))
    onboard_hist = {int(u): g for u, g in onboarding.groupby("userId")}
    empty = {u: pd.DataFrame(columns=["movieId", "rating"]) for u in cold_truth}
    cold_rows = []
    for name, config, hist in [("popularidad (0 valoraciones)", {"modelo": "p", "method": "popularity"}, empty),
                               (f"contenido ({ONBOARDING} valoraciones)", {"modelo": "c", "method": "content"}, onboard_hist),
                               (f"popularidad sin repetir ({ONBOARDING} valoraciones)", {"modelo": "p", "method": "popularity"}, onboard_hist)]:
        result, _, _ = evaluate(final, cold_truth, config, final_counts, history["userId"].nunique(), hist)
        result["modelo"] = name
        cold_rows.append(result)
    cold_table = pd.DataFrame(cold_rows)
    cold_table.to_csv(reports / "usuarios_frios_resultados.csv", index=False)

    # 4) Errores: desempeño del modelo elegido según la actividad del usuario y ejemplos sin aciertos.
    activity = history.groupby("userId").size().rename("historial")
    detail = per_user_chosen.join(activity, on="userId")
    detail["actividad"] = pd.qcut(detail["historial"], 4, labels=["Q1 (menos activos)", "Q2", "Q3", "Q4 (más activos)"])
    by_activity = detail.groupby("actividad", observed=True).agg(
        usuarios=("userId", "size"), historial_mediano=("historial", "median"), ndcg=("ndcg", "mean"),
        hit=("hit", "mean"), sin_aciertos=("hit", lambda s: int((s == 0).sum()))).reset_index()
    by_activity.to_csv(reports / "errores_por_actividad.csv", index=False)
    genres = movies.set_index("movieId")["genres"]
    top_genres = lambda items: pd.Series("|".join(genres.loc[list(items)]).split("|")).value_counts().head(3).index.tolist()
    examples = []
    for user in detail.sort_values(["hit", "historial"]).query("hit == 0")["userId"].head(5):
        liked = history[(history["userId"] == user) & (history["rating"] >= RELEVANT)]["movieId"]
        examples.append({"userId": int(user), "historial": int(activity[user]),
                         "generos_que_le_gustan": ", ".join(top_genres(liked)) if len(liked) else "—",
                         "generos_recomendados": ", ".join(top_genres(recs_chosen[user])),
                         "generos_relevantes_en_test": ", ".join(top_genres(test_truth[user])),
                         "relevantes_en_test": len(test_truth[user])})
    pd.DataFrame(examples).to_csv(reports / "ejemplos_sin_aciertos.csv", index=False)

    # Figura de Pareto (validación).
    figure, axis = plt.subplots(figsize=(6.5, 4.2))
    for row in valid_table.itertuples():
        color = "#e45756" if row.modelo == chosen else ("#4c78a8" if row.pareto else "#bbbbbb")
        axis.scatter(row.cobertura, valid_table.loc[row.Index, f"ndcg@{K}"], s=60, color=color)
        axis.annotate(row.modelo, (row.cobertura, valid_table.loc[row.Index, f"ndcg@{K}"]), fontsize=8,
                      xytext=(5, 4), textcoords="offset points")
    axis.set_xlabel("Cobertura del catálogo")
    axis.set_ylabel(f"NDCG@{K} (validación)")
    axis.set_title("Frontera de Pareto · azul: no dominados · rojo: elegido")
    figure.tight_layout()
    figure.savefig(reports / "pareto.png", dpi=160)
    plt.close(figure)

    extra = {"rmse_test_factorizacion": rmse, "segundos_entrenar_factorizacion": mf_seconds,
             "fraccion_relevantes_alcanzables": reachable, "k": K, "umbral_relevancia": RELEVANT}
    (reports / "resumen.json").write_text(json.dumps({"auditoria": summary, "particion": partition, **extra},
                                                     indent=2, ensure_ascii=False), encoding="utf-8")
    return {"audit": summary, "partition": partition, "grid": pd.DataFrame(grid_rows), "valid": valid_table,
            "decision": decision, "test": test_table, "cold": cold_table, "by_activity": by_activity,
            "examples": pd.DataFrame(examples), "extra": extra}
