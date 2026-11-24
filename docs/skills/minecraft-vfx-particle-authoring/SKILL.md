---
name: minecraft-vfx-particle-authoring
description: Comprehensive production workflow for authoring AAA Minecraft VFX, anime cel-shaded textures, and high-performance particle systems inspired by ModMonster, Endesman, and KilaBash. Covers Blockbench Effect Animator keyframing, Blender ribbon and mesh VFX generation, Photon node curve logic, and Fabric 1.21.1 Java particle renderers.
---

# Minecraft VFX, Particle & Texture Authoring Skill

A unified, production-grade guide and reference manual for crafting AAA-quality visual effects (VFX), anime cel-shaded textures, dynamic particle systems, and combat animation fx for Minecraft Java Edition (Fabric 1.21.1+).

This skill synthesizes the core methodologies of three master Minecraft visual directors and modders:
1. **ModMonster (`@ModMonster`)**: Precision timeline keyframing via Blockbench Effect Animator, kinematic bone locators, and hit-frame-synchronized combat particles.
2. **Endesman / E-Magination (`@Endesman-Emagination`)**: AAA cinematic boss combat, multi-track audio-visual synchronization, multi-phase telegraphed attacks, and layered spatial visual storytelling.
3. **KilaBash (`@kilabashliang2473`)**: Node-driven particle graphs (Photon Editor), 3D mesh particles, UV-scrolling ribbon trails, dynamic sword soaring curves, and custom shader blend modes.

---

## 1. The Tri-Master Methodology Synthesis

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   AAA MINECRAFT VFX ARCHITECTURE                      │
  └──────────────────────────────────┬─────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
  [ MODMONSTER ]              [ ENDESMAN ]                [ KILABASH ]
  Keyframe & Locators         Combat Choreography         Mesh & Ribbon VFX
  ───────────────────         ───────────────────         ───────────────────
  • Bone Locators             • 4-Beat Telegraph Rhythm   • 3D Quad Ribbons
  • Effect Animator Tracks    • Multi-Layer Hierarchy     • UV Scroll Panning
  • Hitbox Sync (Frame 6)     • Screen & Camera Shake     • Noise Dissolve Masks
  • Entity $\to$ World Drift  • Emissive Sub-Bones        • Additive Shader Blends
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  FABRIC 1.21.1 JAVA ENGINE & SHADER INTEGRATION        │
        │  • SpriteBillboardParticle (Age, Velocity, Fullbright) │
        │  • WorldRenderEvents.AFTER_ENTITIES Ribbon Buffers     │
        │  • Sodium/Iris Emissive OptiFine/PBR Glow Maps         │
        └────────────────────────────────────────────────────────┘
