from abc import ABC, abstractmethod


class Counter(ABC):
    @abstractmethod
    async def get(self, counter_id: str) -> int:
        pass

    @abstractmethod
    async def increment(self, counter_id: str, value: int = 1) -> int:
        pass

    @abstractmethod
    async def decrement(self, counter_id: str, value: int = 1) -> int:
        pass

    @abstractmethod
    async def reset(self, counter_id: str) -> None:
        pass
