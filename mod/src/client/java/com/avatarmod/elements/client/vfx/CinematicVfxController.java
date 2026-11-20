package com.avatarmod.elements.client.vfx;

import com.avatarmod.elements.mixin.DisplayEntityAccessor;
import com.avatarmod.elements.mixin.ItemDisplayEntityAccessor;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.model.json.ModelTransformationMode;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.decoration.Brightness;
import net.minecraft.entity.decoration.DisplayEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.math.AffineTransformation;
import net.minecraft.util.math.Vec3d;
import org.joml.Vector3f;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Client-driven Display Entity Controller for Cinematic 3D VFX.
 *
 * Architecture & Invariants:
 * - Visuals are spawned strictly on the client (client.world.addEntity()), completely decoupled
 *   from chunk serialization NBT. Zero world-save persistence.
 * - Memory-only registry mapping (UUID casterUuid, int castSerial, String skillId) -> ActiveVfx.
 * - Lifecycle bound to SkillTimeline: spawns on ACTIVE/HOLD, strictly discards on RECOVERY/IDLE.
 * - Monotonic castSerial tracking drops stale/out-of-order packets and automatically transitions.
 * - Full unshaded brightness (sky: 15, block: 15) for compatibility with Sodium/Iris shaders.
 */
public final class CinematicVfxController {

    public record VfxKey(UUID casterUuid, int castSerial, String skillId) {}

    public static final class ActiveVfx {
        private final VfxKey key;
        private final DisplayEntity.ItemDisplayEntity entity;
        private final VfxType type;
        private int ageTicks;
        private final int maxAgeTicks;

        public ActiveVfx(VfxKey key, DisplayEntity.ItemDisplayEntity entity, VfxType type, int ageTicks, int maxAgeTicks) {
            this.key = key;
            this.entity = entity;
            this.type = type;
            this.ageTicks = ageTicks;
            this.maxAgeTicks = maxAgeTicks;
        }

        public VfxKey key() {
            return key;
        }

        public DisplayEntity.ItemDisplayEntity entity() {
            return entity;
        }

        public VfxType type() {
            return type;
        }

        public int ageTicks() {
            return ageTicks;
        }

        public int maxAgeTicks() {
            return maxAgeTicks;
        }

        public void incrementAge() {
            this.ageTicks++;
        }
    }

    private static final Map<VfxKey, ActiveVfx> ACTIVE_ENTITIES = new ConcurrentHashMap<>();
    private static final Map<UUID, Integer> CASTER_ACTIVE_SERIALS = new ConcurrentHashMap<>();
    private static final Map<VfxKey, Vec3d> PILLAR_GROUND_POSITIONS = new ConcurrentHashMap<>();

    // Server-authoritative positions received before or alongside the ACTIVE phase sync
    private static final Map<VfxKey, Vec3d> SERVER_POSITIONS = new ConcurrentHashMap<>();
    private static final Map<VfxKey, List<Vec3d>> PENDING_WALL_POSITIONS = new ConcurrentHashMap<>();
    private static final Map<VfxKey, String> VFX_PHASES = new ConcurrentHashMap<>();
    private static final List<FlyingMegalithVfx> FLYING_MEGALITHS_CLIENT = new CopyOnWriteArrayList<>();

    public static final class FlyingMegalithVfx {
        private final DisplayEntity.ItemDisplayEntity entity;
        private Vec3d pos;
        private final Vec3d velocity;
        private int ageTicks;
        private final int maxAgeTicks;
        private float pitch;
        private float yaw;

        public FlyingMegalithVfx(DisplayEntity.ItemDisplayEntity entity, Vec3d pos, Vec3d velocity, int maxAgeTicks) {
            this.entity = entity;
            this.pos = pos;
            this.velocity = velocity;
            this.maxAgeTicks = maxAgeTicks;
            this.ageTicks = 0;
            this.pitch = 0.0f;
            this.yaw = 0.0f;
        }

        public boolean tick(MinecraftClient client) {
            ageTicks++;
            if (entity == null || entity.isRemoved() || ageTicks >= maxAgeTicks) {
                detonate(client);
                return false;
            }

            pos = pos.add(velocity);
            entity.setPosition(pos.x, pos.y, pos.z);

            pitch = (pitch + 16.0f) % 360.0f;
            yaw = (yaw + 10.0f) % 360.0f;
            DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
            dispAcc.invokeSetTransformation(new AffineTransformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new org.joml.Quaternionf().rotateX((float) Math.toRadians(pitch)).rotateY((float) Math.toRadians(yaw)),
                    new Vector3f(1.15f, 1.15f, 1.15f),
                    new org.joml.Quaternionf()
            ));

            if (client.world != null) {
                client.world.addParticle(com.avatarmod.elements.particle.AvatarParticles.STONE_CHIP, pos.x, pos.y, pos.z, 0.0, 0.06, 0.0);
                client.world.addParticle(com.avatarmod.elements.particle.AvatarParticles.DUST, pos.x, pos.y + 0.1, pos.z, 0.0, 0.03, 0.0);
                client.world.addParticle(net.minecraft.particle.ParticleTypes.POOF, pos.x, pos.y, pos.z, 0.0, 0.01, 0.0);

                // Collision with solid blocks
                net.minecraft.util.math.BlockPos bp = net.minecraft.util.math.BlockPos.ofFloored(pos);
                if (!client.world.getBlockState(bp).getCollisionShape(client.world, bp).isEmpty()) {
                    detonate(client);
                    return false;
                }
            }
            return true;
        }

