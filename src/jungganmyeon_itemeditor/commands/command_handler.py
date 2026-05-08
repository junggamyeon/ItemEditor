
from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING

from endstone import ColorFormat, Player
from endstone.command import CommandSender
from endstone.inventory import ItemStack

from jungganmyeon_itemeditor.utils.item_serializer import serialize_item

if TYPE_CHECKING:
    from jungganmyeon_itemeditor.main import ItemEditor


class CommandHandler:
    def __init__(self, plugin: ItemEditor) -> None:
        self._plugin = plugin

    def on_command(self, sender: CommandSender, args: list[str]) -> bool:
        if not args:
            return self._cmd_help(sender)

        sub = args[0].lower()
        rest = args[1:]

        match sub:
            case "create":
                return self._cmd_create(sender, rest)
            case "reload" | "rl":
                return self._cmd_reload(sender)
            case "list" | "ls":
                return self._cmd_list(sender)
            case "take" | "get" | "give":
                return self._cmd_take(sender, rest)
            case _:
                return self._cmd_help(sender)

    def _cmd_create(self, sender: CommandSender, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_message(f"{ColorFormat.RED}[ItemEditor] Only players can use this command.")
            return True

        player: Player = sender
        main_hand = player.inventory.item_in_main_hand

        if main_hand is None or main_hand.type == "minecraft:air":
            player.send_message(f"{ColorFormat.RED}[ItemEditor] No item in main hand.")
            return True

        tag = args[0] if args else _generate_tag(player.name)
        serialized = serialize_item(main_hand, tag)

        if self._plugin.config_manager.add_item(tag, serialized):
            self._plugin.item_manager.reload(self._plugin.config_manager.get_items_data())
            player.send_message(f"{ColorFormat.GREEN}[ItemEditor] Saved as {ColorFormat.YELLOW}'{tag}'")
            player.send_message(f"{ColorFormat.GRAY}  Material: {main_hand.type}")
        else:
            player.send_message(f"{ColorFormat.RED}[ItemEditor] Failed to save item.")
            self._plugin.logger.error(f"Failed to save item '{tag}' to Item.yml")

        return True

    def _cmd_reload(self, sender: CommandSender) -> bool:
        items_data = self._plugin.config_manager.reload()
        self._plugin.item_manager.reload(items_data)
        sender.send_message(f"{ColorFormat.GREEN}[ItemEditor] Reloaded — {ColorFormat.WHITE}{len(items_data)} item(s)")
        return True

    def _cmd_list(self, sender: CommandSender) -> bool:
        tags = self._plugin.item_manager.get_all_tags()

        if not tags:
            sender.send_message(f"{ColorFormat.YELLOW}[ItemEditor] No items. Use {ColorFormat.WHITE}/ie create")
            return True

        sender.send_message(f"{ColorFormat.GREEN}[ItemEditor] Items ({len(tags)}):")

        for tag in sorted(tags):
            data = self._plugin.item_manager.get_item_data(tag)
            name = _strip_color(data["name"]) if data and "name" in data else tag
            sender.send_message(f"  {ColorFormat.AQUA}{tag} {ColorFormat.GRAY}({name})")

        return True

    def _cmd_take(self, sender: CommandSender, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_message(f"{ColorFormat.RED}[ItemEditor] Only players can use this command.")
            return True

        if not args:
            sender.send_message(f"{ColorFormat.RED}[ItemEditor] Usage: {ColorFormat.WHITE}/ie take <item>")
            sender.send_message(f"{ColorFormat.GRAY}Use {ColorFormat.WHITE}/ie list")
            return True

        player: Player = sender
        resolved_tag = self._resolve_tag(args[0])

        if resolved_tag is None:
            player.send_message(f"{ColorFormat.RED}[ItemEditor] Item not found: '{args[0]}'")
            sender.send_message(f"{ColorFormat.GRAY}Use {ColorFormat.WHITE}/ie list")
            return True

        item = self._plugin.item_manager.build_item(resolved_tag)
        if item is None:
            player.send_message(f"{ColorFormat.RED}[ItemEditor] Failed to build item.")
            return True

        leftover = player.inventory.add_item(item)

        if not leftover:
            player.send_message(f"{ColorFormat.GREEN}[ItemEditor] Received: {ColorFormat.YELLOW}{_item_display_name(item)}")
        else:
            player.send_message(f"{ColorFormat.YELLOW}[ItemEditor] Inventory full.")

        return True

    def _resolve_tag(self, query: str) -> str | None:
        query_lower = query.lower()
        all_tags = self._plugin.item_manager.get_all_tags()

        for tag in all_tags:
            if tag.lower() == query_lower:
                return tag

        for tag in all_tags:
            data = self._plugin.item_manager.get_item_data(tag)
            if data and "name" in data and _strip_color(data["name"]).lower() == query_lower:
                return tag

        for tag in all_tags:
            if query_lower in tag.lower():
                return tag

        for tag in all_tags:
            data = self._plugin.item_manager.get_item_data(tag)
            if data and "name" in data and query_lower in _strip_color(data["name"]).lower():
                return tag

        return None

    def _cmd_help(self, sender: CommandSender) -> bool:
        sender.send_message(f"{ColorFormat.GREEN}=== ItemEditor ===")
        sender.send_message(f"{ColorFormat.WHITE}/ie create [tag] {ColorFormat.GRAY}— Save held item")
        sender.send_message(f"{ColorFormat.WHITE}/ie list {ColorFormat.GRAY}— List all items")
        sender.send_message(f"{ColorFormat.WHITE}/ie take <item> {ColorFormat.GRAY}— Get an item")
        sender.send_message(f"{ColorFormat.WHITE}/ie reload {ColorFormat.GRAY}— Reload config")
        return True


def _generate_tag(player_name: str) -> str:
    safe_name = "".join(c if c.isalnum() else "_" for c in player_name.lower())
    return f"{safe_name}_{uuid.uuid4().hex[:6]}"


def _item_display_name(item: ItemStack) -> str:
    meta = item.item_meta
    if meta is not None and meta.has_display_name:
        return meta.display_name
    return item.type


def _strip_color(text: str) -> str:
    return re.sub(r"[&§][0-9a-fk-or]", "", text, flags=re.IGNORECASE)
