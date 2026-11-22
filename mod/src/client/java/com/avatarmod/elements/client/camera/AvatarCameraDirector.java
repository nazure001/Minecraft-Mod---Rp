package com.avatarmod.elements.client.camera;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.Camera;
import net.minecraft.entity.Entity;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.RaycastContext;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * Dynamic Cinematic Camera Director for Avatar: Elements (inspired by Ultimate Battle).
 *
 * Implements:
 * 1. Trauma-based Rotational & Translational Screenshake:
 *    Uses polynomial trauma decay (Trauma^2) coupled with smooth, irrational harmonic
 *    oscillations for Pitch, Yaw, and Roll. Eliminates world-coordinate eye jittering and
 *    provides silky-smooth, visceral impact feedback.
 * 2. Dutch Angle Camera Roll:
 *    Hermite smoothstep ease-out tilting on heavy martial slashes, dives, and Avatar State.
 * 3. Raycast Anti-Clipping Orbit:
 *    Ensures third-person camera dynamically pulls in front of walls/obstacles.
 * 4. Sub-tick frame interpolation:
 *    Uses render tickDelta for continuous 60+ FPS motion without tick jitter.
 */
public final class AvatarCameraDirector {

    private static boolean enabled = true;

    // Roll (Dutch Angle)
    private static float currentRoll = 0.0f;
    private static float targetRoll = 0.0f;
    private static int rollDuration = 0;
    private static int rollAge = 0;

    // Trauma-based Screenshake (0.0 to 1.0)
    private static float trauma = 0.0f;
    private static float shakeIntensity = 0.0f;
    private static int shakeTicks = 0;
    private static int shakeMaxTicks = 0;
    private static long clientTickCounter = 0;

    // Cinematic Orbit
    private static boolean cinematicOrbit = false;
    private static int orbitTicksRemaining = 0;
    private static int orbitMaxTicks = 0;
    private static float orbitDistance = 4.5f;

    // Constants for screen shake tuning
    private static final float MAX_PITCH_SHAKE = 4.5f;  // degrees
    private static final float MAX_YAW_SHAKE   = 4.0f;  // degrees
    private static final float MAX_ROLL_SHAKE  = 5.0f;  // degrees
    private static final float MAX_EYE_OFFSET  = 0.06f; // max local translation (blocks)

    private AvatarCameraDirector() {}

    public static boolean isEnabled() {
        return enabled;
    }

    public static void setEnabled(boolean value) {
        enabled = value;
    }

    public static void triggerRoll(float degrees, int durationTicks) {
        if (!enabled) return;
        targetRoll = degrees;
        rollDuration = Math.max(1, durationTicks);
        rollAge = 0;
    }

    public static void triggerShake(float intensity, int durationTicks) {
        if (!enabled) return;
        shakeIntensity = Math.max(shakeIntensity, intensity);
        trauma = Math.min(1.0f, trauma + Math.min(1.0f, intensity));
        shakeTicks = Math.max(shakeTicks, durationTicks);
        shakeMaxTicks = Math.max(shakeMaxTicks, durationTicks);
    }

    public static void triggerCinematicOrbit(float targetDist, int durationTicks) {
        if (!enabled) return;
        cinematicOrbit = true;
        orbitDistance = targetDist;
        orbitTicksRemaining = durationTicks;
        orbitMaxTicks = durationTicks;
        triggerRoll(12.0f, durationTicks);
    }

    public static void tick() {
        clientTickCounter++;

        // Tick roll with smoothstep ease-out
        if (rollDuration > 0 && rollAge < rollDuration) {
            rollAge++;
            float p = (float) rollAge / (float) rollDuration;
            // Smooth hermite decay: f(p) = 1 - (3*p^2 - 2*p^3)
            float factor = Math.max(0.0f, 1.0f - (3.0f * p * p - 2.0f * p * p * p));
            currentRoll = targetRoll * factor;
        } else {
            currentRoll = 0.0f;
            targetRoll = 0.0f;
            rollDuration = 0;
            rollAge = 0;
        }

        // Tick shake & trauma decay
        if (shakeTicks > 0) {
            shakeTicks--;
            float decayStep = 1.0f / Math.max(1, shakeMaxTicks);
            trauma = Math.max(0.0f, trauma - decayStep);
            if (shakeTicks == 0 || trauma <= 0.001f) {
                shakeIntensity = 0.0f;
                shakeMaxTicks = 0;
                trauma = 0.0f;
            }
        } else {
            trauma = 0.0f;
            shakeIntensity = 0.0f;
            shakeMaxTicks = 0;
        }

        // Tick cinematic orbit
        if (orbitTicksRemaining > 0) {
            orbitTicksRemaining--;
            if (orbitTicksRemaining == 0) {
                cinematicOrbit = false;
            }
        }
    }

