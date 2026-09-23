from collections import UserDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskType(str, Enum):
    BINARY = "dicotomica"
    ORDINAL = "ordinal"
    REGRESSION = "intervalo_razon"


@dataclass(frozen=True)
class ModelResult:
    task: TaskType
    model: str
    metrics: dict[str, float]
    predictions: Any = field(repr=False)


class ResultRegistry(UserDict):
    """TAD colección para registrar resultados por tarea y modelo."""

    def add(self, result: ModelResult) -> None:
        self.data[(result.task.value, result.model)] = result

    def by_task(self, task: TaskType) -> list[ModelResult]:
        return [
            result
            for (task_name, _), result in self.data.items()
            if task_name == task.value
        ]
