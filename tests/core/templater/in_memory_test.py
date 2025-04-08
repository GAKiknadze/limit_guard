import pytest

from core.templater.in_memory import InMemoryTemplater, Template, TemplateUpdate


@pytest.mark.asyncio
class TestInMemoryTemplater:
    @pytest.fixture
    async def templater(self):
        return InMemoryTemplater()

    @pytest.fixture
    def sample_template(self) -> Template:
        return Template(id="original", max_value=100)

    async def test_initial_storage_is_empty(self, templater):
        assert await templater.get("any_id") is None

    async def test_create_generates_new_id(self, templater, sample_template):
        created = await templater.create(sample_template)
        assert created.id != "original"
        assert "_" in created.id

    async def test_create_stores_template(self, templater, sample_template):
        created = await templater.create(sample_template)
        stored = await templater.get(created.id)
        assert stored == created

    async def test_get_returns_deepcopy(self, templater, sample_template):
        created = await templater.create(sample_template)
        created.max_value = 200
        stored = await templater.get(created.id)
        assert stored.max_value == sample_template.max_value

    async def test_update_full(self, templater, sample_template):
        created = await templater.create(sample_template)
        update_data = TemplateUpdate(max_value=200)

        updated = await templater.update(created.id, update_data)
        assert updated.max_value == 200
        assert updated.id == created.id

    async def test_update_partial(self, templater):
        original = Template(id="test", max_value=100)
        created = await templater.create(original)

        update_data = TemplateUpdate(max_value=None)
        updated = await templater.update(created.id, update_data)

        assert updated.max_value == 100

    async def test_update_non_existing(self, templater):
        update_data = TemplateUpdate(max_value=200)
        result = await templater.update("non_existing", update_data)
        assert result is None

    async def test_delete_existing(self, templater, sample_template):
        created = await templater.create(sample_template)
        await templater.delete(created.id)
        assert await templater.get(created.id) is None

    async def test_delete_non_existing(self, templater):
        try:
            await templater.delete("non_existing")
        except Exception as e:
            pytest.fail(f"Unexpected exception: {e}")

    async def test_id_generation_format(self, templater, sample_template):
        created = await templater.create(sample_template)
        prefix, hash_part = created.id.split("_")
        assert prefix == "original"
        assert len(hash_part) == 8

    async def test_multiple_operations_flow(self, templater):
        template = await templater.create(Template(id="flow", max_value=10))
        original_id = template.id

        await templater.update(original_id, TemplateUpdate(max_value=20))
        updated = await templater.get(original_id)
        assert updated.max_value == 20

        await templater.delete(original_id)
        assert await templater.get(original_id) is None

    async def test_storage_isolation(self, templater):
        t1 = await templater.create(Template(id="test1", max_value=100))
        _ = await templater.create(Template(id="test2", max_value=200))

        assert len(templater._InMemoryTemplater__storage) == 2

        await templater.delete(t1.id)
        assert len(templater._InMemoryTemplater__storage) == 1

    async def test_update_does_not_affect_other_fields(self, templater):
        original = Template(id="test", max_value=100)
        created = await templater.create(original)

        await templater.update(created.id, TemplateUpdate(max_value=150))
        updated = await templater.get(created.id)

        assert updated.id == created.id
        assert updated.max_value == 150
