package com.avatarmod.elements.client.camera;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.Camera;
import net.minecraft.entity.Entity;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.RaycastContext;
import org.joml.Quaternionf;

import java.util.Random;

/**
 * Dynamic Cinematic Camera Director for Avatar: Elements (inspired by Ultimate Battle).
 *
 * Provides:
 * 1. Dutch Angle Camera Roll: Rotates the camera matrix during heavy impacts, dive-kicks, and Avatar State.
 * 2. Directional Screenshake: Damped harmonic trauma decay on explosive impacts.
 * 3. Raycast Anti-Clipping Orbit: Clamps camera distance against solid blocks so third-person camera never clips into walls.
 * 4. Cinematic Ultimate Orbit: Smoothly pulls camera into dynamic third-person framing during Tier 3 ultimates.
 */
public final class AvatarCameraDirector {

    private static boolean enabled = true;
    private static final Random RNG = new Random();

    // Roll (Dutch Angle)
    private static float currentRoll = 0.0f;
    private static float targetRoll = 0.0f;
    private static int rollDuration = 0;
    private static int rollAge = 0;

    // Screenshake
    private static float shakeIntensity = 0.0f;
    private static int shakeTicks = 0;
    private static int shakeMaxTicks = 0;

    // Cinematic Orbit
    private static boolean cinematicOrbit = false;
    private static int orbitTicksRemaining = 0;
    private static int orbitMaxTicks = 0;
    private static float orbitDistance = 4.5f;

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
        // Tick roll
        if (rollDuration > 0 && rollAge < rollDuration) {
            rollAge++;
            float progress = (float) rollAge / (float) rollDuration;
            // Ease out back to 0
            currentRoll = targetRoll * (1.0f - progress);
        } else {
            currentRoll = 0.0f;
            targetRoll = 0.0f;
            rollDuration = 0;
        }

        // Tick shake
        if (shakeTicks > 0) {
            shakeTicks--;
            if (shakeTicks == 0) {
                shakeIntensity = 0.0f;
                shakeMaxTicks = 0;
            }
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

        Vec3d currentPos = camera.getPos();
        Vec3d resultPos = currentPos;
        boolean posModified = false;

        // 2. Cinematic Orbit & Raycast Anti-Clipping
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

        // 3. Screenshake Jitter
        if (shakeTicks > 0 && shakeIntensity > 0.001f) {
            float progress = (float) shakeTicks / (float) Math.max(1, shakeMaxTicks);
            float currentAmp = shakeIntensity * progress * progress; // Quadratic decay
            float shakeX = (float) (Math.sin(System.currentTimeMillis() * 0.05) * currentAmp * 0.35);
            float shakeY = (float) (Math.cos(System.currentTimeMillis() * 0.07) * currentAmp * 0.25);
            float shakeZ = (float) (Math.sin(System.currentTimeMillis() * 0.09) * currentAmp * 0.25);

            resultPos = resultPos.add(shakeX, shakeY, shakeZ);
            posModified = true;
        }

        return posModified ? resultPos : null;
    }

    public static float getCurrentRoll() {
        return currentRoll;
    }

    public static boolean isShaking() {
        return shakeTicks > 0;
    }

    public static boolean isCinematicActive() {
        return cinematicOrbit;
    }
}
