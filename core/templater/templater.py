from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ..utils import gen_time_hash


class PeriodType(str, Enum):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"


@dataclass(slots=True)
class Template:
    id: str
    max_value: int | None = None
    period_count: int | None = None
    period_type: PeriodType | None = None


@dataclass(slots=True)
class TemplateUpdate:
    max_value: int | None = None
    period_count: int | None = None
    period_type: PeriodType | None = None


class Templater(ABC):
    @abstractmethod
    async def get(self, template_id: str) -> Template | None:
        pass

    @abstractmethod
    async def create(self, template: Template) -> Template:
        pass

    @abstractmethod
    async def update(
        self, template_id: str, template: TemplateUpdate
    ) -> Template | None:
        pass

    @abstractmethod
    async def delete(self, template_id: str) -> None:
        pass

    @staticmethod
    def change_id(value) -> str:
        time_hash = gen_time_hash()
        return f"{value}_{time_hash}"
