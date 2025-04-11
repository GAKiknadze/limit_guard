from copy import deepcopy
from dataclasses import asdict
from typing import Dict, List

from .limiter import Limit, Limiter, LimitUpdate


class InMemoryLimiter(Limiter):
    __storage: Dict[str, Limit]
    __is_cache: bool = False

    def __init__(self, is_cache: bool | None = None):
        super().__init__()
        self.__storage = dict()
        if is_cache:
            self.__is_cache = is_cache

    async def get(
        self,
        entity_id: str | None = None,
        limit_id: str | None = None,
        is_allowed: bool | None = None,
    ) -> List[Limit]:
        result, data = list(), list()

        match (entity_id, limit_id):
            case None, None:
                pass
            case _, None:
                data = [
                    v
                    for k, v in self.__storage.items()
                    if k.startswith(f"{entity_id}__")
                ]
            case None, _:
                data = [
                    v for k, v in self.__storage.items() if k.endswith(f"__{limit_id}")
                ]
            case _, _:
                res = self.__storage.get(f"{entity_id}__{limit_id}")
                if res is not None:
                    data.append(res)

        if is_allowed is not None:
            for d in data:
                if d.is_allowed == is_allowed:
                    result.append(d)
        else:
            result = data

        return result

    async def create(self, limit: Limit) -> Limit:
        new_id = limit.id
        if not self.__is_cache:
            new_id = self.change_id(limit.id)

        new_limit = Limit(
            id=new_id,
            entity_id=limit.entity_id,
            template_id=limit.template_id,
            is_allowed=limit.is_allowed,
            last_reset=limit.last_reset,
        )
        composite_key = f"{new_limit.entity_id}__{new_limit.id}"
        self.__storage[composite_key] = new_limit
        return deepcopy(new_limit)

    async def update(self, limit_id: str, limit: LimitUpdate) -> Limit | None:
        old_limits = await self.get(limit_id=limit_id)
        if len(old_limits) != 1:
            return None
        old_limit = old_limits[0]

        updated_data = {
            **asdict(old_limit),
            **{k: v for k, v in asdict(limit).items() if v is not None},
        }
        new_limit = Limit(**updated_data)

        if limit.entity_id is not None and limit.entity_id != old_limit.entity_id:
            await self.delete(old_limit.id)

        composite_key = f"{new_limit.entity_id}__{new_limit.id}"
        self.__storage[composite_key] = new_limit
        return deepcopy(new_limit)

    async def delete(self, limit_id: str) -> None:
        limits = await self.get(limit_id=limit_id)
        if len(limits) != 1:
            return None

        limit = limits[0]
        self.__storage.pop(f"{limit.entity_id}__{limit.id}", None)
