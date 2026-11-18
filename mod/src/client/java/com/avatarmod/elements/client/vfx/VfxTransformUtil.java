package com.avatarmod.elements.client.vfx;

import net.minecraft.entity.decoration.Brightness;
import net.minecraft.util.math.AffineTransformation;
import net.minecraft.util.math.MathHelper;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * Mathematical and transform utility for Cinematic 3D VFX using Minecraft Display Entities.
 */
public final class VfxTransformUtil {

    private VfxTransformUtil() {}

    /**
     * Creates a rotation quaternion for a ground rune disc lying flat on the XZ plane:
     * 90° pitch rotation around X-axis plus continuous spin rotation around Z-axis.
     *
     * @param angleDegrees Spin rotation in degrees around the disc's surface normal
     * @return Calculated JOML Quaternionf
     */
    public static Quaternionf groundRuneDiscRotation(float angleDegrees) {
        return new Quaternionf()
                .rotateX((float) Math.toRadians(90.0))
                .rotateZ((float) Math.toRadians(angleDegrees));
    }

    /**
     * Creates a rotation quaternion for a crescent wave projectile aligned with the caster's look direction.
     *
     * @param playerYaw   Player yaw angle in degrees
     * @param playerPitch Player pitch angle in degrees
     * @return Calculated JOML Quaternionf aligned with look direction
     */
    public static Quaternionf crescentWaveRotation(float playerYaw, float playerPitch) {
        return new Quaternionf()
                .rotateY((float) Math.toRadians(180.0f - playerYaw))
                .rotateX((float) Math.toRadians(-playerPitch));
    }

    /**
     * Interpolates scale vector smoothly between start and target vectors.
     *
     * @param startScale  Starting scale vector (at progress = 0.0)
     * @param targetScale Target scale vector (at progress = 1.0)
     * @param progress    Interpolation fraction in range [0.0, 1.0]
     * @return Interpolated Vector3f
     */
    public static Vector3f scaleInterpolation(Vector3f startScale, Vector3f targetScale, float progress) {
        float clamped = MathHelper.clamp(progress, 0.0f, 1.0f);
        return new Vector3f(startScale).lerp(targetScale, clamped);
    }

    /**
     * Returns full emissive brightness (sky: 15, block: 15) for shader and dark environment bloom.
     *
     * @return Brightness.FULL instance
     */
    public static Brightness fullBrightness() {
        return Brightness.FULL;
    }

    /**
     * Helper to create a complete AffineTransformation for a spinning ground rune disc.
     */
    public static AffineTransformation createRuneDiscTransform(float scale, float angleDegrees) {
        return new AffineTransformation(
                new Vector3f(0.0f, 0.05f, 0.0f),
                groundRuneDiscRotation(angleDegrees),
                new Vector3f(scale, scale, 0.05f),
                new Quaternionf()
        );
    }

    /**
     * Helper to create a complete AffineTransformation for a crescent wave slash.
     */
    public static AffineTransformation createSlashTransform(float yaw, float pitch, Vector3f scale, float forwardOffset) {
        return new AffineTransformation(
                new Vector3f(0.0f, 0.0f, forwardOffset),
                crescentWaveRotation(yaw, pitch),
                scale,
                new Quaternionf()
        );
    }

    /**
     * Non-uniform scale for the Earth Pillar: the Java model is 2.0 blocks tall
     * but PILLAR_HEIGHT is 2.5, so stretch Y by 1.25 while keeping XZ at 1.0.
     */
    public static AffineTransformation createPillarTransform(float xzScale, float yScale) {
        return new AffineTransformation(
                new Vector3f(0.0f, 0.0f, 0.0f),
                new Quaternionf(),
                new Vector3f(xzScale, yScale, xzScale),
                new Quaternionf()
        );
    }

    /**
     * Helper to create a uniform scale AffineTransformation (e.g. expanding spherical dome).
     */
    public static AffineTransformation createUniformScaleTransform(float scale) {
        return new AffineTransformation(
                new Vector3f(0.0f, 0.0f, 0.0f),
                new Quaternionf(),
                new Vector3f(scale, scale, scale),
                new Quaternionf()
        );
    }

    /**
     * General constructor helper for AffineTransformation.
     */
    public static AffineTransformation createTransform(Vector3f translation, Quaternionf leftRotation, Vector3f scale, Quaternionf rightRotation) {
        return new AffineTransformation(translation, leftRotation, scale, rightRotation);
    }
}
