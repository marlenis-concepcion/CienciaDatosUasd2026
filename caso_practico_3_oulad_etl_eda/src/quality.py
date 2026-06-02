EXPECTED_PRIMARY_KEYS = {
    "courses": ["code_module", "code_presentation"],
    "assessments": ["id_assessment"],
    "student_info": ["id_student", "code_module", "code_presentation"],
    "student_registration": ["id_student", "code_module", "code_presentation"],
    "vle": ["id_site"],
    "student_assessment": ["id_assessment", "id_student"],
    "student_vle": ["code_module", "code_presentation", "id_student", "id_site", "date"],
}


def profile_tables(tables):
    rows = []
    for name, df in tables.items():
        rows.append(
            {
                "table": name,
                "rows": len(df),
                "columns": len(df.columns),
                "null_cells": int(df.isna().sum().sum()),
            }
        )
    return rows


def find_duplicate_keys(tables):
    duplicates = {}
    for name, keys in EXPECTED_PRIMARY_KEYS.items():
        df = tables[name]
        duplicated = df[df.duplicated(keys, keep=False)]
        if not duplicated.empty:
            duplicates[name] = duplicated
    return duplicates


def validate_domains(tables):
    issues = {}
    student_info = tables["student_info"]
    invalid_results = student_info[
        ~student_info["final_result"].isin(["Pass", "Fail", "Withdrawn", "Distinction"])
    ]
    if not invalid_results.empty:
        issues["student_info.final_result"] = invalid_results

    student_assessment = tables["student_assessment"]
    invalid_scores = student_assessment[
        student_assessment["score"].notna()
        & ((student_assessment["score"] < 0) | (student_assessment["score"] > 100))
    ]
    if not invalid_scores.empty:
        issues["student_assessment.score"] = invalid_scores

    student_vle = tables["student_vle"]
    invalid_clicks = student_vle[student_vle["sum_click"] < 0]
    if not invalid_clicks.empty:
        issues["student_vle.sum_click"] = invalid_clicks

    return issues

