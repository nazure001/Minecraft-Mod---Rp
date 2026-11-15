package com.avatarmod.elements.client.vfx;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.client.render.entity.PlayerEntityRenderer;
import net.minecraft.client.render.entity.model.PlayerEntityModel;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Arm;
import net.minecraft.util.math.MathHelper;
import net.minecraft.util.math.RotationAxis;
import net.minecraft.util.math.Vec3d;
import org.joml.Matrix4f;
import org.joml.Vector4f;

/**
 * Helper class for computing attachment point positions (e.g. right knuckle for flame bursts)
 * anchored to the player's animated rig in 3D world space.
 *
 * Implements Animation Rig <-> VFX Placement Contract (R4 / M3):
 * Knuckle Point: P_knuckle = Matrix_right_arm * [-1.0/16.0, 8.0/16.0, 0.0]^T
 */
public final class KnuckleVfxHelper {

    /**
     * Local knuckle offset relative to the right_arm pivot.
     * In ModelPart coordinates (+Y points down towards feet), moving down the arm to the fist
     * requires +8.0 / 16.0 blocks. Steve's arm geometric center is at X = -1.0 / 16.0 blocks.
     */
    public static final Vec3d LOCAL_KNUCKLE_OFFSET = new Vec3d(-1.0 / 16.0, 8.0 / 16.0, 0.0);

    /**
     * Standard player model scale factor applied in PlayerEntityRenderer (15/16).
     */
    public static final float PLAYER_MODEL_SCALE = 0.9375F;

    /**
     * Calculates the world position of the right fist knuckle for the given player.
     *
     * @param player    The client player entity
     * @param tickDelta Render tick delta for sub-tick interpolation
     * @return World coordinates (Vec3d) of the right knuckle attachment point
     */
    public static Vec3d getKnucklePosition(AbstractClientPlayerEntity player, float tickDelta) {
        return getKnucklePosition(player, tickDelta, Arm.RIGHT);
    }

    /**
     * Calculates the world position of a fist knuckle (left or right arm).
     *
     * @param player    The client player entity
     * @param tickDelta Render tick delta for sub-tick interpolation
     * @param arm       The arm to query (Arm.RIGHT or Arm.LEFT)
     * @return World coordinates (Vec3d) of the knuckle attachment point
     */
    public static Vec3d getKnucklePosition(AbstractClientPlayerEntity player, float tickDelta, Arm arm) {
        if (player == null) {
            return Vec3d.ZERO;
        }

        MatrixStack matrices = new MatrixStack();
        applyPlayerArmTransform(matrices, player, tickDelta, arm);

        return transformKnuckle(matrices, LOCAL_KNUCKLE_OFFSET);
    }

    /**
     * Transforms a local offset vector relative to the arm pivot using the given MatrixStack.
     *
     * @param matrices    MatrixStack positioned and oriented at the arm bone
     * @param localOffset Local offset relative to arm pivot
     * @return Transformed coordinates as Vec3d
     */
    public static Vec3d transformKnuckle(MatrixStack matrices, Vec3d localOffset) {
        Matrix4f posMatrix = matrices.peek().getPositionMatrix();
        Vector4f vec = new Vector4f((float) localOffset.x, (float) localOffset.y, (float) localOffset.z, 1.0f);
        posMatrix.transform(vec);
        float w = (vec.w != 0.0f) ? vec.w : 1.0f;
        return new Vec3d(vec.x / w, vec.y / w, vec.z / w);
    }

    /**
     * Translates the MatrixStack by the default local knuckle offset [-1.0/16.0, 8.0/16.0, 0.0].
     *
     * @param matrices MatrixStack at the arm pivot
     */
    public static void translateToKnuckle(MatrixStack matrices) {
        matrices.translate(LOCAL_KNUCKLE_OFFSET.x, LOCAL_KNUCKLE_OFFSET.y, LOCAL_KNUCKLE_OFFSET.z);
    }

    /**
     * Applies full world-to-hand transformation to the given MatrixStack:
     * Lerped Position -> Body Yaw -> Entity Inversion/Scale -> setArmAngle.
     *
     * @param matrices  Target MatrixStack
     * @param player    Client player entity
     * @param tickDelta Sub-tick delta
     * @param arm       Arm to transform (Arm.RIGHT or Arm.LEFT)
     */
    public static void applyPlayerArmTransform(MatrixStack matrices, AbstractClientPlayerEntity player, float tickDelta, Arm arm) {
        Vec3d lerpedPos = player.getLerpedPos(tickDelta);
        matrices.translate(lerpedPos.x, lerpedPos.y, lerpedPos.z);

        float bodyYaw = MathHelper.lerpAngleDegrees(tickDelta, player.prevBodyYaw, player.bodyYaw);
        matrices.multiply(RotationAxis.POSITIVE_Y.rotationDegrees(180.0F - bodyYaw));
        matrices.scale(-1.0F, -1.0F, 1.0F);
        matrices.scale(PLAYER_MODEL_SCALE, PLAYER_MODEL_SCALE, PLAYER_MODEL_SCALE);
        matrices.translate(0.0F, -1.501F, 0.0F);

        MinecraftClient mc = MinecraftClient.getInstance();
        if (mc != null && mc.options != null && mc.options.getPerspective().isFirstPerson() && mc.player == player) {
            // In first-person perspective for the local player, 3rd-person model arm angle is not updated.
            // Fall back to standard arm pivot or first-person viewmodel projection.
            float armX = (arm == Arm.RIGHT ? -5.0F : 5.0F) / 16.0F;
            matrices.translate(armX, 2.0F / 16.0F, 0.0F);
            return;
        }

        if (mc != null && mc.getEntityRenderDispatcher() != null) {
            var renderer = mc.getEntityRenderDispatcher().getRenderer(player);
            if (renderer instanceof PlayerEntityRenderer playerRenderer) {
                PlayerEntityModel<AbstractClientPlayerEntity> model = playerRenderer.getModel();
                if (model != null) {
                    model.setArmAngle(arm, matrices);
                    return;
                }
            }
        }

        // Fallback when playerRenderer is unavailable (e.g. headless tests):
        // Standard right arm pivot offset relative to torso center in vanilla BipedEntityModel (rightArm: -5.0F, leftArm: +5.0F)
        float armX = (arm == Arm.RIGHT ? -5.0F : 5.0F) / 16.0F;
        matrices.translate(armX, 2.0F / 16.0F, 0.0F);
    }

    private KnuckleVfxHelper() {}
}
