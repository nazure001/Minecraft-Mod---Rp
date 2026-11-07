# 🔥 Avatar: The Last Airbender — 7-Tier Elemental Armor Datapack 🌪️

A production-ready Minecraft Java Edition **1.21.1** Datapack introducing the legendary 7-Tier elemental armor progression system for the **Four Nations**: **Fire Nation**, **Water Tribe**, **Earth Kingdom**, and **Air Nomad** (28 Armor Sets, 112 Pieces).

> [!IMPORTANT]
> **Minecraft Java Version 1.21.1 Compatibility (`pack_format: 48`)**
> Built strictly for Minecraft 1.21.1 using native components (`minecraft:custom_data`, `minecraft:trim`, `minecraft:custom_model_data`, `minecraft:item_name`, `minecraft:lore`, `minecraft:attribute_modifiers`).
> Does **NOT** use `minecraft:equippable` or `minecraft:item_model` (which were only added in 1.21.2/1.21.4 and break 1.21.1 clients).

---

## ⚖️ Elemental Equality & 7-Tier Progression Architecture

**All 4 elements follow the exact same tier progression and max potential:**

```
Tier I: Initiate     Tier II: Apprentice     Tier III: Adept     Tier IV: Veteran     Tier V: Master      Tier VI: Mythic     Tier VII: Sovereign
[Leather Base]   ──> [Chainmail Base]    ──> [Iron Base]     ──> [Iron Reinf.]    ──> [Diamond Base]  ──> [Netherite]     ──> [Godplate]
Catalyst 1           Copper + Cat. 2         Iron + Cat. 3       Iron Block + Cat. 4  Diamond Block+Cat.5 Netherite + Cat. 6  Nether Star + Totem
```

Fire is **NOT** the highest tier. Fire, Water, Earth, and Air are 100% equal in tier standing, reaching Netherite base at Mythic and Sovereign Godplate with supreme attributes and particle auras!

---

## 🌟 Four Nations & 7-Tier Feature Matrix

| Nation | Tier I: Initiate (Leather) | Tier II: Apprentice (Chain) | Tier III: Adept (Iron) | Tier IV: Veteran (Iron+) | Tier V: Master (Diamond) | Tier VI: Mythic (Netherite) | Tier VII: Sovereign (Godplate) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **🔥 Fire Nation** | Fire Res I + Speed | Fire Res I + Speed I + Strength I | Fire Res + Str I + Spd I + Haste I | Fire Res + Str II + Spd I + Haste I | Fire Res + Str II + Spd II + Haste I | Fire Res + Str II + Spd II + Haste II + Regen I | **Sovereign Dragon Wrath**: Fire Res + Str III + Spd II + Haste II + Res II + Regen I + Living Dragon Sunfire Aura |
| **🌊 Water Tribe** | Water Breathing I | Water Breathing + Dolphin I | Water Breath + Dolphin + Regen I | Water Breath + Dolphin + Regen I + Res I | Water Breath + Dolphin + Regen II + Res I + Health I (+4 HP) | Water Breath + Dolphin + Regen II + Res II + Health II (+8 HP) | **Sovereign Ocean Spirit**: Water Breath + Dolphin + Conduit Power + Regen II + Res II + Health IV (+16 HP) + Tidal Aura |
| **🪨 Earth Kingdom** | Resistance I | Resistance I + Haste I | Resistance I + Haste I + Absorption I | Resistance II + Haste II | Resistance II + Haste II + Strength I + Health I (+4 HP) | Resistance III + Haste II + Strength II + Health II (+8 HP) | **Sovereign Mountain Titan**: Resistance III + Haste III + Strength II + Health IV (+16 HP) + Tremor Aura |
| **💨 Air Nomad** | Speed I + Jump Boost I | Speed I + Jump Boost I + Slow Falling | Speed II + Jump Boost II + Slow Falling | Speed II + Jump Boost II + Slow Falling + Haste I | Speed III + Jump Boost II + Slow Falling + Haste II | Speed III + Jump Boost III + Slow Falling + Haste II + Regen I | **Sovereign Avatar Nimbus**: Speed IV + Jump Boost III + Slow Falling + Haste III + Regen II + Glowing Avatar Arrow Aura |

---

## 🔨 Crafting & Upgrade System (112 Recipes)

All recipes are shapeless crafting recipes in `data/avatar/recipe/`:

### 1. Initiate Tier (Leather Base + Catalyst 1)
- **🔥 Fire Nation:** `minecraft:leather_<piece>` + **Blaze Powder**
- **🌊 Water Tribe:** `minecraft:leather_<piece>` + **Prismarine Shard**
- **🪨 Earth Kingdom:** `minecraft:leather_<piece>` + **Clay Ball**
- **💨 Air Nomad:** `minecraft:leather_<piece>` + **Feather**

### 2. Apprentice Tier (Initiate Piece + Copper Ingot + Catalyst 2 -> Chainmail Piece)
- **🔥 Fire Nation:** Fire Initiate Piece + **Copper Ingot** + **Magma Cream**
- **🌊 Water Tribe:** Water Initiate Piece + **Copper Ingot** + **Prismarine Crystals**
- **🪨 Earth Kingdom:** Earth Initiate Piece + **Copper Ingot** + **Bamboo**
- **💨 Air Nomad:** Air Initiate Piece + **Copper Ingot** + **Rabbit Hide**

