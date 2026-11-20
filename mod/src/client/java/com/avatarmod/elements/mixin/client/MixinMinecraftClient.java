package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.client.combat.AvatarCombatClient;
import net.minecraft.client.MinecraftClient;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Intercepts attack actions on MinecraftClient to execute fluid elemental
 * martial arts combos and dive-kicks when unarmed or wielding an Avatar weapon.
 */
@Mixin(MinecraftClient.class)
public abstract class MixinMinecraftClient {

    @Inject(method = "doAttack", at = @At("HEAD"), cancellable = true)
    private void avatar$onDoAttack(CallbackInfoReturnable<Boolean> cir) {
        MinecraftClient client = (MinecraftClient) (Object) this;
        if (AvatarCombatClient.tryHandleAttack(client)) {
            cir.setReturnValue(true);
        }
    }
}
