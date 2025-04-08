from typing import Dict

from .counter import Counter


class InMemoryCounter(Counter):
    __storage: Dict[str, int]

    def __init__(self):
        super().__init__()
        self.__storage = dict()

    async def get(self, counter_id: str) -> int:
        return self.__storage.setdefault(counter_id, 0)

    async def increment(self, counter_id: str, value: int = 1) -> int:
        new_value = await self.get(counter_id) + value
        self.__storage.update({counter_id: new_value})
        return new_value

    async def decrement(self, counter_id: str, value: int = 1) -> int:
        new_value = max(await self.get(counter_id) - value, 0)
        self.__storage.update({counter_id: new_value})
        return new_value

    async def reset(self, counter_id: str) -> None:
        self.__storage.update({counter_id: 0})
