from __future__ import annotations

import io
import shutil
import ssl
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import certifi

from .config import ProjectConfig


UCI_DOWNLOAD_URL = (
    "https://archive.ics.uci.edu/static/public/349/"
    "open+university+learning+analytics+dataset.zip"
)


class OULADRepository:
    def __init__(self, config: ProjectConfig):
        self.config = config

    def ensure_archive(self) -> Path:
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.config.archive_path.exists():
            print("Descargando OULAD desde UCI...")
            context = ssl.create_default_context(cafile=certifi.where())
            request = urllib.request.Request(
                UCI_DOWNLOAD_URL,
                headers={"User-Agent": "UASD-OULAD-Academic-Project/1.0"},
            )
            temporary = self.config.archive_path.with_suffix(".zip.part")
            with urllib.request.urlopen(request, context=context) as response:
                with temporary.open("wb") as destination:
                    shutil.copyfileobj(response, destination)
            temporary.replace(self.config.archive_path)
        return self.config.archive_path

    def _read_csv(self, archive: zipfile.ZipFile, filename: str, **kwargs) -> pd.DataFrame:
        candidates = [name for name in archive.namelist() if name.endswith(filename)]
        if not candidates:
            raise FileNotFoundError(f"{filename} no está dentro del archivo OULAD.")
        with archive.open(candidates[0]) as stream:
            return pd.read_csv(stream, **kwargs)

    def load_oulad(self) -> pd.DataFrame:
        archive_path = self.ensure_archive()
        with zipfile.ZipFile(archive_path) as archive:
            students = self._read_csv(archive, "studentInfo.csv")
            assessments = self._read_csv(archive, "assessments.csv")
            student_assessments = self._read_csv(archive, "studentAssessment.csv")
            clicks = self._aggregate_early_clicks(archive)

        student_assessments["score"] = pd.to_numeric(
            student_assessments["score"], errors="coerce"
        )
        assessment_scores = (
            student_assessments.merge(
                assessments[["id_assessment", "code_module", "code_presentation"]],
                on="id_assessment",
                how="left",
            )
            .groupby(["code_module", "code_presentation", "id_student"], as_index=False)
            .agg(
                promedio_evaluaciones=("score", "mean"),
                evaluaciones_entregadas=("id_assessment", "nunique"),
            )
        )
        keys = ["code_module", "code_presentation", "id_student"]
        frame = students.merge(clicks, on=keys, how="left").merge(
            assessment_scores, on=keys, how="left"
        )
        frame["fuente"] = "OULAD"
        return frame

    def _aggregate_early_clicks(self, archive: zipfile.ZipFile) -> pd.DataFrame:
        candidates = [name for name in archive.namelist() if name.endswith("studentVle.csv")]
        if not candidates:
            raise FileNotFoundError("studentVle.csv no está dentro del archivo OULAD.")

        partials: list[pd.DataFrame] = []
        with archive.open(candidates[0]) as raw:
            buffered = io.TextIOWrapper(raw, encoding="utf-8")
            for chunk in pd.read_csv(buffered, chunksize=500_000):
                early = chunk.loc[
                    chunk["date"].between(0, self.config.early_window_days)
                ]
                if early.empty:
                    continue
                partials.append(
                    early.groupby(
                        ["code_module", "code_presentation", "id_student"],
                        as_index=False,
                    ).agg(
                        clicks_28d=("sum_click", "sum"),
                        dias_activos_28d=("date", "nunique"),
                    )
                )

        columns = [
            "code_module",
            "code_presentation",
            "id_student",
            "clicks_28d",
            "dias_activos_28d",
        ]
        if not partials:
            return pd.DataFrame(columns=columns)

        combined = pd.concat(partials, ignore_index=True)
        return combined.groupby(
            ["code_module", "code_presentation", "id_student"], as_index=False
        ).sum()


class ExperimentXFactory:
    """Genera un complemento anónimo y reproducible, sin atribuirlo a una institución real."""

    EDUCATION = [
        "No Formal quals",
        "Lower Than A Level",
        "A Level or Equivalent",
        "HE Qualification",
        "Post Graduate Qualification",
    ]

    def __init__(self, random_state: int = 8237):
        self.rng = np.random.default_rng(random_state)

    def create(self, n: int = 2500) -> pd.DataFrame:
        rng = self.rng
        clicks = np.maximum(0, rng.negative_binomial(4, 0.035, n))
        active_days = np.clip((clicks / 18 + rng.normal(2, 2, n)).round(), 0, 29)
        credits = rng.choice([30, 60, 90, 120], n, p=[0.15, 0.60, 0.20, 0.05])
        attempts = rng.choice([0, 1, 2, 3], n, p=[0.78, 0.16, 0.05, 0.01])
        education = rng.choice(self.EDUCATION, n, p=[0.05, 0.30, 0.38, 0.23, 0.04])
        age = rng.choice(["0-35", "35-55", "55<="], n, p=[0.66, 0.29, 0.05])
        imd = rng.choice(
            [f"{i}-{i + 10}%" for i in range(0, 90, 10)] + ["90-100%"],
            n,
        )
        gender = rng.choice(["M", "F"], n)
        disability = rng.choice(["N", "Y"], n, p=[0.90, 0.10])

        latent = (
            -1.5
            + 0.010 * clicks
            + 0.07 * active_days
            - 0.45 * attempts
            + 0.003 * credits
            + rng.normal(0, 0.8, n)
        )
        passed = rng.random(n) < (1 / (1 + np.exp(-latent)))
        distinction = passed & (latent > 1.6) & (rng.random(n) < 0.45)
        withdrawal = (~passed) & (active_days < 3) & (rng.random(n) < 0.65)
        result = np.where(
            distinction,
            "Distinction",
            np.where(passed, "Pass", np.where(withdrawal, "Withdrawn", "Fail")),
        )
        score = np.clip(48 + 0.055 * clicks + 0.6 * active_days - 3 * attempts + rng.normal(0, 12, n), 0, 100)

        return pd.DataFrame({
            "code_module": "EXP",
            "code_presentation": "2026X",
            "id_student": np.arange(9_000_000, 9_000_000 + n),
            "gender": gender,
            "region": "Experimento X",
            "highest_education": education,
            "imd_band": imd,
            "age_band": age,
            "num_of_prev_attempts": attempts,
            "studied_credits": credits,
            "disability": disability,
            "final_result": result,
            "clicks_28d": clicks,
            "dias_activos_28d": active_days,
            "promedio_evaluaciones": score,
            "evaluaciones_entregadas": rng.integers(1, 7, n),
            "fuente": "Experimento X sintético",
        })
