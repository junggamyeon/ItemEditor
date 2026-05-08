from __future__ import annotations

from typing import TYPE_CHECKING, Any

from itemeditor.utils.item_serializer import deserialize_item

if TYPE_CHECKING:
    from endstone.inventory import ItemStack


class ItemManager:
    def __init__(self, logger: Any) -> None:
        self._logger = logger
        self._registry: dict[str, dict[str, Any]] = {}
        self._built_cache: dict[str, ItemStack | None] = {}

    def reload(self, items_data: dict[str, dict[str, Any]]) -> None:
        self._registry = dict(items_data)
        self._built_cache.clear()
        self._logger.info(f"ItemManager reloaded — {len(self._registry)} item(s) cached")

    def get_item_data(self, tag: str) -> dict[str, Any] | None:
        return self._registry.get(tag)

    def build_item(self, tag: str) -> ItemStack | None:
        if tag in self._built_cache:
            return self._built_cache[tag]

        data = self._registry.get(tag)
        if data is None:
            self._built_cache[tag] = None
            return None

        item = deserialize_item(data)
        self._built_cache[tag] = item
        return item

    def get_all_tags(self) -> list[str]:
        return list(self._registry.keys())

    def has_tag(self, tag: str) -> bool:
        return tag in self._registry
