package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.item.AvatarItems;
import net.minecraft.client.model.ModelPart;
import net.minecraft.client.render.entity.model.BipedEntityModel;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Combat stance and weapon posing for Avatar Elements (inspired by Ultimate Battle).
 *
 * Implements proportional martial arts and weapon-holding stances:
 * - Earth Hammer: Heavy weapon stance resting on shoulder / dragging behind while sprinting.
 * - Dual Swords (Zuko Dual Dao): Twin blade guard with blades angled outward ready to slice.
 * - Water Spear: Two-handed thrust posture ready to pierce / couched charging spear when sprinting.
 * - War Fan (Kyoshi Fans): Defensive upper-torso fan ward and graceful crane balance.
 * - Air Staff: Two-handed monk staff grip and horizontal dash vaulting.
 */
@Mixin(BipedEntityModel.class)
public abstract class MixinBipedEntityModel<T extends LivingEntity> {

    @Shadow public ModelPart head;
    @Shadow public ModelPart body;
    @Shadow public ModelPart rightArm;
    @Shadow public ModelPart leftArm;

    @Inject(method = "setAngles", at = @At("TAIL"))
    private void avatarMod_applyMartialWeaponGripPose(
            T entity, float limbAngle, float limbDistance,
            float age, float headYaw, float headPitch,
            CallbackInfo ci) {
        if (entity instanceof PlayerEntity player) {
            // If actively swinging with hand swing progress, allow swing animation to play
            if (entity.handSwinging || entity.getHandSwingProgress(1.0f) > 0.001f) {
                return;
            }

            ItemStack mainHand = player.getMainHandStack();
            ItemStack offHand = player.getOffHandStack();
            boolean sprinting = player.isSprinting();

            // 1. Earth Hammer (Colossal Weapon)
            if (mainHand.isOf(AvatarItems.EARTH_HAMMER)) {
                if (sprinting) {
                    this.rightArm.pitch = 0.72f;
                    this.rightArm.yaw = 0.22f;
                    this.rightArm.roll = 0.12f;
                } else {
                    this.rightArm.pitch = -1.35f;
                    this.rightArm.yaw = -0.32f;
                    this.rightArm.roll = 0.26f;
                    if (offHand.isEmpty()) {
                        this.leftArm.pitch = -0.72f;
                        this.leftArm.yaw = 0.52f;
                        this.leftArm.roll = -0.16f;
                    }
                }
                return;
            }

            // 2. Dual Swords (Zuko Twin Dao)
            if (mainHand.isOf(AvatarItems.DUAL_SWORDS)) {
                if (sprinting) {
                    // Aerodynamic twin blade sprint trailing behind
                    this.rightArm.pitch = 0.82f;
                    this.rightArm.yaw = 0.20f;
                    this.rightArm.roll = 0.15f;
                    this.leftArm.pitch = 0.82f;
                    this.leftArm.yaw = -0.20f;
                    this.leftArm.roll = -0.15f;
                } else {
                    // Balanced twin blade low-guard stance
                    this.rightArm.pitch = -0.65f;
                    this.rightArm.yaw = 0.32f;
                    this.rightArm.roll = -0.22f;
                    this.leftArm.pitch = -0.45f;
                    this.leftArm.yaw = -0.35f;
                    this.leftArm.roll = 0.18f;
                }
                return;
            }

            // 3. Water Spear (Tribal Harpoon / Spear)
            if (mainHand.isOf(AvatarItems.WATER_SPEAR)) {
                if (sprinting) {
                    // Couched lance charging posture
                    this.rightArm.pitch = -0.95f;
                    this.rightArm.yaw = 0.05f;
                    this.rightArm.roll = 0.05f;
                } else {
                    // Two-handed ready thrust guard
                    this.rightArm.pitch = -1.15f;
                    this.rightArm.yaw = -0.20f;
                    this.rightArm.roll = 0.02f;
                    if (offHand.isEmpty()) {
                        this.leftArm.pitch = -0.75f;
                        this.leftArm.yaw = 0.42f;
                        this.leftArm.roll = -0.12f;
                    }
                }
                return;
            }

            // 4. War Fan (Kyoshi War Fan)
            if (mainHand.isOf(AvatarItems.WAR_FAN)) {
                if (sprinting) {
                    this.rightArm.pitch = 0.65f;
                    this.rightArm.yaw = 0.20f;
                    this.leftArm.pitch = 0.65f;
                    this.leftArm.yaw = -0.20f;
                } else {
                    // Graceful defensive fan ward across upper chest
                    this.rightArm.pitch = -1.10f;
                    this.rightArm.yaw = 0.45f;
                    this.rightArm.roll = -0.55f;
                    if (offHand.isEmpty()) {
                        this.leftArm.pitch = -0.38f;
                        this.leftArm.yaw = -0.28f;
                        this.leftArm.roll = 0.22f;
                    }
                }
                return;
            }

            // 5. Air Staff (Monk Glider Staff)
            if (mainHand.isOf(AvatarItems.AIR_STAFF)) {
                if (sprinting) {
                    // Two-handed horizontal vault sprint
                    this.rightArm.pitch = -0.70f;
                    this.rightArm.yaw = -0.30f;
                    this.leftArm.pitch = -0.70f;
                    this.leftArm.yaw = 0.30f;
                } else {
                    // Diagonal two-handed monk guard
                    this.rightArm.pitch = -0.92f;
                    this.rightArm.yaw = -0.22f;
                    this.rightArm.roll = 0.08f;
                    if (offHand.isEmpty()) {
                        this.leftArm.pitch = -0.58f;
                        this.leftArm.yaw = 0.36f;
                        this.leftArm.roll = -0.10f;
                    }
                }
            }
        }
    }
}
