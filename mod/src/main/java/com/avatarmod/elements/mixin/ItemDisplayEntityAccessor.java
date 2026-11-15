package com.avatarmod.elements.mixin;

import net.minecraft.client.render.model.json.ModelTransformationMode;
import net.minecraft.entity.decoration.DisplayEntity;
import net.minecraft.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(DisplayEntity.ItemDisplayEntity.class)
public interface ItemDisplayEntityAccessor {

    @Invoker("setItemStack")
    void invokeSetItemStack(ItemStack itemStack);

    @Invoker("setTransformationMode")
    void invokeSetTransformationMode(ModelTransformationMode mode);
}