### 3. Adept Tier (Apprentice Piece + Iron Ingot + Catalyst 3 -> Iron Piece)
- **🔥 Fire Nation:** Fire Apprentice Piece + **Iron Ingot** + **Blaze Rod**
- **🌊 Water Tribe:** Water Apprentice Piece + **Iron Ingot** + **Lapis Lazuli**
- **🪨 Earth Kingdom:** Earth Apprentice Piece + **Iron Ingot** + **Amethyst Shard**
- **💨 Air Nomad:** Air Apprentice Piece + **Iron Ingot** + **Phantom Membrane**

### 4. Veteran Tier (Adept Piece + Iron Block + Catalyst 4 -> Reinforced Iron Piece)
- **🔥 Fire Nation:** Fire Adept Piece + **Iron Block** + **Crying Obsidian**
- **🌊 Water Tribe:** Water Adept Piece + **Iron Block** + **Dark Prismarine**
- **🪨 Earth Kingdom:** Earth Adept Piece + **Iron Block** + **Emerald**
- **💨 Air Nomad:** Air Adept Piece + **Iron Block** + **White Wool**

### 5. Master Tier (Veteran Piece + Diamond Block + Catalyst 5 -> Diamond Piece)
- **🔥 Fire Nation:** Fire Veteran Piece + **Diamond Block** + **Magma Block**
- **🌊 Water Tribe:** Water Veteran Piece + **Diamond Block** + **Heart of the Sea**
- **🪨 Earth Kingdom:** Earth Veteran Piece + **Diamond Block** + **Emerald Block**
- **💨 Air Nomad:** Air Veteran Piece + **Diamond Block** + **Wind Charge**

### 6. Mythic Tier (Master Piece + Netherite Ingot + Catalyst 6 -> Netherite Piece)
- **🔥 Fire Nation:** Fire Master Piece + **Netherite Ingot** + **Dragon Breath**
- **🌊 Water Tribe:** Water Master Piece + **Netherite Ingot** + **Nautilus Shell**
- **🪨 Earth Kingdom:** Earth Master Piece + **Netherite Ingot** + **Obsidian**
- **💨 Air Nomad:** Air Master Piece + **Netherite Ingot** + **Breeze Rod**

### 7. Sovereign Tier (Mythic Piece + Nether Star + Totem of Undying -> Sovereign Godplate)
- **🔥 Fire Nation:** Fire Mythic Piece + **Nether Star** + **Totem of Undying**
- **🌊 Water Tribe:** Water Mythic Piece + **Nether Star** + **Totem of Undying**
- **🪨 Earth Kingdom:** Earth Mythic Piece + **Nether Star** + **Totem of Undying**
- **💨 Air Nomad:** Air Mythic Piece + **Nether Star** + **Totem of Undying**

---

## 💻 Commands & Give Functions

Give functions for every tier and element in `data/avatar/function/give/`:

### 1. By Nation and Tier:
```mcfunction
# Fire Nation
/function avatar:give/fire_initiate
/function avatar:give/fire_apprentice
/function avatar:give/fire_adept
/function avatar:give/fire_veteran
/function avatar:give/fire_master
/function avatar:give/fire_mythic
/function avatar:give/fire_sovereign

# Water Tribe
/function avatar:give/water_initiate
/function avatar:give/water_apprentice
/function avatar:give/water_adept
/function avatar:give/water_veteran
/function avatar:give/water_master
/function avatar:give/water_mythic
/function avatar:give/water_sovereign

# Earth Kingdom
/function avatar:give/earth_initiate
/function avatar:give/earth_apprentice
/function avatar:give/earth_adept
/function avatar:give/earth_veteran
/function avatar:give/earth_master
/function avatar:give/earth_mythic
/function avatar:give/earth_sovereign

# Air Nomad
/function avatar:give/air_initiate
/function avatar:give/air_apprentice
/function avatar:give/air_adept
/function avatar:give/air_veteran
/function avatar:give/air_master
/function avatar:give/air_mythic
/function avatar:give/air_sovereign
```

### 2. Shorthand Nation Commands (Gives Tier VII Sovereign Godplate):
```mcfunction
/function avatar:give/fire_nation
/function avatar:give/water_tribe
/function avatar:give/earth_kingdom
/function avatar:give/air_nomad
```

### 3. Backward Compatibility Aliases:
- `/function avatar:give/fire_basic` -> gives `fire_initiate`
- `/function avatar:give/fire_legendary` -> gives `fire_sovereign`
- `/function avatar:give/water_basic` -> gives `water_initiate`
- `/function avatar:give/water_legendary` -> gives `water_sovereign`
- `/function avatar:give/earth_basic` -> gives `earth_initiate`
- `/function avatar:give/earth_legendary` -> gives `earth_sovereign`
- `/function avatar:give/air_basic` -> gives `air_initiate`
- `/function avatar:give/air_legendary` -> gives `air_sovereign`

---

## 🛡️ Scoreboard & Technical Integration

- Scoreboard Objective: `avatar_set`
  - Values: `N T` (Nation: 1=Fire, 2=Water, 3=Earth, 4=Air; Tier: 1..7)
  - Fire: 11..17
  - Water: 21..27
  - Earth: 31..37
  - Air: 41..47
- Custom Model Data: `N T P P` (e.g. 1101 = Fire Initiate Helmet, 4704 = Air Sovereign Boots).
