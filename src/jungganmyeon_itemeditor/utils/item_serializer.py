from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Any

from endstone.enchantments import Enchantment
from endstone.inventory import ItemStack
from ruamel.yaml import YAML

from jungganmyeon_itemeditor.utils.color import translate

if TYPE_CHECKING:
    from endstone.inventory import ItemMeta


ItemData = dict[str, Any]
_yaml = YAML()
_yaml.default_flow_style = False


def serialize_item(item: ItemStack, tag: str) -> ItemData:
    meta = item.item_meta
    data: ItemData = {"material": str(item.type), "amount": int(item.amount)}

    if meta is not None:
        if meta.has_display_name:
            data["name"] = meta.display_name
        if meta.has_lore:
            data["lore"] = list(meta.lore)
        if meta.has_damage:
            data["damage"] = meta.damage
        if meta.is_unbreakable:
            data["unbreakable"] = True
        if meta.has_enchants:
            data["enchant"] = {_enchant_to_str(e): lvl for e, lvl in meta.enchants.items()}

    return data


def deserialize_item(data: ItemData) -> ItemStack | None:
    material = data.get("material")
    if not material:
        return None

    try:
        item = ItemStack(material)
    except Exception:
        return None

    item.amount = data.get("amount", 1)
    meta = item.item_meta
    if meta is None:
        return item

    if "name" in data:
        meta.display_name = translate(str(data["name"]))

    if "lore" in data:
        raw_lore = data["lore"]
        if isinstance(raw_lore, list):
            meta.lore = [translate(str(line)) for line in raw_lore]

    if "damage" in data:
        meta.damage = int(data["damage"])

    if "unbreakable" in data:
        meta.is_unbreakable = bool(data["unbreakable"])

    if "enchant" in data:
        raw_enchants = data["enchant"]
        if isinstance(raw_enchants, dict):
            for ench_name, level in raw_enchants.items():
                enchant = _resolve_enchantment(ench_name)
                if enchant is not None:
                    meta.add_enchant(enchant, int(level), True)

    item.set_item_meta(meta)
    return item


def _resolve_enchantment(name: str) -> str | None:
    if ":" not in name:
        name = f"minecraft:{name.lower()}"
    else:
        name = name.lower()

    try:
        enchant = Enchantment.get(name)
        if enchant is not None:
            return name
    except Exception:
        pass
    return None


def _enchant_to_str(enchant: Enchantment | str) -> str:
    if isinstance(enchant, str):
        return enchant
    return getattr(enchant, "id", str(enchant))


def dump_yaml(data: dict[str, Any]) -> str:
    stream = StringIO()
    _yaml.dump(data, stream)
    return stream.getvalue()


def load_yaml(content: str) -> dict[str, Any]:
    return _yaml.load(content) or {}
