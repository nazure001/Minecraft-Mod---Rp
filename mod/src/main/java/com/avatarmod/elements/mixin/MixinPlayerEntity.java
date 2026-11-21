package com.avatarmod.elements.mixin;

import com.avatarmod.elements.data.PlayerBendingData;
import net.minecraft.entity.Entity;
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
 * Grants intrinsic elemental passives and environmental immunities:
 *
 * Canon & Gameplay Immunity Architecture:
 * 1. Environmental & Self-Inflicted Immunity:
 *    - Firebender: 100% immune to ambient fire (IN_FIRE, ON_FIRE, CAMPFIRE), never burns themselves.
 *    - Waterbender: 100% immune to freezing damage (FREEZE) and harsh cold.
 *    - Airbender: 100% immune to fall damage (FALL) via instinctive air cushioning.
 *    - Earthbender: 100% immune to falling blocks (FALLING_BLOCK, FALLING_STALACTITE) and suffocation (IN_WALL).
 *
 * 2. Opponent Skill Penetration:
 *    - If damage is caused by an opponent (attacker != null && attacker != self), damage connects!
 *    - A Firebender hit by another player's Fire Blast still takes damage (like Zuko in an Agni Kai),
 *      but their fire mastery auto-extinguishes residual burn ticks immediately.
 */
@Mixin(PlayerEntity.class)
public abstract class MixinPlayerEntity {

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
    private void avatar$elementalDamagePassives(DamageSource source, float amount, CallbackInfoReturnable<Boolean> cir) {
        PlayerEntity self = (PlayerEntity) (Object) this;
        if (!(self instanceof ServerPlayerEntity sp)) return;

        PlayerBendingData data = PlayerBendingData.get(sp);
        if (data == null) return;
        String element = data.getActiveElement();
        if (element == null) return;

        Entity attacker = source.getAttacker();
        boolean isOpponentAttack = (attacker != null && attacker != self);

        switch (element) {
            case "FIRE" -> {
                if (source.isOf(DamageTypes.IN_FIRE) || source.isOf(DamageTypes.ON_FIRE) || source.isOf(DamageTypes.CAMPFIRE)) {
                    // Firebenders are completely immune to environmental fire and self-inflicted flames
                    if (!isOpponentAttack) {
                        self.extinguish();
                        cir.setReturnValue(false);
                    } else {
                        // Opponent's fire attacks deal direct damage, but firebender auto-extinguishes after-burn
                        self.extinguish();
                    }
                }
            }
            case "WATER" -> {
                // Waterbenders are immune to ambient freezing damage (Powder Snow)
                if (source.isOf(DamageTypes.FREEZE) && !isOpponentAttack) {
                    cir.setReturnValue(false);
                }
            }
            case "AIR" -> {
                // Airbenders cushion falls with natural kinetic air glides
                if (source.isOf(DamageTypes.FALL) && !isOpponentAttack) {
                    cir.setReturnValue(false);
                }
            }
            case "EARTH" -> {
                // Earthbenders are immune to cave-in collapses, falling rock debris, and wall suffocation
                if ((source.isOf(DamageTypes.FALLING_BLOCK) || source.isOf(DamageTypes.FALLING_STALACTITE) || source.isOf(DamageTypes.IN_WALL)) && !isOpponentAttack) {
                    cir.setReturnValue(false);
                }
            }
        }
    }
}
