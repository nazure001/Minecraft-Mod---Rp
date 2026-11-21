package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.item.AvatarItems;
import net.minecraft.client.model.ModelPart;
import net.minecraft.client.render.entity.model.BipedEntityModel;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Combat stance and heavy weapon posing for Avatar Elements.
 *
 * Implements authentic weight-based posture for heavy weapons (e.g. Earth Hammer):
 * - Idle/walking: Rests massive hammer shaft over the right shoulder with supportive offhand grip.
 * - Sprinting: Drags the colossal hammer low behind the player along the ground.
 * - Actively swinging / PAL animations: Hands yield to swing progress to preserve fluid combat.
 */
@Mixin(BipedEntityModel.class)
public abstract class MixinBipedEntityModel<T extends LivingEntity> {

    @Shadow public ModelPart head;
    @Shadow public ModelPart body;
    @Shadow public ModelPart rightArm;
    @Shadow public ModelPart leftArm;

    @Inject(method = "setAngles", at = @At("TAIL"))
    private void avatarMod_applyHeavyWeaponGripPose(
            T entity, float limbAngle, float limbDistance,
            float age, float headYaw, float headPitch,
            CallbackInfo ci) {
        if (entity instanceof PlayerEntity player) {
            // Check if holding heavy Earth Hammer in main hand
            boolean hasHeavyHammer = player.getMainHandStack().isOf(AvatarItems.EARTH_HAMMER);
            if (hasHeavyHammer && !entity.handSwinging && entity.getHandSwingProgress(1.0f) <= 0.001f) {
                if (player.isSprinting()) {
                    // Dragging heavy hammer along the ground trailing behind
                    this.rightArm.pitch = 0.72f;
                    this.rightArm.yaw = 0.22f;
                    this.rightArm.roll = 0.12f;
                } else {
                    // Resting heavy hammer on shoulder (classic Colossal Weapon stance)
                    this.rightArm.pitch = -1.35f;
                    this.rightArm.yaw = -0.32f;
                    this.rightArm.roll = 0.26f;

                    if (player.getOffHandStack().isEmpty()) {
                        // Left arm supports the shaft across chest in two-handed stance
                        this.leftArm.pitch = -0.72f;
                        this.leftArm.yaw = 0.52f;
                        this.leftArm.roll = -0.16f;
                    }
                }
            }
        }
    }
}
