import pandas as pd


TEXT_COLUMNS = {
    "courses": ["code_module", "code_presentation"],
    "assessments": ["code_module", "code_presentation", "assessment_type"],
    "student_info": [
        "code_module",
        "code_presentation",
        "gender",
        "region",
        "highest_education",
        "imd_band",
        "age_band",
        "disability",
        "final_result",
    ],
    "student_registration": ["code_module", "code_presentation"],
    "student_assessment": [],
    "student_vle": ["code_module", "code_presentation"],
    "vle": ["code_module", "code_presentation", "activity_type"],
}


def clean_tables(tables):
    cleaned = {}
    for name, df in tables.items():
        current = df.copy()
        current = current.replace({"?": pd.NA, "": pd.NA})

        for column in TEXT_COLUMNS.get(name, []):
            if column in current.columns:
                current[column] = current[column].astype("string").str.strip()

        cleaned[name] = current
    return cleaned


def add_student_features(tables):
    student_info = tables["student_info"].copy()
    registration = tables["student_registration"].copy()
    assessment = tables["student_assessment"].copy()
    student_vle = tables["student_vle"].copy()

    clicks = (
        student_vle.groupby(["id_student", "code_module", "code_presentation"], as_index=False)["sum_click"]
        .sum()
        .rename(columns={"sum_click": "total_clicks_student_course"})
    )
    scores = (
        assessment.groupby("id_student", as_index=False)["score"]
        .mean()
        .rename(columns={"score": "avg_score_student"})
    )

    features = student_info.merge(clicks, how="left", on=["id_student", "code_module", "code_presentation"])
    features = features.merge(scores, how="left", on="id_student")
    features = features.merge(
        registration,
        how="left",
        on=["id_student", "code_module", "code_presentation"],
    )
    features["completed_course"] = features["final_result"].isin(["Pass", "Distinction"])
    features["passed_course"] = features["final_result"].isin(["Pass", "Distinction"])
    features["days_until_unregistration"] = features["date_unregistration"]
    features["total_clicks_student_course"] = features["total_clicks_student_course"].fillna(0)
    return features

