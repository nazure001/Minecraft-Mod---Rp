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

    private CinematicVfxController() {}

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
            ActiveVfx removed = ACTIVE_ENTITIES.remove(key);
            if (removed != null && removed.entity() != null) {
                removed.entity().discard();
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
                type = VfxType.SWIRL_VORTEX;
            } else if (sid.contains("avatar_state")) {
                type = VfxType.RUNE_DISC;
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
            if (type == VfxType.CRESCENT_SLASH) {
                Vec3d look = caster.getRotationVec(1.0f);
                entity.setPosition(caster.getX() + look.x * 0.8, caster.getEyeY() - 0.2 + look.y * 0.8, caster.getZ() + look.z * 0.8);
                entity.setYaw(yaw);
                entity.setPitch(pitch);
            } else if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
                entity.setPosition(caster.getX(), caster.getY() + 0.05, caster.getZ());
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
        } else if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
            initialTransform = VfxTransformUtil.createRuneDiscTransform(type.baseScale().x(), 0.0f);
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
                } else {
                    entity.setPosition(caster.getX(), caster.getY() + 0.5, caster.getZ());
                }
            }

            DisplayEntityAccessor dispAcc = (DisplayEntityAccessor) entity;
            if (type == VfxType.RUNE_DISC || type == VfxType.MAGIC_RUNE_CIRCLE) {
                float spinAngle = (vfx.ageTicks() * type.rotationSpeed()) % 360.0f;
                dispAcc.invokeSetTransformation(VfxTransformUtil.createRuneDiscTransform(type.baseScale().x(), spinAngle));
            } else if (type == VfxType.AEGIS_DOME) {
                float progress = Math.min(1.0f, vfx.ageTicks() / 3.0f);
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(VfxTransformUtil.createUniformScaleTransform(scale.x()));
            } else if (type == VfxType.CRESCENT_SLASH) {
                float progress = Math.min(1.0f, (float) vfx.ageTicks() / (float) vfx.maxAgeTicks());
                Vector3f scale = VfxTransformUtil.scaleInterpolation(type.baseScale(), type.targetScale(), progress);
                dispAcc.invokeSetTransformation(VfxTransformUtil.createSlashTransform(entity.getYaw(), entity.getPitch(), scale, 0.5f + vfx.ageTicks() * 0.2f));
            }
        }

        for (VfxKey k : expired) {
            ACTIVE_ENTITIES.remove(k);
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
            if (removed != null && removed.entity() != null) {
                removed.entity().discard();
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
                toRemove.add(k);
            }
        }
        for (VfxKey k : toRemove) {
            ActiveVfx removed = ACTIVE_ENTITIES.remove(k);
            if (removed != null && removed.entity() != null) {
                removed.entity().discard();
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
}
