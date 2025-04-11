from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from ..utils import gen_time_hash


@dataclass(slots=True)
class Limit:
    id: str
    entity_id: str
    template_id: str
    is_allowed: bool
    last_reset: datetime


@dataclass(slots=True)
class LimitUpdate:
    entity_id: str | None = None
    template_id: str | None = None
    is_allowed: bool | None = None
    last_reset: datetime | None = None


class Limiter(ABC):
    @abstractmethod
    async def get(
        self,
        entity_id: str | None = None,
        limit_id: str | None = None,
        is_allowed: bool | None = None,
    ) -> List[Limit]:
        pass

    @abstractmethod
    async def create(self, limit: Limit) -> Limit:
        pass

    @abstractmethod
    async def update(self, limit_id: str, limit: LimitUpdate) -> Limit | None:
        pass

    @abstractmethod
    async def delete(self, limit_id: str) -> None:
        pass

    @staticmethod
    def change_id(value) -> str:
        time_hash = gen_time_hash()
        return f"{value}_{time_hash}"