```

### A. ModMonster: Kinematic Locators & Timeline Keyframing
- **The Problem:** Emitting particles from absolute entity coordinates `(x, y, z)` causes particles to spawn at the entity's feet or center of mass, ignoring weapon swings, hand gestures, and head turns.
- **The ModMonster Solution:**
  1. **Bone Locators:** Attach empty null bones or pivot markers to child elements in Blockbench (e.g. `locator_weapon_tip`, `locator_mouth`, `locator_left_fist`, `locator_root_ground`).
  2. **Effect Animator Tracks:** Keyframe VFX events directly inside the Blockbench Animation timeline alongside bone rotations and translations. An impact burst occurs at the exact frame of weapon contact (e.g., Frame 8 of an 18-frame swing).
  3. **World Transform Inheritance:** The emitter queries the bone locator's dynamic global matrix `M_world = M_entity * M_limb * M_locator` every tick, instantly transferring positional velocity to spawned particles without positional lag or teleporting drift.

### B. Endesman: Combat Choreography & Telegraph Hierarchy
- **The 4-Beat Combat Rhythm:**
  1. **Beat 1: Telegraph / Anticipation (0% - 35% time):** The boss draws back. Ground runes, concentric glowing rings, or suction chi particles appear around the ground zero zone. Players have a clear visual warning of the danger area.
  2. **Beat 2: Flashpoint / Apex (35% - 45% time):** Energy condenses tightly at the locator (e.g., weapon tip glows blinding white `0xF000F0`). Audio pitch peaks.
  3. **Beat 3: Climax / Release (45% - 60% time):** Explosive impact. High-velocity mesh slash ribbon, directional shockwave ring, ground fissure decals, and dynamic entity screen rumble.
  4. **Beat 4: Dissipation / Aftermath (60% - 100% time):** Core blast vanishes; lingering smoke, burning ground embers, heat distortion particles, and slow debris settling.
- **Multi-Layer Visual Stacking:** Never rely on a single particle. Always stack at least 3 visual layers:
  - *Layer 1 (Core Burst):* High-opacity, sharp, additive bright mesh or sprite.
  - *Layer 2 (Telegraph/Decal):* Flat ground-aligned quad or planar crack geometry.
  - *Layer 3 (Atmosphere):* Diffuse lingering particles (ash, sparks, steam, embers).

### C. KilaBash: 3D Mesh Particles & Ribbon Shader Logic
- **Beyond 2D Billboards:** 2D camera-facing billboards look flat when viewed from steep angles. KilaBash replaces them with **low-poly 3D extruded quads and ribbons** that occupy physical 3D space.
- **Curved Ribbon Strips:** A weapon swing generates a curved strip of quads forming a crescent arc:
  - UV coordinates are mapped flat from `0.0` to `1.0` along the length of the arc ($U$) and `0.0` to `1.0` across the width ($V$).
  - An animated alpha texture scrolls along the $U$ axis: `U_offset = (tick / lifetime)`.
  - Leading edge is razor-sharp (100% opacity); trailing edge fades softly to 0% with noise erosion.
- **Node-Driven Curves (Photon Paradigm):**
  - **Size-over-Lifetime:** Fast initial expansion ($0 \to 1.5\times$ in 3 ticks), followed by plateau and taper.
  - **Color-over-Lifetime:** Bright white highlight $\to$ saturated elemental color $\to$ deep dark burnt edge $\to$ complete alpha fade.

---

## 2. Technical Asset Production Pipelines

### Stage 1: Mesh Ribbon & Slash Arc Construction (Blender 4.x & Blockbench)

#### Creating a Curved Slash Mesh in Blender:
1. **Curve Guide:**
   - Add a Bézier Curve in the $X-Y$ plane (`Shift+A` $\to$ Curve $\to$ Bézier).
   - Shape it into a 120° to 180° crescent arc matching your attack swing radius ($1.5\text{m} - 2.5\text{m}$).
2. **Ribbon Strip Extrusion:**
   - In Edit Mode, extrude curve vertices or apply a Curve Bevel with a flat profile of width $0.3\text{m} - 0.6\text{m}$.
   - Alternatively, convert Curve to Mesh (`Alt+C` or Right Click $\to$ Convert to Mesh) and bridge edge loops.
   - Target polycount: **8 to 16 quad segments** (never exceed 32 quads; keep lightweight for real-time engine batching).
3. **UV Alignment (Critical for Ribbon Scrolling):**
   - In the UV Editor, ensure the strip is unwrapped into a straight rectangle spanning $[0, 0]$ to $[1, 1]$.
   - $U$ axis = Arc Length (From weapon hilt/start of swing to tip/end of swing).
   - $V$ axis = Arc Width (From inner arc radius to sharp outer blade edge).
4. **Vertex Colors / Alpha Masking:**
   - Paint vertex alpha: Inner edge = 0.8, Outer edge = 1.0, Tail vertices = 0.0, Head vertices = 1.0.
   - Export as `.obj` or `.json` blockbench model with centered pivot `(0, 0, 0)`.

```
UV Unwrapped Ribbon Quad Strip:
(0, 1) Outer Edge (V = 1.0) ───────────────────────────────── (1, 1) Outer Edge
  │   Segment 1  │  Segment 2  │  Segment 3  │  Segment 4   │
(0, 0) Inner Edge (V = 0.0) ───────────────────────────────── (1, 0) Inner Edge
Swing Start (U = 0.0)                                    Swing End (U = 1.0)
```

---

### Stage 2: Cel-Shaded & Emissive Texturing Rules

To capture the high-contrast anime style of Avatar and top-tier mods:

#### The 3-Tone Discrete Break Rule:
1. **Highlight / Core Glow (Tone 1):**
   - Color: Near-white or pale tinted core (`#FFFFFF`, `#FFF4D0`, `#E0FFFF`).
   - Area: Center 15% - 25% of the stroke.
   - Purpose: Represents extreme heat, raw chi, or intense energy.
