from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..utils import gen_time_hash


@dataclass
class Template:
    id: str
    max_value: int


@dataclass
class TemplateUpdate:
    max_value: int | None = None


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
