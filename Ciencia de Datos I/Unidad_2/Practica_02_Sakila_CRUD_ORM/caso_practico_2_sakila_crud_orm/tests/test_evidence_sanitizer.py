import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "ejecutar_con_evidencia.py"
SPEC = importlib.util.spec_from_file_location("ejecutar_con_evidencia", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_sanitize_hides_personal_paths():
    text = (
        "/Users/example/Documents/proyecto/main.py\n"
        "/home/example/proyecto/main.py\n"
        r"C:\Users\example\proyecto\main.py"
    )

    sanitized = MODULE.sanitize(text)

    assert "/Users/example" not in sanitized
    assert "/home/example" not in sanitized
    assert r"C:\Users\example" not in sanitized
    assert sanitized.count("<HOME>") == 3


def test_sanitize_hides_project_root():
    text = f"{MODULE.ROOT}/caso_practico_2_sakila_crud_orm/src/main.py"

    assert MODULE.sanitize(text) == (
        "<PROJECT_ROOT>/caso_practico_2_sakila_crud_orm/src/main.py"
    )


def test_sanitize_hides_python_installation_paths():
    text = (
        "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/"
        "site-packages/mysql/connector/cursor_cext.py"
    )

    assert MODULE.sanitize(text) == "<PYTHON_INSTALL>"
