from __future__ import annotations

import numpy as np
import pandas as pd


EDUCATION_ORDER = {
    "No Formal quals": 0,
    "Lower Than A Level": 1,
    "A Level or Equivalent": 2,
    "HE Qualification": 3,
    "Post Graduate Qualification": 4,
}
AGE_ORDER = {"0-35": 0, "35-55": 1, "55<=": 2}
RESULT_ORDER = {"Withdrawn": 0, "Fail": 1, "Pass": 2, "Distinction": 3}


def imd_midpoint(value) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).replace("%", "")
    try:
        low, high = text.split("-")
        return (float(low) + float(high)) / 2
    except ValueError:
        return np.nan


class FeatureEngineer:
    feature_columns = [
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
    ]

    numeric_columns = [
        "clicks_28d",
        "dias_activos_28d",
        "studied_credits",
        "num_of_prev_attempts",
        "educacion_ordinal",
        "edad_ordinal",
        "imd_midpoint",
    ]
    categorical_columns = ["gender", "disability", "code_module"]

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        data = frame.copy()
        data["clicks_28d"] = data["clicks_28d"].fillna(0)
        data["dias_activos_28d"] = data["dias_activos_28d"].fillna(0)
        data["educacion_ordinal"] = data["highest_education"].map(EDUCATION_ORDER)
        data["edad_ordinal"] = data["age_band"].map(AGE_ORDER)
        data["imd_midpoint"] = data["imd_band"].map(imd_midpoint)
        data["aprobo"] = data["final_result"].isin(["Pass", "Distinction"]).astype(int)
        data["resultado_ordinal"] = data["final_result"].map(RESULT_ORDER)
        return data.dropna(subset=["resultado_ordinal"]).reset_index(drop=True)
