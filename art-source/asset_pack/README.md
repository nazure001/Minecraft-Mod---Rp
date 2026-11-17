# Avatar Elements Asset Pack — 2026-11-08 (Full Production Bundle)

Target: Minecraft Java 1.21.1 / Fabric.

## Included Production Modules
1. **2D PNG Artwork & 27 Atlases (`atlases/`, `individual/`, `gui/`)**:
   - 256 crop-ready manifest entries across Atlases `01`–`22` (including `04` flipbooks, `05b` runtime ribbons, `20` charge release/cancel accents, `21` construct damage cracks & source highlights, and `22` QoL utility cues).
   - Multi-resolution convenience exports in `individual/runtime16/`, `individual/runtime32/`, and `individual/runtime64/`.
2. **3D Procedural VFX Meshes & Blockbench Models (`meshes/vfx/`, `models/bbmodel/`)**:
   - 9 parametric 3D VFX meshes in both `.obj`/`.mtl` and Blockbench 4.10 `.bbmodel` formats (`vfx_ring`, `vfx_arc`, `vfx_cone`, `vfx_sphere_shell`, `vfx_dome`, `vfx_tube`, `vfx_funnel`, `vfx_wave_sheet`, `vfx_octopus_tentacle`).
   - Weapon & container Blockbench models (`staff_candidate_2.bbmodel` with `staff_tip`/`staff_base` locators, `water_skin_container.bbmodel`, `lava_crucible_container.bbmodel`, `earth_boulder_construct.bbmodel`).
3. **PAL Animations & Rig Attachment Profiles (`animations/pal/`, `animations/attachment_profiles.json`)**:
   - 14 Player Animation Library (`.animation.json`) keyframe animations matched to `CONTENT_SPEC.md` windup/active/recovery tick timings and non-occluding first-person offsets.
4. **Synthesized Elemental & UI Audio (`sounds/source_wav/*.wav`, `assets/avatar_elements/sounds/**/*.ogg`, `sounds.json`)**:
   - 17 mono 44.1kHz 16-bit WAV source files and Vorbis OGG runtime files with spatial attenuation and localization subtitles.
5. **Fabric 1.21.1 Resourcepack Namespace & Java Integration (`assets/avatar_elements/`, `fabric_src/`)**:
   - Ready-to-load `pack.mcmeta`, `particles/*.json`, `sounds.json`, `models/item/*.json`, `lang/en_us.json`, `lang/id_id.json`, and Java 1.21.1 client integration classes (`AvatarParticles.java`, `AvatarSounds.java`, `ProceduralVfxMeshes.java`, `VfxLifecycleManager.java`).
