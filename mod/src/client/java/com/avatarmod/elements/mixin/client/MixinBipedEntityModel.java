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
     * Pose — Sikap Siaga (Ready Stance) from CLAUDE_READY_POSE_HANDOFF.md §7.
     * Vanilla 6-bone projection of full upper_arm+forearm+staff rig.
     * All angles are ABSOLUTE (override vanilla walk animation while staff held).
     *
     * Source values (degrees → radians):
     *   torso  : yaw -25° / pitch +5°
     *   head   : yaw compensates body, pitch -5°
     *   rightArm: projected from V=[+0.867,-9.186,-0.738] → pitch+4.6°/yaw-5.4°/roll+5.4°
     *   leftArm : projected from V=[+3.666,-8.159,-2.741] → pitch+17°/yaw+24.1°/roll-22.5°
     *
     * Elbow bend requires PAL custom bones — next phase after fire_jab verified.
     */
    private void applyReadyPose() {
        body.yaw   = -0.4363f; // -25.0°
        body.pitch =  0.0873f; // +5.0°

        // Head compensates body yaw so gaze stays forward; pitch from handoff
        head.yaw  +=  0.4363f; // +25.0° offset
        head.pitch = -0.0873f; // -5.0°

        rightArm.pitch =  0.0803f; // +4.6°
        rightArm.yaw   = -0.0942f; // -5.4°
        rightArm.roll  =  0.0942f; // +5.4°

        leftArm.pitch  =  0.2967f; // +17.0°
        leftArm.yaw    =  0.4208f; // +24.1°
        leftArm.roll   = -0.3927f; // -22.5°
    }
}
