# 🌊 Avatar: The Last Airbender — 7-Tier Elemental Armor Resource Pack 🌪️

Official companion **Resource Pack** for the **Avatar Armor Datapack**, engineered strictly for **Minecraft Java Edition 1.21.1** (`pack_format: 34`).

> [!IMPORTANT]
> **Minecraft Java Version 1.21.1 Compatibility (`pack_format: 34`)**
> In Minecraft 1.21.1, `minecraft:equippable` and `minecraft:item_model` do not exist (they were added in 1.21.2/1.21.4).
> This resource pack implements the battle-tested, 100% vanilla-compatible 1.21.1 architecture:
> - **Item Model Overrides**: Defined in `assets/minecraft/models/item/` for Leather, Chainmail, Iron, Diamond, and Netherite armor pieces via `custom_model_data`.
> - **Custom Armor Visuals**: Rendered in-game via vanilla's `minecraft:trim` system with dedicated materials and trim patterns for all 28 sets.
> - **112 Unique 16x16 Pixel Art Icons**: One distinct inventory and held item texture for every single piece across all 4 nations and 7 tiers!

---

## 🌟 Visual Showcase & Custom Model Data (CMD)

CMD follows the intuitive format `NTPP` where:
- `N`: Nation (1 = Fire, 2 = Water, 3 = Earth, 4 = Air)
- `T`: Tier (1 = Initiate, 2 = Apprentice, 3 = Adept, 4 = Veteran, 5 = Master, 6 = Mythic, 7 = Sovereign)
- `PP`: Piece (01 = Helmet, 02 = Chestplate, 03 = Leggings, 04 = Boots)

| Nation | Tier | Base Item | Trim Material & Pattern | Custom Model Data |
| :--- | :--- | :--- | :--- | :--- |
| **🔥 Fire** | I: Initiate | Leather | `minecraft:redstone` + `sentry` | 1101..1104 |
| **🔥 Fire** | II: Apprentice | Chainmail | `minecraft:copper` + `dune` | 1201..1204 |
| **🔥 Fire** | III: Adept | Iron | `minecraft:redstone` + `wild` | 1301..1304 |
| **🔥 Fire** | IV: Veteran | Iron (Reinf.) | `minecraft:copper` + `host` | 1401..1404 |
| **🔥 Fire** | V: Master | Diamond | `minecraft:gold` + `vex` | 1501..1504 |
| **🔥 Fire** | VI: Mythic | Netherite | `minecraft:netherite` + `spire` | 1601..1604 |
| **🔥 Fire** | VII: Sovereign | Netherite (Godplate) | `minecraft:redstone` + `silence` | 1701..1704 |
| **🌊 Water** | I: Initiate | Leather | `minecraft:lapis` + `coast` | 2101..2104 |
| **🌊 Water** | II: Apprentice | Chainmail | `minecraft:lapis` + `dune` | 2201..2204 |
| **🌊 Water** | III: Adept | Iron | `minecraft:diamond` + `wild` | 2301..2304 |
| **🌊 Water** | IV: Veteran | Iron (Reinf.) | `minecraft:lapis` + `host` | 2401..2404 |
| **🌊 Water** | V: Master | Diamond | `minecraft:amethyst` + `eye` | 2501..2504 |
| **🌊 Water** | VI: Mythic | Netherite | `minecraft:diamond` + `spire` | 2601..2604 |
| **🌊 Water** | VII: Sovereign | Netherite (Godplate) | `minecraft:lapis` + `silence` | 2701..2704 |
| **🪨 Earth** | I: Initiate | Leather | `minecraft:emerald` + `coast` | 3101..3104 |
| **🪨 Earth** | II: Apprentice | Chainmail | `minecraft:copper` + `dune` | 3201..3204 |
| **🪨 Earth** | III: Adept | Iron | `minecraft:emerald` + `wild` | 3301..3304 |
| **🪨 Earth** | IV: Veteran | Iron (Reinf.) | `minecraft:iron` + `host` | 3401..3404 |
| **🪨 Earth** | V: Master | Diamond | `minecraft:gold` + `eye` | 3501..3504 |
| **🪨 Earth** | VI: Mythic | Netherite | `minecraft:netherite` + `spire` | 3601..3604 |
| **🪨 Earth** | VII: Sovereign | Netherite (Godplate) | `minecraft:emerald` + `silence` | 3701..3704 |
| **💨 Air** | I: Initiate | Leather | `minecraft:gold` + `coast` | 4101..4104 |
| **💨 Air** | II: Apprentice | Chainmail | `minecraft:copper` + `dune` | 4201..4204 |
| **💨 Air** | III: Adept | Iron | `minecraft:quartz` + `wild` | 4301..4304 |
| **💨 Air** | IV: Veteran | Iron (Reinf.) | `minecraft:gold` + `host` | 4401..4404 |
| **💨 Air** | V: Master | Diamond | `minecraft:gold` + `vex` | 4501..4504 |
| **💨 Air** | VI: Mythic | Netherite | `minecraft:diamond` + `spire` | 4601..4604 |
| **💨 Air** | VII: Sovereign | Netherite (Godplate) | `minecraft:quartz` + `silence` | 4701..4704 |

---

## 📂 Resource Pack Architecture

```
avatar-armor-resourcepack/
├── pack.mcmeta                                    # pack_format: 34 (1.21.1)
├── pack.png                                       # Preserved official logo
├── generate_textures.py                           # 112 Texture generator script
├── create_evolution_sheet.py                      # 7-Tier Evolution comparison generator
├── create_preview.py                              # 7-Tier Showcase poster generator
├── README.md                                      # Documentation
└── assets/
    ├── minecraft/
    │   └── models/
    │       └── item/                              # 20 Vanilla Armor Model Overrides
    │           ├── leather_{helmet,chestplate,leggings,boots}.json
    │           ├── chainmail_{helmet,chestplate,leggings,boots}.json
    │           ├── iron_{helmet,chestplate,leggings,boots}.json
    │           ├── diamond_{helmet,chestplate,leggings,boots}.json
    │           └── netherite_{helmet,chestplate,leggings,boots}.json
    └── avatar/
        ├── models/
        │   └── item/                              # 112 Item Models (+ Legacy Aliases)
        │       ├── fire_initiate_helmet.json
        │       ├── fire_apprentice_helmet.json
        │       ├── ...
        └── textures/
            ├── item/                              # 112 16x16 Pixel Art Textures (+ Aliases)
            │   ├── fire_initiate_helmet.png
            │   ├── fire_apprentice_helmet.png
            │   ├── ...
            └── entity/
                └── equipment/                     # 8 Entity Layer Textures (64x32)
```

---

## 🛠️ Texture Generation & Maintenance

All 112 textures, entity layers, and evolution sheets can be regenerated deterministically:

```bash
python generate_textures.py
python create_evolution_sheet.py
python create_preview.py
```
