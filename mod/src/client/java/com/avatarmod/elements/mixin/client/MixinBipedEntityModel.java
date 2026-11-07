package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.item.AvatarItems;
import net.minecraft.client.render.entity.model.BipedEntityModel;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.client.model.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * PoC: apply static "Sikap Siaga" (ready stance) bone angles when
 * player holds the air_staff and is not in combat.
 *
 * Bone limits (vanilla PlayerEntityModel):
 *   head, body, rightArm, leftArm, rightLeg, leftLeg (+ sleeve/pants layers)
 *   NO upper_arm / forearm — elbow bend requires GeckoLib or EMF.
 */
@Mixin(BipedEntityModel.class)
public abstract class MixinBipedEntityModel<T extends LivingEntity> {

    @Shadow public ModelPart head;
    @Shadow public ModelPart body;
    @Shadow public ModelPart rightArm;
    @Shadow public ModelPart leftArm;

    @Inject(method = "setAngles", at = @At("TAIL"))
    private void avatarMod_applyStaffReadyPose(
            T entity, float limbAngle, float limbDistance,
            float age, float headYaw, float headPitch,
            CallbackInfo ci) {

        if (!(entity instanceof PlayerEntity player)) return;

        // Only apply when holding air_staff in main hand
        if (!player.getMainHandStack().isOf(AvatarItems.AIR_STAFF)) return;

        // Skip during locomotion to avoid jank (limbDistance > 0.1 means moving fast)
        // For PoC we apply regardless; refine after visual review
        applyReadyPose();
    }

    /**
     * Pose 1 — Sikap Siaga (Ready Stance) derived from pose_data.json:
     *   torso.yaw  = +18°  → 0.314 rad
     *   torso.pitch=  +2°  → 0.035 rad
     *   head compensates torso yaw so gaze stays forward
     *
     * Arm angles are approximated from staff contact data
     * (rh_u_on_staff=5.5, lh_u_on_staff=15.0 → right hand near grip, left near middle).
     * Full IK solve deferred until elbow-bone support (GeckoLib phase).
     */
    private void applyReadyPose() {
        // Torso rotation (adds to vanilla body swing)
        body.yaw += 0.31f;    // +18°
        body.pitch += 0.035f; // +2°

        // Right arm — dominant/rear grip, slightly lowered at side-hip
        rightArm.pitch = -0.55f;  // ~-31° forward
        rightArm.yaw   =  0.20f;  //  ~12° inward
        rightArm.roll  =  0.10f;

        // Left arm — guide/front grip, stretched forward across chest
        leftArm.pitch = -0.80f;   // ~-46° forward
        leftArm.yaw   = -0.30f;   //  ~17° outward
        leftArm.roll  = -0.08f;

        // Head: vanilla already sets headYaw/headPitch to track look direction.
        // Compensate for body yaw so the head tracks the same world direction.
        head.yaw -= 0.31f;
    }
}
