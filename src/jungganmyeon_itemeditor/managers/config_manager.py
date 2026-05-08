from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class ConfigManager:
    def __init__(self, data_folder: str, plugin_logger: Any) -> None:
        self._data_folder = Path(data_folder)
        self._items_file = self._data_folder / "Item.yml"
        self._logger = plugin_logger
        self._items_data: dict[str, Any] = {}
        self._loaded: bool = False
        self._yaml = YAML()
        self._yaml.default_flow_style = False
        self._yaml.preserve_quotes = True

    @property
    def items_file(self) -> Path:
        return self._items_file

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def ensure_exists(self, default_content: str | None = None) -> None:
        if self._items_file.exists():
            return

        self._data_folder.mkdir(parents=True, exist_ok=True)

        if default_content is not None:
            self._items_file.write_text(default_content, encoding="utf-8")
            self._logger.info(f"Created default Item.yml at {self._items_file}")
        else:
            self._items_file.write_text(
                "# ItemEditor — Custom Items Data\n"
                "# Edit this file to add, modify, or remove custom items.\n\n"
                "items: {}\n",
                encoding="utf-8",
            )
            self._logger.info(f"Created empty Item.yml at {self._items_file}")

    def load(self) -> dict[str, Any]:
        try:
            with self._items_file.open("r", encoding="utf-8") as f:
                raw = self._yaml.load(f)

            items = raw.get("items") if isinstance(raw, dict) else {}
            if not isinstance(items, dict):
                items = {}

            self._items_data = items
            self._loaded = True
            self._logger.info(f"Loaded {len(items)} item(s) from Item.yml")
            return items

        except Exception as e:
            self._logger.error(f"Failed to read Item.yml: {e}")
            self._items_data = {}
            self._loaded = False
            return {}

    def save(self, items: dict[str, Any]) -> bool:
        try:
            self._data_folder.mkdir(parents=True, exist_ok=True)

            content = [
                "# ItemEditor — Custom Items Data",
                "#",
                "# Edit this file to add, modify, or remove custom items.",
                "#",
                "# Available fields:",
                "#   material     — Minecraft item identifier (e.g. minecraft:diamond_sword)",
                "#   name         — Display name with color codes (&b, &c, &l, etc.)",
                "#   lore         — List of lore lines (supports color codes)",
                "#   amount       — Stack size (default: 1)",
                "#   damage       — Item damage value (0 = pristine)",
                "#   unbreakable  — true/false (infinite durability)",
                "#   enchant      — Dict of enchantment_id: level (bypasses vanilla limits)",
                "#",
                "# Color codes (use & instead of §):",
                "#   &0 Black  &1 Dark Blue  &2 Dark Green  &3 Dark Aqua",
                "#   &4 Dark Red  &5 Dark Purple  &6 Gold  &7 Gray",
                "#   &8 Dark Gray  &9 Blue  &a Green  &b Aqua",
                "#   &c Red  &d Light Purple  &e Yellow  &f White",
                "#   &k Obfuscated  &l Bold  &m Strikethrough",
                "#   &n Underline  &o Italic  &r Reset",
                "",
                "items:",
            ]

            for tag, data in items.items():
                content.append(f"  {tag}:")
                for key, value in data.items():
                    if isinstance(value, dict):
                        content.append(f"    {key}:")
                        for k, v in value.items():
                            content.append(f"      {k}: {v}")
                    elif isinstance(value, list):
                        content.append(f"    {key}:")
                        for v in value:
                            content.append(f"      - \"{v}\"")
                    else:
                        content.append(f"    {key}: {value}")

            self._items_file.write_text("\n".join(content) + "\n", encoding="utf-8")
            self._items_data = items
            return True

        except OSError as e:
            self._logger.error(f"Failed to write Item.yml: {e}")
            return False

    def add_item(self, tag: str, data: dict[str, Any]) -> bool:
        self._items_data[tag] = data
        return self.save(self._items_data)

    def remove_item(self, tag: str) -> bool:
        if tag in self._items_data:
            del self._items_data[tag]
            return self.save(self._items_data)
        return False

    def get_item_data(self, tag: str) -> dict[str, Any] | None:
        return self._items_data.get(tag)

    def get_all_tags(self) -> list[str]:
        return list(self._items_data.keys())

    def get_items_data(self) -> dict[str, Any]:
        return dict(self._items_data)

    def reload(self) -> dict[str, Any]:
        self._loaded = False
        return self.load()
