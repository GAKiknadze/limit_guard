from copy import deepcopy
from dataclasses import asdict
from typing import Dict

from .templater import Template, Templater, TemplateUpdate


class InMemoryTemplater(Templater):
    __storage: Dict[str, Template]
    __is_cache: bool = False

    def __init__(self, is_cache: bool | None = None):
        super().__init__()
        self.__storage = dict()
        if is_cache:
            self.__is_cache = is_cache

    async def get(self, template_id: str) -> Template | None:
        return self.__storage.get(template_id)

    async def create(self, template: Template) -> Template:
        new_id = template.id
        if not self.__is_cache:
            new_id = self.change_id(template.id)

        new_template = Template(id=new_id, max_value=template.max_value)
        self.__storage[new_template.id] = new_template
        return deepcopy(new_template)

    async def update(
        self, template_id: str, template: TemplateUpdate
    ) -> Template | None:
        saved_template = await self.get(template_id)
        if saved_template is None:
            return None

        for key, value in asdict(template).items():
            if value is not None and hasattr(saved_template, key):
                setattr(saved_template, key, value)

        self.__storage.update({template_id: saved_template})
        return deepcopy(saved_template)

    async def delete(self, template_id: str) -> None:
        self.__storage.pop(template_id, None)
