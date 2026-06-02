import pandas as pd
import pytest

from src.extract import to_snake_case
from src.quality import find_duplicate_keys, validate_domains
from src.transform import clean_tables


def test_to_snake_case_converts_camel_case():
    assert to_snake_case("studentInfo") == "student_info"
    assert to_snake_case("dateRegistration") == "date_registration"


def test_clean_tables_converts_question_marks_to_null():
    tables = {
        "student_info": pd.DataFrame(
            {
                "code_module": [" AAA "],
                "code_presentation": ["2013J"],
                "gender": ["M"],
                "region": ["?"],
                "highest_education": ["HE Qualification"],
                "imd_band": ["?"],
                "age_band": ["35-55"],
                "disability": ["N"],
                "final_result": ["Pass"],
            }
        )
    }

    cleaned = clean_tables(tables)["student_info"]

    assert cleaned.loc[0, "code_module"] == "AAA"
    assert pd.isna(cleaned.loc[0, "region"])
    assert pd.isna(cleaned.loc[0, "imd_band"])


def test_find_duplicate_keys_detects_student_info_duplicates():
    tables = {
        "courses": pd.DataFrame(),
        "assessments": pd.DataFrame(),
        "student_registration": pd.DataFrame(),
        "vle": pd.DataFrame(),
        "student_assessment": pd.DataFrame(),
        "student_vle": pd.DataFrame(),
        "student_info": pd.DataFrame(
            {
                "id_student": [1, 1],
                "code_module": ["AAA", "AAA"],
                "code_presentation": ["2013J", "2013J"],
            }
        ),
    }

    duplicates = find_duplicate_keys(tables)

    assert "student_info" in duplicates
    assert len(duplicates["student_info"]) == 2


def test_validate_domains_detects_invalid_score_and_clicks():
    tables = {
        "student_info": pd.DataFrame({"final_result": ["Pass", "Unknown"]}),
        "student_assessment": pd.DataFrame({"score": [95, 130]}),
        "student_vle": pd.DataFrame({"sum_click": [3, -1]}),
    }

    issues = validate_domains(tables)

    assert "student_info.final_result" in issues
    assert "student_assessment.score" in issues
    assert "student_vle.sum_click" in issues

