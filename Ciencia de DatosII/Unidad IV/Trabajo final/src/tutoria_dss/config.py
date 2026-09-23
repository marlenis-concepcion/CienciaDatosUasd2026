from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA_URL = "https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip"
DATA_SHA256 = "e90e55fd65ec462ae283ebeb2cca409319e3460ed898d8754f62fb35cc83a65d"
DATA_PATH = ROOT / "data/raw/data.csv"


def load_config(path: Path = ROOT / "configs/dss.yml") -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))
