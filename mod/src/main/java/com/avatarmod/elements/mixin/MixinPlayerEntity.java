package com.avatarmod.elements.mixin;

import com.avatarmod.elements.data.PlayerBendingData;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.damage.DamageTypes;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.server.network.ServerPlayerEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Grants intrinsic elemental passives:
 * - Firebenders are completely immune to environmental fire, burn ticks, and campfire damage.
 */
@Mixin(PlayerEntity.class)
public abstract class MixinPlayerEntity {

    @Inject(method = "isFireImmune", at = @At("HEAD"), cancellable = true)
    private void avatar$firebenderFireImmunity(CallbackInfoReturnable<Boolean> cir) {
        if ((Object) this instanceof ServerPlayerEntity sp) {
            PlayerBendingData data = PlayerBendingData.get(sp);
            if (data != null && "FIRE".equals(data.getActiveElement())) {
                cir.setReturnValue(true);
            }
        }
    }

    @Inject(method = "tick", at = @At("HEAD"))
    private void avatar$firebenderExtinguish(CallbackInfo ci) {
        PlayerEntity self = (PlayerEntity) (Object) this;
        if (self.isOnFire() && self instanceof ServerPlayerEntity sp) {
            PlayerBendingData data = PlayerBendingData.get(sp);
            if (data != null && "FIRE".equals(data.getActiveElement())) {
                self.extinguish();
            }
        }
    }

    @Inject(method = "damage", at = @At("HEAD"), cancellable = true)
    private void avatar$firebenderDamageImmunity(DamageSource source, float amount, CallbackInfoReturnable<Boolean> cir) {
        PlayerEntity self = (PlayerEntity) (Object) this;
        if (self instanceof ServerPlayerEntity sp) {
            PlayerBendingData data = PlayerBendingData.get(sp);
            if (data != null && "FIRE".equals(data.getActiveElement())) {
                if (source.isOf(DamageTypes.IN_FIRE) || source.isOf(DamageTypes.ON_FIRE) || source.isOf(DamageTypes.CAMPFIRE)) {
                    self.extinguish();
                    cir.setReturnValue(false);
                }
            }
        }
    }
}