2. **Body / Midtone (Tone 2):**
   - Color: Highly saturated elemental hue (`#E85D04` for Fire, `#00B4D8` for Water, `#90E0EF` for Air, `#588157` for Earth).
   - Area: 50% - 70% of the graphic.
   - Purpose: Provides the identifiable elemental identity.
3. **Outer Rim / Accent Shadow (Tone 3):**
   - Color: Deep contrasting tone or dark energy edge (`#370617` for Fire, `#03045E` for Water, `#344E41` for Earth).
   - Area: Outer 10% border.
   - Purpose: Gives crisp graphic silhouette readability against any Minecraft background (sky, cave, leaves).

#### Texture Atlas Specs:
- **Particle Atlas Grid:** $256 \times 256\text{ px}$ or $512 \times 512\text{ px}$ sprite sheets.
- **Individual Frame Resolution:** $32 \times 32\text{ px}$ or $64 \times 64\text{ px}$ per animation frame.
- **Format:** 32-bit PNG with clean 8-bit alpha channels (zero halo artifacts; dilate RGB colors under 0% alpha).
- **Emissive Layering:**
  - Create companion `_glow.png` or `_e.png` textures for OptiFine/Sodium/Iris shader packs.
  - White pixels in `_glow.png` render with full 100% emissive intensity regardless of ambient Minecraft light level.

---

### Stage 3: Emitter Architecture & Blockbench Effect Keyframing

#### Setting up Locators in Blockbench:
1. In the **Edit** tab of your entity/weapon model, create empty group folders named with the `locator_` prefix:
   - `locator_hand_r` (inside Right Arm bone)
   - `locator_sword_tip` (at the tip of the weapon mesh)
   - `locator_ground_zero` (at feet level, oriented with $Y = 0$)
   - `locator_mouth` (for breath/roar attacks)
2. Ensure the locator's pivot point is placed exactly at the desired particle emergence point.
3. In the **Animate** tab:
   - Select the animation (e.g. `attack_sweep`).
   - Open the **Effects** track (click the small star/sparkle icon at the top of the timeline).
   - On the exact frame of the swing apex (e.g., Frame 6, 0.3s):
     - Add a **Particle Keyframe**: `avatar:fire_slash_crescent` at `locator_sword_tip`.
     - Add a **Sound Keyframe**: `avatar:element.fire.slash` with volume 1.0, pitch 1.1.
     - Add a **Screen Shake Cue** (if using client event triggers).

---

### Stage 4: Fabric 1.21.1 Java Client Rendering Engine

#### 1. High-Performance Fullbright Particle (`SpriteBillboardParticle`):
```java
package net.avatar.client.particle;

import net.fabricmc.api.EnvType;
import net.fabricmc.api.Environment;
import net.minecraft.client.particle.*;
import net.minecraft.client.world.ClientWorld;

@Environment(EnvType.CLIENT)
public class ElementalAnimeParticle extends SpriteBillboardParticle {
    private final SpriteProvider spriteProvider;
    private final boolean isEmissive;

    public ElementalAnimeParticle(ClientWorld world, double x, double y, double z,
                                  double vx, double vy, double vz,
                                  SpriteProvider spriteProvider, boolean isEmissive) {
        super(world, x, y, z, vx, vy, vz);
        this.spriteProvider = spriteProvider;
        this.isEmissive = isEmissive;
        this.maxAge = 12 + this.random.nextInt(6);
        this.gravityStrength = 0.02F;
        this.scale = 0.45F + (this.random.nextFloat() * 0.2F);
        
        // Initial Velocity with damping
        this.velocityX = vx;
        this.velocityY = vy;
        this.velocityZ = vz;
        
        // CRITICAL: Initialize first frame
        this.setSpriteForAge(this.spriteProvider);
    }

    @Override
    public ParticleTextureSheet getType() {
        // Use PARTICLE_SHEET_TRANSLUCENT for alpha blending or PARTICLE_SHEET_OPAQUE
        return ParticleTextureSheet.PARTICLE_SHEET_TRANSLUCENT;
    }

    @Override
    public void tick() {
        this.prevPosX = this.x;
        this.prevPosY = this.y;
        this.prevPosZ = this.z;

        if (this.age++ >= this.maxAge) {
            this.markDead();
            return;
        }

        // Advance animation frame based on particle age
        this.setSpriteForAge(this.spriteProvider);

        // Alpha decay: sharp until 70% age, then rapid fade out
        float progress = (float) this.age / (float) this.maxAge;
        if (progress > 0.7F) {
            this.alpha = 1.0F - ((progress - 0.7F) / 0.3F);
        } else {
            this.alpha = 1.0F;
        }

        // Apply friction and motion
        this.move(this.velocityX, this.velocityY, this.velocityZ);
        this.velocityX *= 0.92;
        this.velocityY -= this.gravityStrength;
        this.velocityZ *= 0.92;
    }

    @Override
    public int getBrightness(float tint) {
        // If emissive, return maximum sky and block light (0xF000F0 = 15 block, 15 sky)
        return this.isEmissive ? 0xF000F0 : super.getBrightness(tint);
    }
}
```

