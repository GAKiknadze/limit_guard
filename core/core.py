from typing import Tuple

from .counter import Counter, InMemoryCounter
from .exceptions import BadSpecification, ObjectNotFound
from .limiter import InMemoryLimiter, Limit, Limiter, LimitUpdate
from .templater import InMemoryTemplater, Template, Templater, TemplateUpdate


class Core:
    __cache_used: bool = False

    __templater: Templater
    __limiter: Limiter
    __counter: Counter
    __cache_templater: Templater | None = None
    __cache_limiter: Limiter | None = None
    __cache_counter: Counter | None = None

    def __init__(
        self,
        templater: Templater,
        limiter: Limiter,
        counter: Counter,
        cache_templater: Templater | None = None,
        cache_limiter: Limiter | None = None,
        cache_counter: Counter | None = None,
    ):
        self.__templater = templater
        self.__limiter = limiter
        self.__counter = counter

        if any((cache_templater, cache_limiter, cache_counter)):
            if all((cache_templater, cache_limiter, cache_counter)):
                self.__cache_templater = cache_templater
                self.__cache_limiter = cache_limiter
                self.__cache_counter = cache_counter
                self.__cache_used = True
            else:
                raise BadSpecification(
                    "Not all cache parameters are specified. Please check your code :)"
                )

    @staticmethod
    def __get_storages(
        value: str, *args, **kwargs
    ) -> Tuple[Templater, Limiter, Counter]:
        templater, limiter, counter = None, None, None
        if value.startswith("memory"):
            templater = InMemoryTemplater(*args, **kwargs)
            limiter = InMemoryLimiter(*args, **kwargs)
            counter = InMemoryCounter(*args, **kwargs)
        else:
            raise NotImplementedError(
                f"Storage type not implemented for path: `{value}`"
            )
        return templater, limiter, counter

    @classmethod
    def __new__(cls, main: str, cache: str | None = None) -> "Core":
        c_t, c_l, c_c = None, None, None

        tlc = cls.__get_storages(main)
        if cache is not None:
            c_t, c_l, c_c = cls.__get_storages(cache, is_cache=True)

        return cls(*tlc, c_t, c_l, c_c)

    async def template_create(self, template: Template) -> Template:
        saved_template = await self.__templater.create(template)

        if self.__cache_used:
            await self.__cache_templater.create(saved_template)  # type: ignore[union-attr]

        return saved_template

    async def template_update(
        self, template_id: str, template: TemplateUpdate
    ) -> Template:
        saved_template = await self.__templater.update(template_id, template)
        if saved_template is None:
            raise ObjectNotFound(f"Template with id `{template_id}` not found")

        if self.__cache_used:
            await self.__cache_templater.update(template_id, template)  # type: ignore[union-attr]

        return saved_template

    async def template_get_by_id(self, template_id: str) -> Template:
        if self.__cache_used:
            cached_template = await self.__cache_templater.get(template_id)  # type: ignore[union-attr]
            if cached_template is not None:
                return cached_template

        saved_template = await self.__templater.get(template_id)
        if saved_template is None:
            raise ObjectNotFound(f"Template with id `{template_id}` not found")

        return saved_template

    async def template_get_list(self):
        pass

    async def template_delete(self, template_id: str) -> None:
        await self.__templater.delete(template_id)
        if self.__cache_used:
            await self.__cache_templater.delete(template_id)  # type: ignore[union-attr]

    async def limit_create(self, limit: Limit) -> Limit:
        saved_limit = await self.__limiter.create(limit)

        if self.__cache_used:
            await self.__cache_limiter.create(saved_limit)  # type: ignore[union-attr]

        return saved_limit

    async def limit_update(self, limit_id: str, limit: LimitUpdate) -> Limit:
        saved_limit = await self.__limiter.update(limit_id, limit)
        if saved_limit is None:
            raise ObjectNotFound(f"Limit with id `{limit_id}` not found")

        if self.__cache_used:
            await self.__cache_limiter.update(limit_id, limit)  # type: ignore[union-attr]

        return saved_limit

    async def limit_get_by_id(self):
        pass

    async def limit_get_list(self):
        pass

    async def limit_delete(self, limit_id: str) -> None:
        await self.__limiter.delete(limit_id)
        await self.__counter.reset(limit_id)

        if self.__cache_used:
            await self.__cache_limiter.delete(limit_id)  # type: ignore[union-attr]
            await self.__cache_counter.reset(limit_id)  # type: ignore[union-attr]

    async def limit_usage(self):
        pass

    async def limit_consume(self):
        pass

    async def limit_reset(self):
        pass
