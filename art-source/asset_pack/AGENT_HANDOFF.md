# Agent handoff — Avatar Elements 2D art

## Start here
1. Run B0 repository audit first. Do not overwrite an existing asset before comparing its quality, dimensions, alpha, and provenance.
2. Read `docs/asset_manifest.json`; every crop record has `atlas_file`, `x`, `y`, `width`, and `height`.
3. Or use `python docs/crop_atlas.py --pack . --out extracted` to crop every atlas entry. Add `--name skill_fire_jab` to crop one item.

## Priority slice
- B1 Fire Jab art: `skill_fire_jab`, `particle_ember`, `particle_flame_tongue`, `particle_smoke_puff`, `flame_burst` frames, `fire_impact`, `ribbon_flame_edge`.
- B2 Fire Blast charge layers: `orb_fire_core`, `orb_fire_shell`, `orb_fire_orbit_ring`, `orb_fire_accent_particles`; only render when the verified server state says the skill is charging.
- B3 starters: Air `ribbon_soft_streak` / `ribbon_hard_crescent`; Water `ribbon_water_flow`, droplet/splash/foam; Earth dust/stone chip.
- B4 UI: 9-slice panel, roller, shared controls, theme trims, HUD pieces. Use the same widget system for all themes.

## Non-negotiable gameplay mapping
- Fire Jet is a dash, not a projectile. Fire Blast is the primary HOLD_RELEASE orb candidate.
- Water Whip is a whip/flow shape, not a charge orb. Air Staff Attack uses a staff trail.
- Lightning is a Fire sub-bending visual variant, not a fifth playable element.
- Orb components are cosmetic layers; no OrbEntity for a hand-attached charge phase. Spawn a projectile entity only when gameplay actually releases a projectile.
- Never infer damage, chi, cooldown, hitbox, material, collision, unlock, or server state from artwork.

## Technical caveats
- PNGs are source artwork. The runtime renderer still needs to define blend/depth/light, UV, pivot, attachment, lifetime, LOD, and reduced-effects behavior.
- Tube/ribbon/cone/dome/funnel/wave-sheet geometry is renderer work, not supplied by a flat PNG.
- PAL rig/animation, SFX/OGG, particle registration/JSON, packet sync, renderer code, and server gameplay are not included.
- `runtime32` skill/status icons are downsampled convenience exports; source icons remain 128px.
- Material maps are 128x128 periodic texture seeds; visually inspect tiling at runtime before treating them as final.
- This pack has not been integrated or runtime-verified in Minecraft 1.21.1.

## Armor, Weapons & Active Combo Synergy Expansion (Atlases 23–26)
- **7 Armor Sets (28 pieces)**: Icons in `23_armor_sets_icons.png`, humanoid layers in `assets/avatar_elements/textures/models/armor/*_layer_1/2.png`, 3D Blockbench models in `models/bbmodel/armor/`, and capabilities in `data/avatar_elements/capabilities/armors/`.
- **16 Canonical Weapons & Shields**: Icons in `24_canonical_weapons.png`, 3D models in `models/bbmodel/weapons/`, handheld item JSONs in `assets/avatar_elements/models/item/`, and capabilities in `data/avatar_elements/capabilities/weapons/`.
- **8 Weapon Swing Trails & Imbue Skins**: Seamless trails in `25_weapon_swing_trails.png` (`128x32` in `assets/avatar_elements/textures/vfx/trail_*_128x32.png`) and per-element trail configs in `assets/avatar_elements/item_skins/weapon_*.json`.
- **12 Active Weapon + Full-Set + Element Combos**: Icons in `26_weapon_combo_icons.png`, PAL animations in `animations/pal/combos/`, and declarative synergy rules in `data/avatar_elements/synergies/weapon_armor_element_combos.json`.
- Read `docs/ARMOR_WEAPON_RESEARCH_SPEC.md` for the full B0 audit and runtime integration checklist.