#### 2. Quad Mesh Ribbon Rendering via `WorldRenderEvents.AFTER_ENTITIES`:
For rendering curved 3D ribbons and ground shockwave rings in Minecraft 1.21.1:

```java
WorldRenderEvents.AFTER_ENTITIES.register(context -> {
    Camera camera = context.camera();
    Vec3d camPos = camera.getPos();
    MatrixStack matrices = context.matrixStack();
    
    // Iterate active dynamic VFX meshes
    VFXManager.getActiveRibbons().forEach(ribbon -> {
        matrices.push();
        matrices.translate(ribbon.getX() - camPos.x, ribbon.getY() - camPos.y, ribbon.getZ() - camPos.z);
        matrices.multiply(RotationAxis.POSITIVE_Y.rotationDegrees(ribbon.getYaw()));
        matrices.multiply(RotationAxis.POSITIVE_X.rotationDegrees(ribbon.getPitch()));

        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.depthMask(false); // Prevents particle self-clipping z-sorting artifacts
        RenderSystem.setShader(GameRenderer::getPositionTexColorProgram);
        RenderSystem.setShaderTexture(0, ribbon.getTextureId());

        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder buffer = tessellator.begin(VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_TEXTURE_COLOR);

        // Build ribbon quad strips from precomputed curve points
        for (int i = 0; i < ribbon.getSegments().size() - 1; i++) {
            RibbonSegment curr = ribbon.getSegments().get(i);
            RibbonSegment next = ribbon.getSegments().get(i + 1);

            float u0 = curr.u;
            float u1 = next.u;
            int r = ribbon.getRed(), g = ribbon.getGreen(), b = ribbon.getBlue(), a = (int)(curr.alpha * 255);

            buffer.vertex(matrices.peek().getPositionMatrix(), curr.x0, curr.y0, curr.z0).texture(u0, 0f).color(r, g, b, a);
            buffer.vertex(matrices.peek().getPositionMatrix(), curr.x1, curr.y1, curr.z1).texture(u0, 1f).color(r, g, b, a);
            buffer.vertex(matrices.peek().getPositionMatrix(), next.x1, next.y1, next.z1).texture(u1, 1f).color(r, g, b, a);
            buffer.vertex(matrices.peek().getPositionMatrix(), next.x0, next.y0, next.z0).texture(u1, 0f).color(r, g, b, a);
        }

        BufferRenderer.drawWithGlobalProgram(buffer.end());
        RenderSystem.depthMask(true);
        RenderSystem.disableBlend();
        matrices.pop();
    });
});
```

---

## 3. Production Recipes (Step-by-Step)

### Recipe 1: Wuxia Crescent Sword Slash (KilaBash Style)
- **Use Case:** High-speed sword swings, Airblade projectile, or Fire Katana sweeps.
- **Parameters:**
  - Geometry: 12-quad curved arc strip, radius 1.8m, arc 140°.
  - Lifetime: 6 ticks (0.3 seconds) — fast, snappy, aggressive.
  - UV Scrolling:
    - Tick 0: Arc invisible, UV range $[-0.2, 0.0]$.
    - Tick 2: Arc expands rapidly, UV range $[0.0, 0.7]$.
    - Tick 4: Arc completes curve, UV range $[0.4, 1.0]$.
    - Tick 6: Arc fully dissolved by noise mask, opacity $0.0$.
  - Accompanying Billboards: 8 directional sparks (`avatar:spark_directional`) ejected tangentially along the arc's velocity vector.

