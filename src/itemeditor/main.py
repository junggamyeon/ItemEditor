
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from endstone import ColorFormat, Server
from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from itemeditor.commands.command_handler import CommandHandler
from itemeditor.managers.config_manager import ConfigManager
from itemeditor.managers.item_manager import ItemManager
from itemeditor.utils.item_serializer import dump_yaml

if TYPE_CHECKING:
    from endstone import Logger


class ItemEditor(Plugin):
    api_version = "0.11"
    prefix = "§b§l[ItemEditor]§r"
    version = "1.0.0"
    description = "Create, manage, and spawn custom items with extended enchantments."
    authors = ["ServerDev"]

    commands = {
        "ie": {
            "description": "ItemEditor main command",
            "usages": [
                "/ie",
                "/ie create",
                "/ie create <tag: string>",
                "/ie list",
                "/ie take <item: string>",
                "/ie reload",
            ],
            "permissions": ["itemeditor.command.ie"],
        },
    }

    permissions = {
        "itemeditor.command.ie": {"description": "Access to all ItemEditor commands", "default": "op"},
        "itemeditor.command.create": {"description": "Allow saving items to Item.yml", "default": "op"},
        "itemeditor.command.take": {"description": "Allow taking custom items", "default": "op"},
        "itemeditor.command.reload": {"description": "Allow reloading Item.yml", "default": "op"},
    }

    _instance: "ItemEditor | None" = None

    def __init__(self) -> None:
        super().__init__()
        self._command_handler: CommandHandler | None = None
        self._config_manager: ConfigManager | None = None
        self._item_manager: ItemManager | None = None

    @classmethod
    def get_instance(cls) -> "ItemEditor":
        if cls._instance is None:
            raise RuntimeError("ItemEditor has not been initialized")
        return cls._instance

    def on_load(self) -> None:
        ItemEditor._instance = self
        self._init_managers()

    def on_enable(self) -> None:
        self._command_handler = CommandHandler(self)
        items_data = self._config_manager.load()
        self._item_manager.reload(items_data)
        self._log_startup()

    def on_disable(self) -> None:
        self.logger.info(f"{ColorFormat.RED}ItemEditor disabled.")

    @property
    def config_manager(self) -> ConfigManager:
        if self._config_manager is None:
            raise RuntimeError("ConfigManager not initialized")
        return self._config_manager

    @property
    def item_manager(self) -> ItemManager:
        if self._item_manager is None:
            raise RuntimeError("ItemManager not initialized")
        return self._item_manager

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name != "ie" or self._command_handler is None:
            return False
        return self._command_handler.on_command(sender, args)

    def _init_managers(self) -> None:
        data_folder = str(Path(self.data_folder).resolve())
        self._config_manager = ConfigManager(data_folder, self.logger)
        self._config_manager.ensure_exists(self._default_item_yml())
        self._item_manager = ItemManager(self.logger)

    def _default_item_yml(self) -> str:
        default_items = {
            "example_sword": {
                "material": "minecraft:diamond_sword",
                "name": "&bExample Sword",
                "lore": ["&7Custom Lore", "&eVery Strong"],
                "damage": 20,
                "unbreakable": True,
                "enchant": {"minecraft:mending": 100000, "minecraft:sharpness": 5000},
            },
            "dragon_pickaxe": {
                "material": "minecraft:diamond_pickaxe",
                "name": "&5&lDragon Pickaxe",
                "lore": ["&7Mine anything instantly", "&cOwner only!"],
                "unbreakable": True,
                "enchant": {"minecraft:efficiency": 5000, "minecraft:unbreaking": 1000, "minecraft:mending": 50000},
            },
            "god_axe": {
                "material": "minecraft:netherite_axe",
                "name": "&6&lGod Axe",
                "lore": ["&7Forged by the gods", "&eUnstoppable power"],
                "unbreakable": True,
                "enchant": {"minecraft:sharpness": 10000, "minecraft:fire_aspect": 5000, "minecraft:mending": 100000},
            },
        }
        return dump_yaml({"items": default_items})

    def _log_startup(self) -> None:
        self.logger.info(f"{ColorFormat.GREEN}═══════════════════════════════════════")
        self.logger.info(f"{ColorFormat.GREEN}  ItemEditor v{self.version} enabled!")
        self.logger.info(f"{ColorFormat.GREEN}  Config: Item.yml")
        self.logger.info(f"{ColorFormat.GREEN}  Commands: /ie create | list | take | reload")
        self.logger.info(f"{ColorFormat.GREEN}═══════════════════════════════════════")
