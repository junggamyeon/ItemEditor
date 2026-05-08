<div align="center">

  <img src="icon.png" width="160" height="160">

  <h2>ItemEditor</h2>
  <p><b>A production-quality Endstone Bedrock Server plugin for creating, saving, and spawning custom items with extended enchantment levels.</b></p>

</div>

<h3>Features</h3>

- **`/ie create`** — Save the item in your main hand to `Item.yml` with a unique tag
- **`/ie take <item>`** — Spawn any registered custom item into your inventory
- **`/ie list`** — View all registered item tags
- **`/ie reload`** — Hot-reload `Item.yml` without restarting the server
- **Extended enchantments** — Set enchantment levels far beyond vanilla caps (e.g. `MENDING: 100000`)
- **Custom metadata** — Set custom display names, lore, damage values, and unbreakability
- **Permission-based** — All commands require operator (configurable)
- **Hot-reload** — Reload items at runtime without restart

<h3>Commands</h3>

| Command | Permission | Description |
|---------|-----------|-------------|
| `/ie create` | `itemeditor.command.create` | Save held item to Item.yml |
| `/ie take <item>` | `itemeditor.command.take` | Give yourself a custom item |
| `/ie list` | `itemeditor.command.ie` | List all registered item tags |
| `/ie reload` | `itemeditor.command.reload` | Reload Item.yml |

<h3>Item.yml Format</h3>

```yaml
items:
  my_sword:
    material: minecraft:diamond_sword
    name: "&b&lEpic Sword"
    lore:
      - "&7Forged in the nether"
      - "&cDeal massive damage"
    damage: 20
    unbreakable: true
    enchant:
      minecraft:sharpness: 5000
      minecraft:mending: 100000
```

<h3>Available Fields</h3>

| Field | Type | Description |
|-------|------|-------------|
| `material` | string | Minecraft item ID (e.g. `minecraft:diamond_sword`) |
| `name` | string | Display name with color codes |
| `lore` | list[string] | Item lore lines |
| `amount` | int | Stack size (default: 1) |
| `damage` | int | Item damage value |
| `unbreakable` | bool | Infinite durability |
| `enchant` | dict | `enchant_id: level` pairs |

<h3>Permissions</h3>

| Permission | Default | Description |
|------------|---------|-------------|
| `itemeditor.command.ie` | OP | Master permission (covers all subcommands) |
| `itemeditor.command.create` | OP | Save items |
| `itemeditor.command.take` | OP | Take items |
| `itemeditor.command.reload` | OP | Reload config |

<h3>License</h3>

MIT License - See [LICENSE](LICENSE) file for details.
