from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def python_for(project: Path) -> str:
    local_python = project / ".venv" / "bin" / "python"
    return str(local_python) if local_python.exists() else sys.executable


def run_tests(label: str, project: Path) -> None:
    env = os.environ.copy()
    env.update({
        "MPLCONFIGDIR": str(project / ".matplotlib-cache"),
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    })
    print(f"\n== {label} ==")
    subprocess.run(
        [python_for(project), "-m", "pytest", "-q"],
        cwd=project,
        env=env,
        check=True,
    )


def main() -> None:
    run_tests(
        "Unidad 2 - Práctica 02 Sakila",
        ROOT / "Unidad_2" / "Practica_02_Sakila_CRUD_ORM",
    )
    run_tests(
        "Unidad 4 - Práctica 04 OULAD",
        ROOT / "Unidad_4" / "Practica_04_Proyecto_Final_OULAD",
    )
    print("\nRepositorio validado correctamente.")


if __name__ == "__main__":
    main()
