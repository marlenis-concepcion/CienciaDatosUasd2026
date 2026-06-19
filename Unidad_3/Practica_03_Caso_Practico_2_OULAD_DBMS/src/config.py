from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    random_state: int = 8237
    early_window_days: int = 28
    test_size: float = 0.25
    sample_size: int | None = None
    synthetic_only: bool = False

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def output_dir(self) -> Path:
        return self.root / "outputs"

    @property
    def archive_path(self) -> Path:
        return self.data_dir / "oulad.zip"
