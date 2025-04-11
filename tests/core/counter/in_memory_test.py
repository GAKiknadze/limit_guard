import pytest

from core.counter import InMemoryCounter


@pytest.mark.asyncio
class TestInMemoryCounter:
    async def test_initial_storage_is_empty(self):
        counter = InMemoryCounter()
        assert len(counter._InMemoryCounter__storage) == 0

    async def test_get_returns_zero_for_new_counter_id(self):
        counter = InMemoryCounter()
        value = await counter.get("test")
        assert value == 0

    async def test_increment_updates_value_correctly(self):
        counter = InMemoryCounter()

        result = await counter.increment("test", 5)
        assert result == 5
        assert counter._InMemoryCounter__storage["test"] == 5

        result = await counter.increment("test", 3)
        assert result == 8
        assert counter._InMemoryCounter__storage["test"] == 8

    async def test_decrement_updates_value_correctly(self):
        counter = InMemoryCounter()

        await counter.increment("test", 10)

        result = await counter.decrement("test", 3)
        assert result == 7
        assert counter._InMemoryCounter__storage["test"] == 7

        result = await counter.decrement("test", 10)
        assert result == 0
        assert counter._InMemoryCounter__storage["test"] == 0

    async def test_reset_sets_value_to_zero(self):
        counter = InMemoryCounter()

        await counter.increment("test", 7)
        await counter.reset("test")

        assert counter._InMemoryCounter__storage["test"] == 0

    async def test_default_increment_value_is_one(self):
        counter = InMemoryCounter()
        result = await counter.increment("test")
        assert result == 1
        assert counter._InMemoryCounter__storage["test"] == 1

    async def test_default_decrement_value_is_one(self):
        counter = InMemoryCounter()
        await counter.increment("test", 5)
        result = await counter.decrement("test")
        assert result == 4
        assert counter._InMemoryCounter__storage["test"] == 4
