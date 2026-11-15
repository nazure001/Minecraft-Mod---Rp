package com.avatarmod.elements.mixin;

import net.minecraft.entity.decoration.Brightness;
import net.minecraft.entity.decoration.DisplayEntity;
import net.minecraft.util.math.AffineTransformation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(DisplayEntity.class)
public interface DisplayEntityAccessor {

    @Invoker("setTransformation")
    void invokeSetTransformation(AffineTransformation transformation);

    @Invoker("setInterpolationDuration")
    void invokeSetInterpolationDuration(int duration);

    @Invoker("setStartInterpolation")
    void invokeSetStartInterpolation(int startInterpolation);

    @Invoker("setBrightness")
    void invokeSetBrightness(Brightness brightness);

    @Invoker("setBillboardMode")
    void invokeSetBillboardMode(DisplayEntity.BillboardMode mode);

    @Invoker("setViewRange")
    void invokeSetViewRange(float range);
}