        private void detonate(MinecraftClient client) {
            if (entity != null) entity.discard();
            if (client.world != null) {
                spawnTransientVfx(VfxType.MARTIAL_SHOCKWAVE, pos, 0.0f, 0.0f);
                spawnTransientVfx(VfxType.HITSTOP_FLASH, pos.add(0, 0.8, 0), 0.0f, 0.0f);
                if (client.player != null && client.player.squaredDistanceTo(pos) < 256.0) {
                    com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerShake(0.80f, 12);
                }
            }
        }
    }

    private CinematicVfxController() {}

    /**
     * Receives the server-authoritative position for a positional skill (e.g. Earth Pillar).
     * Called from ClientNetworkHandler on the main thread, before or alongside the phase sync.
     */
    public static void onSkillPosition(UUID casterUuid, int castSerial, String skillId,
                                       double x, double y, double z) {
        if (casterUuid == null) return;
        VfxKey key = new VfxKey(casterUuid, castSerial, skillId);
        Vec3d position = new Vec3d(x, y, z);
        if ("avatar:earth_pillar".equals(skillId)) {
            ActiveVfx existing = ACTIVE_ENTITIES.get(key);
            if (existing != null && existing.type() == VfxType.EARTH_PILLAR) {
                if (!PILLAR_GROUND_POSITIONS.containsKey(key)) {
                    PILLAR_GROUND_POSITIONS.put(key, position);
                    SERVER_POSITIONS.remove(key);
                } else {
                    int subIdx = PILLAR_GROUND_POSITIONS.size() + 1;
                    VfxKey subKey = new VfxKey(casterUuid, castSerial, skillId + "#" + subIdx);
                    PILLAR_GROUND_POSITIONS.put(subKey, position);
                    spawnPillarEntityAt(subKey, position);
                }
                return;
            }

            // Entity not spawned yet: accumulate positions for this castSerial
            List<Vec3d> pending = PENDING_WALL_POSITIONS.computeIfAbsent(key, k -> new CopyOnWriteArrayList<>());
            pending.add(position);
            if (!SERVER_POSITIONS.containsKey(key)) {
                SERVER_POSITIONS.put(key, position);
            }
            return;
        }

        ActiveVfx existing = ACTIVE_ENTITIES.get(key);
        if (existing != null) {
            SERVER_POSITIONS.remove(key);
        } else {
            SERVER_POSITIONS.put(key, position);
        }
    }

    private static void spawnPillarEntityAt(VfxKey key, Vec3d groundPos) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client == null || client.world == null) return;
        VfxType type = VfxType.EARTH_PILLAR;
        DisplayEntity.ItemDisplayEntity entity = new DisplayEntity.ItemDisplayEntity(EntityType.ITEM_DISPLAY, client.world);
        entity.setPosition(groundPos.x, groundPos.y - 2.75, groundPos.z);

        DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
        dispAcc.invokeSetInterpolationDuration(type.durationTicks());
        dispAcc.invokeSetStartInterpolation(0);
        dispAcc.invokeSetBrightness(Brightness.FULL);
        dispAcc.invokeSetBillboardMode(DisplayEntity.BillboardMode.FIXED);
        dispAcc.invokeSetViewRange(64.0f);

        ItemDisplayEntityAccessor itemAcc = (ItemDisplayEntityAccessor) entity;
        itemAcc.invokeSetItemStack(type.createItemStack());
        itemAcc.invokeSetTransformationMode(ModelTransformationMode.FIXED);

        dispAcc.invokeSetTransformation(VfxTransformUtil.createPillarTransform(type.baseScale().x(), type.baseScale().x() * 1.25f));
        client.world.addEntity(entity);
        ACTIVE_ENTITIES.put(key, new ActiveVfx(key, entity, type, 0, type.durationTicks()));
    }

    /**
     * Spawns a transient, non-persistent client-side VFX entity (shockwave, impact flash, trail)
     * that automatically plays its lifetime animation and cleans up.
     */
    public static void spawnTransientVfx(VfxType type, Vec3d pos, float yaw, float pitch) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client == null || client.world == null || type == null) return;
        DisplayEntity.ItemDisplayEntity entity = new DisplayEntity.ItemDisplayEntity(EntityType.ITEM_DISPLAY, client.world);
        entity.setPosition(pos.x, pos.y, pos.z);
        entity.setYaw(yaw);
        entity.setPitch(pitch);

        DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
        dispAcc.invokeSetInterpolationDuration(type.durationTicks());
        dispAcc.invokeSetStartInterpolation(0);
        dispAcc.invokeSetBrightness(Brightness.FULL);
        dispAcc.invokeSetBillboardMode(DisplayEntity.BillboardMode.FIXED);
        dispAcc.invokeSetViewRange(64.0f);

        ItemDisplayEntityAccessor itemAcc = (ItemDisplayEntityAccessor) entity;
        itemAcc.invokeSetItemStack(type.createItemStack());
        itemAcc.invokeSetTransformationMode(ModelTransformationMode.FIXED);

        dispAcc.invokeSetTransformation(VfxTransformUtil.createUniformScaleTransform(type.baseScale().x()));
        client.world.addEntity(entity);

        VfxKey key = new VfxKey(UUID.randomUUID(), (int) (System.nanoTime() & 0x7FFFFFFF), type.skillId());
        ACTIVE_ENTITIES.put(key, new ActiveVfx(key, entity, type, 0, type.durationTicks()));
    }

    /**
     * Handles S2CPhaseSync packet dispatch on the client main thread.
     */
    public static void onPhaseSync(UUID casterUuid, String skillId, String phase, int ticksIn, int castSerial) {
        if (casterUuid == null || castSerial < 0) {
            return;
        }

        Integer currentActive = CASTER_ACTIVE_SERIALS.get(casterUuid);
        if (currentActive != null && castSerial < currentActive) {
            // Drop stale packet from an older cast serial
            return;
        }

        VfxKey key = new VfxKey(casterUuid, castSerial, skillId);
        VFX_PHASES.put(key, phase);

        if ("ACTIVE".equals(phase) || "HOLD".equals(phase)) {
            // If caster started a new serial, clean up any previous entities for this caster
            if (currentActive == null || castSerial > currentActive) {
                cleanupCasterPrior(casterUuid, castSerial);
                CASTER_ACTIVE_SERIALS.put(casterUuid, castSerial);
            }

            if (!ACTIVE_ENTITIES.containsKey(key)) {
                spawnVfxEntity(key);
            }
        } else if ("RECOVERY".equals(phase) || "IDLE".equals(phase)) {
            // Earth pillar is a persistent interactive world object — do not discard on phase end
            if (!"avatar:earth_pillar".equals(key.skillId())) {
                ActiveVfx removed = ACTIVE_ENTITIES.remove(key);
                PILLAR_GROUND_POSITIONS.remove(key);
                SERVER_POSITIONS.remove(key);
                if (removed != null && removed.entity() != null) {
                    removed.entity().discard();
                }
            }

            if ("IDLE".equals(phase) && currentActive != null && castSerial == currentActive) {
                CASTER_ACTIVE_SERIALS.remove(casterUuid);
            }
        }
    }

    private static void spawnVfxEntity(VfxKey key) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client == null || client.world == null) {
            return;
        }

        VfxType type = VfxType.fromSkillId(key.skillId());
        if (type == null) {
            String sid = key.skillId() != null ? key.skillId().toLowerCase() : "";
            if (sid.contains("sweep")) {
                type = VfxType.CRESCENT_SLASH;
            } else if (sid.contains("guard")) {
                type = VfxType.AEGIS_DOME;
            } else if (sid.contains("vortex")) {
                type = VfxType.AIR_VORTEX_FUNNEL;
            } else if (sid.contains("avatar_state")) {
                type = VfxType.RUNE_DISC;
            } else if (sid.contains("boulder_launch") || sid.contains("megalith")) {
                type = VfxType.BOULDER_LAUNCH_MEGALITH;
            } else if (sid.contains("water_whip") || sid.contains("whip")) {
                type = VfxType.WATER_WHIP_STREAM;
            } else if (sid.contains("earth_boulder") || sid.contains("shards")) {
                type = VfxType.CAPTURED_EARTH_SHARDS;
            } else if (sid.contains("armor")) {
                type = VfxType.EARTH_ARMOR_OVERLAY;
            } else {
                // Do not spawn unsolicited display entities for skills without 3D cinematic VFX
                return;
            }
        }

        DisplayEntity.ItemDisplayEntity entity = new DisplayEntity.ItemDisplayEntity(EntityType.ITEM_DISPLAY, client.world);

        PlayerEntity caster = client.world.getPlayerByUuid(key.casterUuid());
        float yaw = 0.0f;
        float pitch = 0.0f;

        if (caster != null) {
            yaw = caster.getYaw();
            pitch = caster.getPitch();
            if (type == VfxType.EARTH_PILLAR) {
                Vec3d serverPos = SERVER_POSITIONS.remove(key);
                Vec3d groundPos = serverPos != null ? serverPos : findPillarGroundClient(caster, 8.0);
                PILLAR_GROUND_POSITIONS.put(key, groundPos);
                entity.setPosition(groundPos.x, groundPos.y - 2.75, groundPos.z);

                List<Vec3d> extras = PENDING_WALL_POSITIONS.remove(key);
                if (extras != null) {
                    for (Vec3d extraPos : extras) {
                        if (extraPos.squaredDistanceTo(groundPos) < 0.01) continue;
                        int subIdx = PILLAR_GROUND_POSITIONS.size() + 1;
                        VfxKey subKey = new VfxKey(key.casterUuid(), key.castSerial(), key.skillId() + "#" + subIdx);
                        PILLAR_GROUND_POSITIONS.put(subKey, extraPos);
                        spawnPillarEntityAt(subKey, extraPos);
                    }
                }
            } else if (type == VfxType.CRESCENT_SLASH) {
                Vec3d look = caster.getRotationVec(1.0f);
                entity.setPosition(caster.getX() + look.x * 0.8, caster.getEyeY() - 0.2 + look.y * 0.8, caster.getZ() + look.z * 0.8);
                entity.setYaw(yaw);
                entity.setPitch(pitch);
            } else if (type == VfxType.WATER_WHIP_STREAM) {
                Vec3d look = caster.getRotationVec(1.0f);
                entity.setPosition(caster.getX() + look.x * 0.5, caster.getEyeY() - 0.2 + look.y * 0.5, caster.getZ() + look.z * 0.5);
                entity.setYaw(yaw);
                entity.setPitch(pitch);
            } else if (type == VfxType.BOULDER_LAUNCH_MEGALITH) {
                Vec3d look = caster.getRotationVec(1.0f);
                entity.setPosition(caster.getX() + look.x * 1.5, caster.getEyeY() - 0.2 + look.y * 1.5, caster.getZ() + look.z * 1.5);
                entity.setYaw(yaw);
                entity.setPitch(pitch);
            } else if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
                entity.setPosition(caster.getX(), caster.getY() + 0.05, caster.getZ());
            } else if (type == VfxType.AIR_VORTEX_FUNNEL || type == VfxType.SWIRL_VORTEX || type == VfxType.SWIRLING_VORTEX) {
                entity.setPosition(caster.getX(), caster.getY() + 0.1, caster.getZ());
            } else if (type == VfxType.CAPTURED_EARTH_SHARDS) {
                entity.setPosition(caster.getX(), caster.getY() + 0.8, caster.getZ());
            } else if (type == VfxType.EARTH_ARMOR_OVERLAY) {
                entity.setPosition(caster.getX(), caster.getY() + 0.125, caster.getZ());
                entity.setYaw(yaw);
            } else if (type == VfxType.MARTIAL_SHOCKWAVE) {
                entity.setPosition(caster.getX(), caster.getY() + 0.05, caster.getZ());
            } else if (type == VfxType.HITSTOP_FLASH) {
                Vec3d look = caster.getRotationVec(1.0f);
                entity.setPosition(caster.getX() + look.x * 1.2, caster.getEyeY() - 0.2 + look.y * 1.2, caster.getZ() + look.z * 1.2);
            } else if (type == VfxType.DIVE_KICK_TRAIL) {
                entity.setPosition(caster.getX(), caster.getY() + 0.5, caster.getZ());
            } else {
                entity.setPosition(caster.getX(), caster.getY() + 0.5, caster.getZ());
            }
        }

        // Apply accessors
        DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
        dispAcc.invokeSetInterpolationDuration(type.durationTicks());
        dispAcc.invokeSetStartInterpolation(0);
        dispAcc.invokeSetBrightness(Brightness.FULL);
        dispAcc.invokeSetBillboardMode(DisplayEntity.BillboardMode.FIXED);
        dispAcc.invokeSetViewRange(64.0f);

        ItemDisplayEntityAccessor itemAcc = (ItemDisplayEntityAccessor) entity;
        itemAcc.invokeSetItemStack(type.createItemStack());
        itemAcc.invokeSetTransformationMode(ModelTransformationMode.FIXED);

        // Initial transform
        AffineTransformation initialTransform;
        if (type == VfxType.CRESCENT_SLASH) {
            initialTransform = VfxTransformUtil.createSlashTransform(yaw, pitch, type.baseScale(), 0.5f);
        } else if (type == VfxType.WATER_WHIP_STREAM) {
            initialTransform = VfxTransformUtil.createSlashTransform(yaw, pitch, type.baseScale(), 0.2f);
        } else if (type == VfxType.BOULDER_LAUNCH_MEGALITH) {
            initialTransform = VfxTransformUtil.createSlashTransform(yaw, pitch, type.baseScale(), 0.0f);
        } else if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
            initialTransform = VfxTransformUtil.createRuneDiscTransform(type.baseScale().x(), 0.0f);
        } else if (type == VfxType.AIR_VORTEX_FUNNEL || type == VfxType.SWIRL_VORTEX || type == VfxType.SWIRLING_VORTEX) {
            initialTransform = new AffineTransformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new org.joml.Quaternionf().rotateY((float) Math.toRadians(0.0f)),
                    type.baseScale(),
                    new org.joml.Quaternionf()
            );
        } else if (type == VfxType.CAPTURED_EARTH_SHARDS) {
            initialTransform = new AffineTransformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new org.joml.Quaternionf().rotateY((float) Math.toRadians(0.0f)),
                    type.baseScale(),
                    new org.joml.Quaternionf()
            );
        } else if (type == VfxType.EARTH_ARMOR_OVERLAY) {
            initialTransform = new AffineTransformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new org.joml.Quaternionf().rotateY((float) Math.toRadians(180.0f - yaw)),
                    type.baseScale(),
                    new org.joml.Quaternionf()
            );
        } else if (type == VfxType.EARTH_PILLAR) {
            initialTransform = VfxTransformUtil.createPillarTransform(type.baseScale().x(), type.baseScale().x() * 1.25f);
        } else {
            initialTransform = VfxTransformUtil.createUniformScaleTransform(type.baseScale().x());
        }
        dispAcc.invokeSetTransformation(initialTransform);

        // Spawn strictly client-side
        client.world.addEntity(entity);

        ACTIVE_ENTITIES.put(key, new ActiveVfx(key, entity, type, 0, type.durationTicks()));
    }

    /**
     * Ticks all active VFX display entities on client tick (END_CLIENT_TICK).
     * Updates sub-tick scale interpolation, quaternion rotation, and checks duration limits.
     */
    public static void tick(MinecraftClient client) {
        if (client == null || client.world == null) {
            clear();
            return;
        }

        FLYING_MEGALITHS_CLIENT.removeIf(m -> !m.tick(client));

        List<VfxKey> expired = new ArrayList<>();

        for (Map.Entry<VfxKey, ActiveVfx> entry : ACTIVE_ENTITIES.entrySet()) {
            VfxKey key = entry.getKey();
            ActiveVfx vfx = entry.getValue();
            DisplayEntity.ItemDisplayEntity entity = vfx.entity();

            if (entity == null || entity.isRemoved()) {
                expired.add(key);
                continue;
            }

            vfx.incrementAge();
            if (vfx.ageTicks() >= vfx.maxAgeTicks()) {
                entity.discard();
                expired.add(key);
                continue;
            }

            // Update entity position and transform
            VfxType type = vfx.type();
            PlayerEntity caster = client.world.getPlayerByUuid(key.casterUuid());

            if (type.followCaster() && caster != null) {
                if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
                    entity.setPosition(caster.getX(), caster.getY() + 0.05, caster.getZ());
                } else if (type == VfxType.AIR_VORTEX_FUNNEL || type == VfxType.SWIRL_VORTEX || type == VfxType.SWIRLING_VORTEX) {
                    entity.setPosition(caster.getX(), caster.getY() + 0.1, caster.getZ());
                } else if (type == VfxType.CAPTURED_EARTH_SHARDS) {
                    entity.setPosition(caster.getX(), caster.getY() + 0.8, caster.getZ());
                } else if (type == VfxType.EARTH_ARMOR_OVERLAY) {
                    entity.setPosition(caster.getX(), caster.getY() + 0.125, caster.getZ());
                    entity.setYaw(caster.getYaw());
                } else if (type == VfxType.WATER_WHIP_STREAM) {
                    Vec3d look = caster.getRotationVec(1.0f);
                    entity.setPosition(caster.getX() + look.x * 0.5, caster.getEyeY() - 0.2 + look.y * 0.5, caster.getZ() + look.z * 0.5);
                    entity.setYaw(caster.getYaw());
                    entity.setPitch(caster.getPitch());
                } else {
                    entity.setPosition(caster.getX(), caster.getY() + 0.5, caster.getZ());
                }
            }

            DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
            if (type == VfxType.EARTH_PILLAR) {
                Vec3d groundPos = PILLAR_GROUND_POSITIONS.get(key);
                if (groundPos != null) {
                    double yOffset = computePillarYOffset(vfx.ageTicks());
                    entity.setPosition(groundPos.x, groundPos.y + yOffset, groundPos.z);
                }
            } else if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
                float spinAngle = (vfx.ageTicks() * type.rotationSpeed()) % 360.0f;
                dispAcc.invokeSetTransformation(VfxTransformUtil.createRuneDiscTransform(type.baseScale().x(), spinAngle));
            } else if (type == VfxType.AIR_VORTEX_FUNNEL || type == VfxType.SWIRL_VORTEX || type == VfxType.SWIRLING_VORTEX) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                float spinAngle = (vfx.ageTicks() * type.rotationSpeed()) % 360.0f;
                dispAcc.invokeSetTransformation(new AffineTransformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new org.joml.Quaternionf().rotateY((float) Math.toRadians(spinAngle)),
                        scale,
                        new org.joml.Quaternionf()
                ));
            } else if (type == VfxType.CAPTURED_EARTH_SHARDS) {
                float orbitAngle = (vfx.ageTicks() * type.rotationSpeed()) % 360.0f;
                float floatBob = (float) Math.sin(vfx.ageTicks() * 0.2f) * 0.05f;
                dispAcc.invokeSetTransformation(new AffineTransformation(
                        new Vector3f(0.0f, floatBob, 0.0f),
                        new org.joml.Quaternionf().rotateY((float) Math.toRadians(orbitAngle)),
                        type.baseScale(),
                        new org.joml.Quaternionf()
                ));
            } else if (type == VfxType.EARTH_ARMOR_OVERLAY) {
                dispAcc.invokeSetTransformation(new AffineTransformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new org.joml.Quaternionf().rotateY((float) Math.toRadians(180.0f - entity.getYaw())),
                        type.baseScale(),
                        new org.joml.Quaternionf()
                ));
            } else if (type == VfxType.BOULDER_LAUNCH_MEGALITH) {
                String phase = VFX_PHASES.getOrDefault(key, "ACTIVE");

                if ("HOLD".equals(phase) && caster != null) {
                    // Hover and expand in front of the caster during charge
                    Vec3d look = caster.getRotationVec(1.0f);
                    Vec3d hoverPos = caster.getEyePos().add(look.multiply(1.8));
                    double jitter = Math.sin(vfx.ageTicks() * 0.9) * 0.03;
                    entity.setPosition(hoverPos.x, hoverPos.y - 0.2 + jitter, hoverPos.z);
                    entity.setYaw(caster.getYaw());
                    entity.setPitch(caster.getPitch());

                    // Progressive swelling scale: from 0.8 up to 2.8 (or 3.5 if holding hammer)
                    float holdProgress = Math.min(1.0f, (float) vfx.ageTicks() / 40.0f);
                    boolean hasHammer = caster.getMainHandStack().getItem() instanceof com.avatarmod.elements.item.EarthHammerItem;
                    float maxScale = hasHammer ? 3.5f : 2.8f;
                    float currentScale = 0.8f + (maxScale - 0.8f) * holdProgress;

                    Vector3f scaleVec = new Vector3f(currentScale, currentScale, currentScale);
                    dispAcc.invokeSetTransformation(VfxTransformUtil.createSlashTransform(entity.getYaw(), entity.getPitch(), scaleVec, vfx.ageTicks() * 0.15f));

                    if (client.world != null) {
                        client.world.addParticle(com.avatarmod.elements.particle.AvatarParticles.STONE_CHIP,
                                hoverPos.x + (Math.random() - 0.5) * currentScale * 0.6,
                                hoverPos.y + (Math.random() - 0.5) * currentScale * 0.6,
                                hoverPos.z + (Math.random() - 0.5) * currentScale * 0.6,
                                0.0, 0.02, 0.0);
                    }
                } else {
                    // ACTIVE phase: flying projectile
                    Vec3d look = Vec3d.fromPolar(entity.getPitch(), entity.getYaw());
                    entity.setPosition(entity.getX() + look.x * 1.35, entity.getY() + look.y * 1.35, entity.getZ() + look.z * 1.35);
                    if (client.world != null) {
                        client.world.addParticle(com.avatarmod.elements.particle.AvatarParticles.STONE_CHIP, entity.getX(), entity.getY(), entity.getZ(), 0.0, 0.04, 0.0);
                        client.world.addParticle(com.avatarmod.elements.particle.AvatarParticles.DUST, entity.getX(), entity.getY() + 0.1, entity.getZ(), 0.0, 0.02, 0.0);
                        net.minecraft.util.math.BlockPos bp = net.minecraft.util.math.BlockPos.ofFloored(entity.getPos());
                        if (!client.world.getBlockState(bp).getCollisionShape(client.world, bp).isEmpty()) {
                            entity.discard();
                            expired.add(key);
                            spawnTransientVfx(VfxType.MARTIAL_SHOCKWAVE, entity.getPos(), 0.0f, 0.0f);
                            spawnTransientVfx(VfxType.HITSTOP_FLASH, entity.getPos().add(0, 0.8, 0), 0.0f, 0.0f);
                            com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerShake(0.65f, 8);
                        }
                    }
                    float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                    Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                    dispAcc.invokeSetTransformation(VfxTransformUtil.createSlashTransform(entity.getYaw(), entity.getPitch(), scale, vfx.ageTicks() * 0.4f));
                }
            } else if (type == VfxType.WATER_WHIP_STREAM) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                float stretchZ = progress < 0.4f ? progress / 0.4f : 1.0f - (progress - 0.4f) / 0.6f;
                Vector3f currentScale = new Vector3f(type.baseScale().x(), type.baseScale().y(), type.baseScale().z() * Math.max(0.2f, stretchZ));
                dispAcc.invokeSetTransformation(VfxTransformUtil.createSlashTransform(entity.getYaw(), entity.getPitch(), currentScale, 0.2f + progress * 0.8f));
            } else if (type == VfxType.AEGIS_DOME) {
                float progress = Math.min(1.0f, vfx.ageTicks() / 3.0f);
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(VfxTransformUtil.createUniformScaleTransform(scale.x()));
            } else if (type == VfxType.CRESCENT_SLASH) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(VfxTransformUtil.createSlashTransform(entity.getYaw(), entity.getPitch(), scale, 0.5f + vfx.ageTicks() * 0.2f));
            } else if (type == VfxType.MARTIAL_SHOCKWAVE) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(VfxTransformUtil.createUniformScaleTransform(scale.x()));
            } else if (type == VfxType.HITSTOP_FLASH) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                float spin = (vfx.ageTicks() * 30.0f) % 360.0f;
                dispAcc.invokeSetTransformation(new AffineTransformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new org.joml.Quaternionf().rotateZ((float) Math.toRadians(spin)),
                        scale,
                        new org.joml.Quaternionf()
                ));
            } else if (type == VfxType.DIVE_KICK_TRAIL) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(new AffineTransformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new org.joml.Quaternionf().rotateY((float) Math.toRadians(entity.getYaw())),
                        scale,
                        new org.joml.Quaternionf()
                ));
            }
        }

        for (VfxKey k : expired) {
            ACTIVE_ENTITIES.remove(k);
            PILLAR_GROUND_POSITIONS.remove(k);
            SERVER_POSITIONS.remove(k);
        }
    }

    /**
     * Cancels an active skill cast immediately, cleanly discarding entities.
     */
    public static void cancelSkill(UUID casterUuid, int castSerial) {
        if (casterUuid == null) return;
        List<VfxKey> toRemove = new ArrayList<>();
        for (VfxKey k : ACTIVE_ENTITIES.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() == castSerial) {
                toRemove.add(k);
            }
        }
        for (VfxKey k : toRemove) {
            ActiveVfx removed = ACTIVE_ENTITIES.remove(k);
            PILLAR_GROUND_POSITIONS.remove(k);
            SERVER_POSITIONS.remove(k);
            PENDING_WALL_POSITIONS.remove(k);
            if (removed != null && removed.entity() != null) {
                removed.entity().discard();
            }
        }
        for (VfxKey k : SERVER_POSITIONS.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() == castSerial) {
                SERVER_POSITIONS.remove(k);
            }
        }
        for (VfxKey k : PENDING_WALL_POSITIONS.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() == castSerial) {
                PENDING_WALL_POSITIONS.remove(k);
            }
        }
        Integer current = CASTER_ACTIVE_SERIALS.get(casterUuid);
        if (current != null && current == castSerial) {
            CASTER_ACTIVE_SERIALS.remove(casterUuid);
        }
    }

    private static void cleanupCasterPrior(UUID casterUuid, int newSerial) {
        List<VfxKey> toRemove = new ArrayList<>();
        for (VfxKey k : ACTIVE_ENTITIES.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() < newSerial) {
                ActiveVfx vfx = ACTIVE_ENTITIES.get(k);
                // Do NOT discard EARTH_PILLAR when starting another skill! Earth pillars persist until kicked or crumbled!
                if (vfx != null && vfx.type() == VfxType.EARTH_PILLAR) {
                    continue;
                }
                toRemove.add(k);
            }
        }
        for (VfxKey k : toRemove) {
            ActiveVfx removed = ACTIVE_ENTITIES.remove(k);
            PILLAR_GROUND_POSITIONS.remove(k);
            SERVER_POSITIONS.remove(k);
            PENDING_WALL_POSITIONS.remove(k);
            if (removed != null && removed.entity() != null) {
                removed.entity().discard();
            }
        }
        for (VfxKey k : SERVER_POSITIONS.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() < newSerial) {
                SERVER_POSITIONS.remove(k);
            }
        }
        for (VfxKey k : PENDING_WALL_POSITIONS.keySet()) {
            if (k.casterUuid().equals(casterUuid) && k.castSerial() < newSerial) {
                PENDING_WALL_POSITIONS.remove(k);
            }
        }
    }

    /**
     * Purges all active display entities and clears registries.
     * Hooked to DISCONNECT, JOIN, and AFTER_CLIENT_WORLD_CHANGE.
     */
    public static void clear() {
        for (ActiveVfx vfx : ACTIVE_ENTITIES.values()) {
            if (vfx.entity() != null) {
                vfx.entity().discard();
            }
        }
        ACTIVE_ENTITIES.clear();
        CASTER_ACTIVE_SERIALS.clear();
        PILLAR_GROUND_POSITIONS.clear();
        SERVER_POSITIONS.clear();
        PENDING_WALL_POSITIONS.clear();
        for (FlyingMegalithVfx m : FLYING_MEGALITHS_CLIENT) {
            if (m.entity != null) m.entity.discard();
        }
        FLYING_MEGALITHS_CLIENT.clear();
    }

    public static int getActiveCount() {
        return ACTIVE_ENTITIES.size();
    }

    public static boolean hasActiveVfx(UUID casterUuid, int castSerial, String skillId) {
        return ACTIVE_ENTITIES.containsKey(new VfxKey(casterUuid, castSerial, skillId));
    }

    public static Map<VfxKey, ActiveVfx> getActiveEntities() {
        return Collections.unmodifiableMap(ACTIVE_ENTITIES);
    }

    /**
     * Computes the Y offset for the earth pillar animation.
     * Ticks 0-2: burst upward from -2.75 to +0.15 (overshoot)
     * Ticks 2-4: settle from +0.15 to 0.0
     * Ticks 4-132: hold stance at 0.0 (active manipulatable pillar!)
     * Ticks 132-140: sink back to -2.75 if not interacted with.
     */
    private static double computePillarYOffset(int ageTicks) {
        if (ageTicks <= 2) {
            double t = ageTicks / 2.0;
            return -2.75 + t * (2.75 + 0.15);  // lerp from -2.75 to +0.15
        } else if (ageTicks <= 4) {
            double t = (ageTicks - 2) / 2.0;
            return 0.15 - t * 0.15;  // settle from +0.15 to 0.0
        } else if (ageTicks <= 132) {
            return 0.0;  // held interactive stance
        } else if (ageTicks <= 140) {
            double t = (ageTicks - 132) / 8.0;
            return -t * 2.75;  // sink back down
        }
        return -2.75;
    }

    /**
     * Handles S2CPillarAction broadcast on client:
     * actionType: 0 = KICK, 1 = STRIKE, 2 = CRUMBLE
     */
    public static void onPillarAction(UUID casterUuid, int actionType,
                                      double x, double y, double z,
                                      double dirX, double dirY, double dirZ) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client == null || client.world == null) return;

        // Find active pillar display entities near x,y,z or belonging to caster
        List<VfxKey> toDiscard = new ArrayList<>();
        for (Map.Entry<VfxKey, ActiveVfx> entry : ACTIVE_ENTITIES.entrySet()) {
            VfxKey k = entry.getKey();
            if (entry.getValue().type() == VfxType.EARTH_PILLAR) {
                if (k.casterUuid().equals(casterUuid)
                        || (entry.getValue().entity() != null && entry.getValue().entity().squaredDistanceTo(x, y, z) < 9.0)) {
                    toDiscard.add(k);
                }
            }
        }

        if (actionType == 0) {
            // KICK (Power Kick): launch standing pillars forward as flying megalith projectiles!
            Vec3d kickDir = new Vec3d(dirX, dirY, dirZ);
            if (kickDir.lengthSquared() < 1e-4) kickDir = new Vec3d(0, 0, 1);
            kickDir = kickDir.normalize();
            Vec3d kickVel = kickDir.multiply(1.4); // MEGALITH_SPEED

            for (VfxKey k : toDiscard) {
                ActiveVfx vfx = ACTIVE_ENTITIES.remove(k);
                PILLAR_GROUND_POSITIONS.remove(k);
                SERVER_POSITIONS.remove(k);
                if (vfx != null && vfx.entity() != null) {
                    Vec3d startPos = vfx.entity().getPos().add(0, 1.25, 0);
                    FLYING_MEGALITHS_CLIENT.add(new FlyingMegalithVfx(vfx.entity(), startPos, kickVel, 30));
                }
            }

            if (client.player != null && client.player.getUuid().equals(casterUuid)) {
                client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                com.avatarmod.elements.client.anim.AvatarAnimations.triggerComboAnimation(
                        client.player,
                        net.minecraft.util.Identifier.of("avatar_elements", "martial_roundhouse"),
                        2,
                        com.zigythebird.playeranimcore.easing.EasingType.EASE_OUT_CUBIC
                );
                com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerRoll(-8.0f, 12);
                com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerShake(0.6f, 10);
            }
        } else if (actionType == 1) {
            // STRIKE (Rapid Barrage): trigger punch feedback & hand swing
            if (client.player != null && client.player.getUuid().equals(casterUuid)) {
                client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                var animId = com.avatarmod.elements.client.anim.AvatarAnimations.getAnimationForSkill("fire_jab");
                if (animId != null) {
                    com.avatarmod.elements.client.anim.AvatarAnimations.triggerComboAnimation(client.player, animId);
                }
            }
        } else if (actionType == 2) {
            // CRUMBLE: discard standing pillar
            for (VfxKey k : toDiscard) {
                ActiveVfx vfx = ACTIVE_ENTITIES.remove(k);
                PILLAR_GROUND_POSITIONS.remove(k);
                SERVER_POSITIONS.remove(k);
                if (vfx != null && vfx.entity() != null) {
                    vfx.entity().discard();
                }
            }
        }
    }

    public static boolean hasNearbyPillarClient(Vec3d pos, double maxDist) {
        double maxDistSq = maxDist * maxDist;
        for (Vec3d gPos : PILLAR_GROUND_POSITIONS.values()) {
            if (gPos.squaredDistanceTo(pos) <= maxDistSq) {
                return true;
            }
        }
        for (ActiveVfx vfx : ACTIVE_ENTITIES.values()) {
            if (vfx.type() == VfxType.EARTH_PILLAR && vfx.entity() != null && !vfx.entity().isRemoved()) {
                if (vfx.entity().squaredDistanceTo(pos) <= maxDistSq) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Client-side approximation of EarthPillarSkill.findPillarCenter.
     * Walks the caster's horizontal look direction and raycasts down through air & water to lock solid ground/seabed.
     */
    private static Vec3d findPillarGroundClient(PlayerEntity caster, double range) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client == null || client.world == null) {
            return caster.getPos();
        }

        Vec3d eye = caster.getEyePos();
        Vec3d look = caster.getRotationVec(1.0f);

        // 1. Line-of-sight raycast penetrating water
        Vec3d lookEnd = eye.add(look.multiply(range));
        net.minecraft.world.RaycastContext lookCtx = new net.minecraft.world.RaycastContext(
                eye, lookEnd,
                net.minecraft.world.RaycastContext.ShapeType.COLLIDER,
                net.minecraft.world.RaycastContext.FluidHandling.NONE,
                caster
        );
        net.minecraft.util.hit.BlockHitResult lookHit = client.world.raycast(lookCtx);
        if (lookHit.getType() == net.minecraft.util.hit.HitResult.Type.BLOCK) {
            return new Vec3d(lookHit.getPos().x, lookHit.getBlockPos().getY() + 1.0, lookHit.getPos().z);
        }

        Vec3d dir = new Vec3d(look.x, 0, look.z);
        if (dir.lengthSquared() < 1.0e-4) dir = Vec3d.fromPolar(0, caster.getYaw());
        dir = dir.normalize();

        Vec3d target = caster.getPos().add(dir.multiply(range));
        net.minecraft.util.math.BlockPos cursor = net.minecraft.util.math.BlockPos.ofFloored(target);

        // Scan upward if buried in hill
        if (!client.world.getBlockState(cursor).getCollisionShape(client.world, cursor).isEmpty()) {
            for (int i = 0; i <= 8; i++) {
                net.minecraft.util.math.BlockPos above = cursor.up(i);
                if (client.world.getBlockState(above).getCollisionShape(client.world, above).isEmpty()) {
                    return new Vec3d(target.x, above.getY(), target.z);
                }
            }
        }

        // Raycast downward through air & water up to 64 blocks to find solid seabed/ground
        Vec3d start = new Vec3d(target.x, cursor.getY() + 0.5, target.z);
        Vec3d end = new Vec3d(target.x, Math.max((double) client.world.getBottomY(), cursor.getY() - 64.0), target.z);
        net.minecraft.world.RaycastContext downCtx = new net.minecraft.world.RaycastContext(
                start, end,
                net.minecraft.world.RaycastContext.ShapeType.COLLIDER,
                net.minecraft.world.RaycastContext.FluidHandling.NONE,
                caster
        );
        net.minecraft.util.hit.BlockHitResult downHit = client.world.raycast(downCtx);
        if (downHit.getType() == net.minecraft.util.hit.HitResult.Type.BLOCK) {
            return new Vec3d(target.x, downHit.getBlockPos().getY() + 1.0, target.z);
        }

        return target;
    }
}