### Recipe 2: Boss Telegraphed Ground Fissure (Endesman Style)
- **Use Case:** Roaming Sub-boss ground slam or Fire Lord Ozai meteor landing.
- **Timeline Breakdown:**
  - **Phase 1: Telegraph (Ticks 0 - 20 / 1.0s):**
    - Spawn a flat ground decal quad ($3.0\text{m} \times 3.0\text{m}$) at ground level ($Y + 0.015$ to avoid z-fighting).
    - Decal pulses with expanding warning circles (`avatar:rune_warning_circle`) scaling from $0.5\text{m} \to 3.0\text{m}$.
    - Suction particles drawn toward the strike center point at $-0.1\text{m/tick}$ velocity.
  - **Phase 2: Strike & Eruption (Tick 20 / 1.0s):**
    - Screen shake triggered for players within 16 blocks.
    - Ground cracks texture (`avatar:fissure_lava_cracks`) stamped onto ground decal.
    - Vertical flame/earth pillar launched upward: 16 ascending flame mesh ribbons + 12 rocky debris particles ejected with parabolic gravity.
  - **Phase 3: Residual Heat (Ticks 21 - 80 / 3.0s):**
    - Ground crack decal slowly fades from orange glow $\to$ charred black stone $\to$ transparent.
    - Ambient vertical smoke plumes float up lazily ($+0.03\text{m/tick}$).

### Recipe 3: Multi-Hit Melee Combo with Locator Hitsparks (ModMonster Style)
- **Use Case:** Monk Chi Fist 3-hit combo or Dual Dagger flurry.
- **Implementation:**
  - Weapon model possesses locator at blade edge: `locator_edge`.
  - On entity hit detection (server confirms attack frame):
    - Client queries exact world coordinates of `locator_edge`.
    - Spawns 1 cross-shaped hit spark (`avatar:chi_hitspark_cross`, scale 0.8, lifetime 4 ticks).
    - Spawns 1 ring shockwave (`avatar:shockwave_radial`, expanding from scale $0.2 \to 1.2$ in 5 ticks).
    - Spawns 6 micro directional flecks scattering 45° away from the attack normal.

---

## 4. Performance & Optimization Guardrails

To maintain stable 60+ FPS even during chaotic multiplayer boss fights:

| Budget Item | Target Limit | Hard Ceiling | Optimization Technique |
|---|---|---|---|
| Active Particles (Client) | 250 | 600 max | Automatic distance-based spawn throttling ($>32\text{m}$ = 50% count). |
| Mesh Ribbon Triangles | 24 tris / ribbon | 48 tris max | Keep ribbons low-poly; let texture shaders do the detail work. |
| Particle Texture Sheets | $256 \times 256$ | $512 \times 512$ | Batch all particle frames into unified element atlases. |
| Object Allocations | 0 alloc / frame | 0 in render loop | Pre-allocate and reuse `Vector3f`, `Matrix4f`, and segment arrays. |
| View Frustum Culling | Enabled | Mandatory | Skip tick/draw calls if emitter bounding box is outside camera frustum. |
| Depth Mask Policy | `depthMask(false)` | Mandatory | Always disable depth writes for translucent blending to eliminate quad clipping. |

---

## 5. Verification Checklist

Before releasing any VFX or particle asset into the production pack:
- [ ] **Frame Rate Stability:** Tested in a cluster of 5 simultaneous attacks without FPS drops below 60.
- [ ] **Z-Fighting Check:** Ground decals have $+0.015$ Y-offset above block surfaces.
- [ ] **Perspective Readability:** VFX looks visually appealing from first-person, third-person, and spectator aerial views.
- [ ] **Shader Compatibility:** Tested on Vanilla graphics, Sodium, and Iris shader packs (no black rectangular backgrounds).
- [ ] **Particle Age Cleanup:** Every particle strictly executes `this.markDead()` upon reaching `maxAge`. No lingering zombie particles.
- [ ] **Lighting Integration:** Emissive particles correctly return `0xF000F0` in `getBrightness()`.
