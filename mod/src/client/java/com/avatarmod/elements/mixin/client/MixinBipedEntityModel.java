package com.avatarmod.elements.mixin.client;

import net.minecraft.client.render.entity.model.BipedEntityModel;
import net.minecraft.entity.LivingEntity;
import net.minecraft.client.model.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Combat stance and martial arts posing for Avatar Elements.
 *
 * NOTE: Dynamic skeletal poses (including combat stances and staff attacks)
 * are managed exclusively through PlayerAnimationLib (PAL) layers to prevent
 * locking vanilla arm swing progress, mining/breaking blocks, and left-click attacks.
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
        // Disabled: Skeletal animations are now delegated to PlayerAnimationLib (PAL)
        // to maintain native hand swing progress and fluid player control.
    }
}
