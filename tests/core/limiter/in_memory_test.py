from datetime import datetime, timedelta

import pytest

from core.limiter import InMemoryLimiter, Limit, LimitUpdate


@pytest.mark.asyncio
class TestInMemoryLimiter:
    @pytest.fixture
    async def limiter(self):
        return InMemoryLimiter()

    @pytest.fixture
    def sample_limit(self) -> Limit:
        return Limit(
            id="test",
            entity_id="user_1",
            template_id="template_A",
            is_allowed=True,
            last_reset=datetime.utcnow(),
        )

    async def test_create_and_get_basic(self, limiter, sample_limit):
        created = await limiter.create(sample_limit)
        assert created.id != sample_limit.id
        assert "_" in created.id

        result = await limiter.get(entity_id=created.entity_id, limit_id=created.id)
        assert len(result) == 1
        assert result[0] == created

    async def test_get_filters(self, limiter):
        l1 = await limiter.create(
            Limit(
                id="1",
                entity_id="user1",
                template_id="t1",
                is_allowed=True,
                last_reset=datetime.utcnow(),
            )
        )
        l2 = await limiter.create(
            Limit(
                id="2",
                entity_id="user1",
                template_id="t2",
                is_allowed=False,
                last_reset=datetime.utcnow(),
            )
        )
        l3 = await limiter.create(
            Limit(
                id="3",
                entity_id="user2",
                template_id="t1",
                is_allowed=True,
                last_reset=datetime.utcnow(),
            )
        )

        assert len(await limiter.get(entity_id="user1")) == 2
        # assert len(await limiter.get(limit_id="1")) == 1
        assert len(await limiter.get(entity_id="user1", is_allowed=False)) == 1

    async def test_update_changes_composite_key(self, limiter, sample_limit):
        created = await limiter.create(sample_limit)
        original_key = f"{created.entity_id}__{created.id}"

        update = LimitUpdate(entity_id="new_entity")
        updated = await limiter.update(created.id, update)

        assert original_key not in limiter._InMemoryLimiter__storage
        new_key = f"{updated.entity_id}__{updated.id}"
        assert new_key in limiter._InMemoryLimiter__storage

    async def test_delete_removes_from_storage(self, limiter, sample_limit):
        created = await limiter.create(sample_limit)
        key = f"{created.entity_id}__{created.id}"

        await limiter.delete(created.id)
        assert key not in limiter._InMemoryLimiter__storage

    async def test_update_partial_fields(self, limiter):
        original = await limiter.create(
            Limit(
                id="partial",
                entity_id="e1",
                template_id="t1",
                is_allowed=True,
                last_reset=datetime.utcnow(),
            )
        )

        new_time = datetime.utcnow() + timedelta(hours=1)
        update = LimitUpdate(is_allowed=False, last_reset=new_time)
        updated = await limiter.update(original.id, update)

        assert updated.is_allowed is False
        assert updated.last_reset == new_time
        assert updated.template_id == original.template_id

    async def test_edge_cases(self, limiter):
        assert await limiter.update("invalid", LimitUpdate()) is None

        await limiter.delete("invalid")

        assert len(await limiter.get()) == 0

    async def test_deepcopy_isolation(self, limiter, sample_limit):
        created = await limiter.create(sample_limit)
        created.is_allowed = False

        stored = await limiter.get(limit_id=created.id)
        assert stored[0].is_allowed != created.is_allowed

    async def test_id_generation_uniqueness(self, limiter, sample_limit):
        ids = set()
        for _ in range(5):
            limit = await limiter.create(sample_limit)
            ids.add(limit.id)

        assert len(ids) == 5