    /**
     * Called from MixinCamera.update (TAIL) to apply Dutch angle roll, screenshake, and anti-clipping orbit.
     * Returns new camera position if modified, or null if position is untouched.
     */
    public static Vec3d calculateCameraAdjustment(Camera camera, Entity focusedEntity, Quaternionf rotation, boolean thirdPerson, float tickDelta) {
        if (!enabled || camera == null || focusedEntity == null) return null;
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.world == null) return null;

        // 1. Dutch Angle Camera Roll
        float roll = currentRoll;
        if (Math.abs(roll) > 0.01f) {
            rotation.rotateZ((float) Math.toRadians(roll));
        }

        // 2. Cinematic Trauma Screenshake (Rotational + subtle local translation)
        Vec3d currentPos = camera.getPos();
        Vec3d resultPos = currentPos;
        boolean posModified = false;

        if (trauma > 0.001f || shakeTicks > 0) {
            // Shake amplitude is quadratic trauma (Trauma^2) for snappy impact + soft silky falloff
            float effectiveTrauma = Math.max(trauma, (float) shakeTicks / Math.max(1, shakeMaxTicks));
            float shakeAmp = effectiveTrauma * effectiveTrauma * Math.max(0.2f, shakeIntensity);

            // Time with sub-tick interpolation for continuous 60+ FPS motion
            float renderTime = (float) (clientTickCounter) + tickDelta;

            // Incommensurate harmonic frequencies for organic, non-repeating feel
            float rotPitch = MAX_PITCH_SHAKE * shakeAmp * (float) (Math.sin(renderTime * 1.45) * 0.7 + Math.sin(renderTime * 2.89) * 0.3);
            float rotYaw   = MAX_YAW_SHAKE   * shakeAmp * (float) (Math.cos(renderTime * 1.83) * 0.7 + Math.cos(renderTime * 3.21) * 0.3);
            float rotRoll  = MAX_ROLL_SHAKE  * shakeAmp * (float) (Math.sin(renderTime * 2.11) * 0.7 + Math.cos(renderTime * 3.77) * 0.3);

            // Apply angular trauma to camera rotation matrix
            rotation.rotateX((float) Math.toRadians(rotPitch));
            rotation.rotateY((float) Math.toRadians(rotYaw));
            rotation.rotateZ((float) Math.toRadians(rotRoll));

            // Subtle camera-local translation (along local Up and Right axes, never raw world XYZ)
            Vector3f localRight = new Vector3f(1.0f, 0.0f, 0.0f).rotate(rotation);
            Vector3f localUp    = new Vector3f(0.0f, 1.0f, 0.0f).rotate(rotation);

            float localOffsetX = MAX_EYE_OFFSET * shakeAmp * (float) Math.sin(renderTime * 1.62);
            float localOffsetY = MAX_EYE_OFFSET * shakeAmp * (float) Math.cos(renderTime * 2.14);

            resultPos = resultPos.add(
                    localRight.x * localOffsetX + localUp.x * localOffsetY,
                    localRight.y * localOffsetX + localUp.y * localOffsetY,
                    localRight.z * localOffsetX + localUp.z * localOffsetY
            );
            posModified = true;
        }

        // 3. Cinematic Orbit & Raycast Anti-Clipping
        if (cinematicOrbit && focusedEntity == client.player) {
            Vec3d eye = focusedEntity.getCameraPosVec(tickDelta);
            Vec3d look = focusedEntity.getRotationVec(tickDelta);
            Vec3d back = new Vec3d(-look.x, Math.max(-0.2, -look.y + 0.2), -look.z).normalize();
            Vec3d targetCamPos = eye.add(back.multiply(orbitDistance));

            // Raycast anti-clipping check from eye to targetCamPos
            RaycastContext clipCtx = new RaycastContext(
                    eye,
                    targetCamPos,
                    RaycastContext.ShapeType.COLLIDER,
                    RaycastContext.FluidHandling.NONE,
                    focusedEntity
            );
            BlockHitResult hit = client.world.raycast(clipCtx);
            if (hit.getType() == HitResult.Type.BLOCK) {
                // Pull camera forward in front of the blocking wall
                Vec3d hitPos = hit.getPos();
                Vec3d safeDir = eye.subtract(hitPos).normalize();
                resultPos = hitPos.add(safeDir.multiply(0.2));
            } else {
                resultPos = targetCamPos;
            }
            posModified = true;
        }

        return posModified ? resultPos : null;
    }

    public static float getCurrentRoll() {
        return currentRoll;
    }

    public static boolean isShaking() {
        return shakeTicks > 0 || trauma > 0.001f;
    }

    public static boolean isCinematicActive() {
        return cinematicOrbit;
    }
}
