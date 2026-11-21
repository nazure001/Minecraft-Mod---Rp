package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.item.AvatarItems;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.client.network.ClientPlayerEntity;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.render.item.HeldItemRenderer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.item.ItemStack;
import net.minecraft.util.Hand;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Renders the offhand Dao blade in first person when wielding Zuko Dual Broadswords
 * with an empty offhand, providing authentic dual-wield visual immersion.
 */
@Mixin(HeldItemRenderer.class)
public abstract class MixinHeldItemRenderer {

    @Shadow
    private float equipProgressMainHand;

    @Shadow
    protected abstract void renderFirstPersonItem(
            AbstractClientPlayerEntity player, float tickDelta, float pitch,
            Hand hand, float swingProgress, ItemStack item, float equipProgress,
            MatrixStack matrices, VertexConsumerProvider vertexConsumers, int light
    );

    @Inject(
            method = "renderItem(FLnet/minecraft/client/util/math/MatrixStack;Lnet/minecraft/client/render/VertexConsumerProvider$Immediate;Lnet/minecraft/client/network/ClientPlayerEntity;I)V",
            at = @At("TAIL")
    )
    private void avatar$renderDualSwordsFirstPersonOffhand(
            float tickDelta, MatrixStack matrices, VertexConsumerProvider.Immediate vertexConsumers,
            ClientPlayerEntity player, int light, CallbackInfo ci
    ) {
        if (player.getMainHandStack().isOf(AvatarItems.DUAL_SWORDS) && player.getOffHandStack().isEmpty()) {
            float swing = player.getHandSwingProgress(tickDelta);
            float offhandSwing = (player.preferredHand == Hand.OFF_HAND) ? swing : (swing * 0.85f);
            float equip = Math.max(this.equipProgressMainHand, 0.90f);
            this.renderFirstPersonItem(
                    player, tickDelta, player.getPitch(tickDelta), Hand.OFF_HAND,
                    offhandSwing, player.getMainHandStack(), equip,
                    matrices, vertexConsumers, light
            );
        }
    }
}
