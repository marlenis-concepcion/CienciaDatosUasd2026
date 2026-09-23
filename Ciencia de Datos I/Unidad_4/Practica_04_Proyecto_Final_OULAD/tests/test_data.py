import io
import zipfile

import pandas as pd
import pytest

from src.config import ProjectConfig
from src.data import ExperimentXFactory, OULADRepository


def make_zip(path, files):
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)


def test_experiment_x_is_reproducible():
    first = ExperimentXFactory(100).create(25)
    second = ExperimentXFactory(100).create(25)
    pd.testing.assert_frame_equal(first, second)


def test_experiment_x_has_anonymous_unique_ids_and_valid_ranges():
    frame = ExperimentXFactory(8237).create(100)
    assert frame["id_student"].is_unique
    assert frame["id_student"].min() >= 9_000_000
    assert frame["promedio_evaluaciones"].between(0, 100).all()
    assert frame["dias_activos_28d"].between(0, 29).all()
    assert set(frame["fuente"]) == {"Experimento X sintético"}


def test_read_csv_accepts_files_inside_nested_zip_folder(tmp_path):
    archive_path = tmp_path / "sample.zip"
    make_zip(archive_path, {"oulad/studentInfo.csv": "id_student,gender\n1,F\n"})
    repository = OULADRepository(ProjectConfig(root=tmp_path))
    with zipfile.ZipFile(archive_path) as archive:
        frame = repository._read_csv(archive, "studentInfo.csv")
    assert frame.to_dict("records") == [{"id_student": 1, "gender": "F"}]


def test_read_csv_reports_missing_required_file(tmp_path):
    archive_path = tmp_path / "sample.zip"
    make_zip(archive_path, {"other.csv": "value\n1\n"})
    repository = OULADRepository(ProjectConfig(root=tmp_path))
    with zipfile.ZipFile(archive_path) as archive:
        with pytest.raises(FileNotFoundError, match="studentInfo.csv"):
            repository._read_csv(archive, "studentInfo.csv")


def test_early_click_aggregation_respects_configured_window(tmp_path):
    archive_path = tmp_path / "sample.zip"
    csv = io.StringIO()
    pd.DataFrame({
        "code_module": ["AAA", "AAA", "AAA", "AAA"],
        "code_presentation": ["2013J"] * 4,
        "id_student": [1, 1, 1, 2],
        "id_site": [10, 10, 11, 12],
        "date": [0, 10, 29, 5],
        "sum_click": [3, 4, 100, 2],
    }).to_csv(csv, index=False)
    make_zip(archive_path, {"studentVle.csv": csv.getvalue()})
    repository = OULADRepository(
        ProjectConfig(root=tmp_path, early_window_days=28)
    )
    with zipfile.ZipFile(archive_path) as archive:
        result = repository._aggregate_early_clicks(archive)
    student_one = result.loc[result["id_student"] == 1].iloc[0]
    assert student_one["clicks_28d"] == 7
    assert student_one["dias_activos_28d"] == 2


def test_early_click_aggregation_returns_empty_schema_when_window_has_no_rows(tmp_path):
    archive_path = tmp_path / "sample.zip"
    content = (
        "code_module,code_presentation,id_student,id_site,date,sum_click\n"
        "AAA,2013J,1,10,99,3\n"
    )
    make_zip(archive_path, {"studentVle.csv": content})
    repository = OULADRepository(
        ProjectConfig(root=tmp_path, early_window_days=28)
    )
    with zipfile.ZipFile(archive_path) as archive:
        result = repository._aggregate_early_clicks(archive)
    assert result.empty
    assert result.columns.tolist() == [
        "code_module",
        "code_presentation",
        "id_student",
        "clicks_28d",
        "dias_activos_28d",
    ]
