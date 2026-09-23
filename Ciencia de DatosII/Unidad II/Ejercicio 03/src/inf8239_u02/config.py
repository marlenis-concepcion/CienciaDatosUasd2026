from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

SMS_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
SMS_SHA256 = "1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3"


@dataclass(frozen=True)
class Settings:
    data_source: str = os.getenv("DATA_SOURCE", "url")
    dataset_path: Path = ROOT / os.getenv("DATASET_PATH", "data/raw/sms_spam.csv")
    dataset_url: str = os.getenv("DATASET_URL", SMS_URL)
    dataset_sha256: str = os.getenv("DATASET_SHA256", SMS_SHA256)
    text_column: str = os.getenv("TEXT_COLUMN", "text")
    target_column: str = os.getenv("TARGET_COLUMN", "label")
    random_state: int = int(os.getenv("RANDOM_STATE", "42"))


settings = Settings()
