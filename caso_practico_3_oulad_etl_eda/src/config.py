from dataclasses import dataclass
import os
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"
AUDIT_DATA_DIR = PROJECT_DIR / "data" / "audit"


@dataclass(frozen=True)
class PostgresConfig:
    host: str = os.getenv("OULAD_DB_HOST", "localhost")
    port: int = int(os.getenv("OULAD_DB_PORT", "5432"))
    database: str = os.getenv("OULAD_DB_NAME", "oulad")
    user: str = os.getenv("OULAD_DB_USER", "oulad_loader")
    password: str = os.getenv("OULAD_DB_PASSWORD", "")

    def connect_kwargs(self):
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.database,
            "user": self.user,
            "password": self.password,
        }


CSV_FILES = {
    "courses": "courses.csv",
    "assessments": "assessments.csv",
    "student_info": "studentInfo.csv",
    "student_registration": "studentRegistration.csv",
    "student_assessment": "studentAssessment.csv",
    "student_vle": "studentVle.csv",
    "vle": "vle.csv",
}
