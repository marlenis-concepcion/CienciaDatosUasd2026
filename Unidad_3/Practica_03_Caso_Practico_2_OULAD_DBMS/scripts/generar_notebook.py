import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "Proyecto_Final_OULAD_Colab.ipynb"


def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


cells = [
    md(
        """
        # Proyecto final colaborativo: Machine Learning sobre OULAD

        **UASD | INF-8237-C2 | Mccarthy Team**

        Este cuaderno ejecuta el proyecto POO/OSEMN incluido en el folder
        `Practica_04_Proyecto_Final_OULAD`. Utiliza OULAD y un Experimento X sintético claramente
        identificado. No contiene rutas de una computadora personal.
        """
    ),
    md(
        """
        ## 1. Preparar el proyecto

        En Colab, comprima el folder como `Practica_04_Proyecto_Final_OULAD.zip`, ejecute esta
        celda y seleccione el ZIP. Localmente, el cuaderno encuentra automáticamente el folder
        padre.
        """
    ),
    code(
        """
        import os
        import sys
        import zipfile
        from pathlib import Path

        def find_project():
            candidates = [
                Path.cwd(),
                Path.cwd().parent,
                Path.cwd() / "Practica_04_Proyecto_Final_OULAD",
            ]
            for candidate in candidates:
                if (candidate / "src" / "pipeline.py").exists():
                    return candidate.resolve()
            return None

        PROJECT_ROOT = find_project()
        if PROJECT_ROOT is None:
            try:
                from google.colab import files
                uploaded = files.upload()
                zip_name = next(name for name in uploaded if name.lower().endswith(".zip"))
                with zipfile.ZipFile(zip_name) as archive:
                    archive.extractall(".")
                PROJECT_ROOT = find_project()
            except ImportError as exc:
                raise RuntimeError("Ejecute desde el folder del proyecto.") from exc

        if PROJECT_ROOT is None:
            raise RuntimeError("No se encontró src/pipeline.py en el ZIP.")

        os.chdir(PROJECT_ROOT)
        sys.path.insert(0, str(PROJECT_ROOT))
        print("Proyecto:", PROJECT_ROOT.name)
        """
    ),
    md("## 2. Instalar dependencias"),
    code(
        """
        import subprocess
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            check=True,
        )
        """
    ),
    md(
        """
        ## 3. Ejecutar OSEMN

        La primera ejecución descarga OULAD desde UCI. El procesamiento de `studentVle.csv`
        se realiza por bloques para controlar el uso de memoria.
        """
    ),
    code(
        """
        from src.config import ProjectConfig
        from src.pipeline import OULADProject

        config = ProjectConfig(root=PROJECT_ROOT)
        metricas = OULADProject(config).run()
        display(metricas.round(4))
        """
    ),
    md("## 4. Revisar las salidas"),
    code(
        """
        import pandas as pd
        from IPython.display import display, Image

        display(pd.read_csv("outputs/metricas_generales.csv").round(4))
        display(pd.read_csv("outputs/f1_manual.csv").round(4))
        display(
            pd.read_csv("outputs/importancias_variables.csv")
            .sort_values("importancia", ascending=False)
            .head(20)
        )
        print(Path("outputs/hallazgos.txt").read_text(encoding="utf-8"))
        display(Image("outputs/eda_alto_nivel.png"))
        """
    ),
    md(
        """
        ## 5. Evidencia caso a caso

        Los archivos siguientes contienen `y_test`, `y_pred`, modelo, identificador anónimo,
        fuente y resultado original.
        """
    ),
    code(
        """
        for filename in [
            "predicciones_binarias.csv",
            "predicciones_ordinales.csv",
            "predicciones_regresion.csv",
        ]:
            frame = pd.read_csv(Path("outputs") / filename)
            print(filename, frame.shape)
            display(frame.head())
        """
    ),
    md(
        """
        ## 6. Descargar evidencias

        La celda crea un ZIP portable con métricas, predicciones, gráficos y hallazgos.
        """
    ),
    code(
        """
        import shutil
        shutil.make_archive("evidencias_proyecto_oulad", "zip", "outputs")
        try:
            from google.colab import files
            files.download("evidencias_proyecto_oulad.zip")
        except ImportError:
            print("Archivo creado:", Path("evidencias_proyecto_oulad.zip").resolve())
        """
    ),
    md(
        """
        ## Declaración de colaboración y uso responsable

        El equipo debe completar nombres, matrículas y responsabilidades en el README. Las
        predicciones se presentan con fines académicos. No deben usarse para sancionar,
        excluir ni tomar decisiones automáticas sobre estudiantes.
        """
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"name": OUTPUT.name, "provenance": []},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(OUTPUT.relative_to(ROOT))
