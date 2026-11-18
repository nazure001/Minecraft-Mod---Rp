
# 🪨 Earth Pillar 3D Asset Specification & Handoff (Canon v2 — ATLA/LOK)
> **Author:** Antigravity IDE (3D Asset Production Lead)
> **Consumer:** Claude Code (Runtime Implementer) & User (QA Reviewer)
> **Target:** Minecraft Fabric 1.21.1 (Client-only VFX Pillar)
> **Status:** Asset Complete — Canon Revised per ATLA/LOK Source Material
> **Canon Sources:** ATLA S2E01, S2E07 (Earth Rumble VI), LOK S1 Pro-bending arena

---

## Canon Accuracy Notes (v2 Revision)

| Element | Old (v1) | New (v2 Canon) | ATLA Source |
| :--- | :--- | :--- | :--- |
| **Crown shape** | Pyramid spire (non-canon) | Crenelated flat crown — 3 blunt protrusions | S2E07 Earth Rumble pillars |
| **Jade vein** | Present (green accent) | Removed — standard pillar has NO jade | Jade = special locations / metalbending |
| **Texture palette** | Dark grey-green | Warm grey granite + reddish-brown soil | ATLA Earth Kingdom stone palette |
| **Eruption timing** | 0.14s to full height (slow) | 0.06s to full height (explosive) | ATLA animation: ~1-2 frames at 24fps |
| **Column taper** | Moderate pyramid taper | Near-uniform width (monolithic) | Hung Ga stance = rooted/blocky |
| **Rupture shards** | Tall pointed (22.5 deg tilt) | Wide flat plates (15 deg shallow) | Ground crack plates, not rock spikes |
| **Hold duration** | 0.22-0.75s | 0.10-0.80s | ATLA pillar = combat platform, long hold |

---

## 1. Asset Files Summary & Locations

| Component | File Path | Format / Spec |
| :--- | :--- | :--- |
| **Blockbench Project** | `art-source/asset_pack/models/bbmodel/earth_pillar.bbmodel` | Blockbench 4.10 project file, hierarchy, UVs, embedded texture & eruption keyframes. |
| **Universal 3D Mesh** | `art-source/asset_pack/meshes/vfx/earth_pillar.obj` | Metric scale 1.0 (1 unit = 0.0625m, total height 2.875m), ground pivot at (0,0,0). |
| **Material Library** | `art-source/asset_pack/meshes/vfx/earth_pillar.mtl` | Links to earth_pillar.png. |
| **Bedrock Geometry** | `art-source/asset_pack/models/earth_pillar.geo.json` | Format 1.12.0, identifier geometry.earth_pillar. |
| **Java Display Model** | `art-source/asset_pack/models/earth_pillar.json` | Compatible with BlockDisplayEntity / ItemDisplayEntity. |
| **Texture Atlas** | `art-source/asset_pack/assets/avatar_elements/textures/vfx/earth_pillar.png` | 64x64 PNG — warm granite strata, reddish-brown soil base, dry crack (NO jade). |
| **Emergence Animation**| `art-source/asset_pack/animations/earth_pillar.animation.json` | 1.3s eruption timeline — canon ATLA speed (0.06s rise), long hold, rapid fractured crumble. |
| **3D Turntable GIF** | `art-source/asset_pack/previews/earth_pillar/earth_pillar_turntable.gif` | 360 degree rotating render. |
| **Isometric Preview** | `art-source/asset_pack/previews/earth_pillar/earth_pillar_isometric.png` | Isometric beauty render with ground contact marker. |

---

## 2. Geometry & Coordinate System Alignment

* **Ground Pivot Point:** Asset origin (0.0, 0.0, 0.0) is at the ground contact point.
* **Column Height:** Y = 0.0 to Y = 46.0 units (2.875 blocks / meters).
* **Footprint:** Foundation slab [-11, +11] units; radial debris up to 1.6 blocks. Aligns with FOOTPRINT_RADIUS = 1.6f in EarthPillarSkill.java.
* **Crown:** Flat-topped crenelated (3 protrusions) — canonical ATLA monolith, NOT spire/pyramid.

```
       *  Y = +2.88m (46u) -- Crown Protrusion A (tallest tooth)
       |  Y = +2.78m (44.5)-- Crown Protrusion B
       |  Y = +2.63m (42u) -- Crown Platform Slab (combat stance)
       |  Y = +2.50m (40u) -- Upper Column Top
       |  Y = +2.00m (32u) -- Mid-Upper Column Join
       |  Y = +1.25m (20u) -- Lower-Mid Column Join
       |  Y = +0.19m ( 3u) -- Basal Slab Top
-------+----------------------- Ground Surface (Y = 0.0, Pivot)
       v  Y = -0.25m (-4u) -- Subterranean Anchor
```

---

## 3. Canon-Accurate Animation Timeline (For Claude Code)

```
t = 0.00s : Start -- fully underground (Y = -48 units)
t = 0.03s : Burst begins -- linear rise, NO ease-in (earthbending is abrupt)
t = 0.06s : FULL HEIGHT -- overshoot to Y = +1.5
t = 0.10s : SLAM SETTLE -- locks to Y = 0 (heavy SFX cue)
t = 0.80s : HOLD END -- rigid platform hold (0.70s long, combat use)
t = 0.90s : CRUMBLE STAGE 1 -- drops to Y = -8 (fractured, NOT smooth)
t = 1.05s : CRUMBLE STAGE 2 -- drops to Y = -28 (rapid fragmentation)
t = 1.20s : FULLY SUBMERGED -- Y = -48, despawn trigger
```

---

## 4. Verification Checklist

- [x] Ground pivot is at (0, 0, 0).
- [x] Bounding box does not exceed footprint radius 1.6 blocks.
- [x] Texture is 64x64 ATLA canon palette (warm granite, reddish soil, NO jade).
- [x] Crown geometry is FLAT-TOPPED crenelated, not pyramid/spire.
- [x] Eruption timing matches ATLA animation speed (0.06s to full height).
- [x] No modifications made to mod/src/ runtime code.
- [x] Universal .bbmodel, .obj, .geo.json, and .json formats provided.
