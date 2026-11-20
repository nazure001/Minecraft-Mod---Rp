package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.item.AvatarItems;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.render.entity.feature.FeatureRenderer;
import net.minecraft.client.render.entity.feature.FeatureRendererContext;
import net.minecraft.client.render.entity.feature.HeldItemFeatureRenderer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.ModelWithArms;
import net.minecraft.client.render.model.json.ModelTransformationMode;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.entity.LivingEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.util.Arm;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Renders the matching secondary blade in the offhand when holding
 * Zuko Dual Dao Broadswords (AvatarItems.DUAL_SWORDS) in the main hand.
 */
@Mixin(HeldItemFeatureRenderer.class)
public abstract class MixinHeldItemFeatureRenderer<T extends LivingEntity, M extends EntityModel<T> & ModelWithArms>
        extends FeatureRenderer<T, M> {

    public MixinHeldItemFeatureRenderer(FeatureRendererContext<T, M> context) {
        super(context);
    }

    @Shadow
    protected abstract void renderItem(LivingEntity entity, ItemStack stack,
                                       ModelTransformationMode transformationMode,
                                       Arm arm, MatrixStack matrices,
                                       VertexConsumerProvider vertexConsumers, int light);

    @Inject(
            method = "render(Lnet/minecraft/client/util/math/MatrixStack;Lnet/minecraft/client/render/VertexConsumerProvider;ILnet/minecraft/entity/LivingEntity;FFFFFF)V",
            at = @At("TAIL")
    )
    private void avatar$renderDualSwordsOffhand(
            MatrixStack matrixStack, VertexConsumerProvider vertexConsumerProvider, int light,
            T livingEntity, float f, float g, float h, float j, float k, float l,
            CallbackInfo ci) {

        if (livingEntity.getOffHandStack().isEmpty() && livingEntity.getMainHandStack().isOf(AvatarItems.DUAL_SWORDS)) {
            Arm offArm = (livingEntity.getMainArm() == Arm.RIGHT) ? Arm.LEFT : Arm.RIGHT;
            ModelTransformationMode mode = (offArm == Arm.LEFT)
                    ? ModelTransformationMode.THIRD_PERSON_LEFT_HAND
                    : ModelTransformationMode.THIRD_PERSON_RIGHT_HAND;

            matrixStack.push();
            if (this.getContextModel().child) {
                matrixStack.translate(0.0f, 0.75f, 0.0f);
                matrixStack.scale(0.5f, 0.5f, 0.5f);
            }
            this.renderItem(livingEntity, livingEntity.getMainHandStack(), mode, offArm, matrixStack, vertexConsumerProvider, light);
            matrixStack.pop();
        }
    }
}
