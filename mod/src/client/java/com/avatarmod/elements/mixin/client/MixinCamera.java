package com.avatarmod.elements.mixin.client;

import com.avatarmod.elements.client.camera.AvatarCameraDirector;
import net.minecraft.client.render.Camera;
import net.minecraft.entity.Entity;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.BlockView;
import org.joml.Quaternionf;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin to apply cinematic camera effects:
 * 1. Dutch Angle Camera Roll
 * 2. Directional Trauma Screenshake
 * 3. Raycast Anti-Clipping Orbit
 */
@Mixin(Camera.class)
public abstract class MixinCamera {

    @Shadow @Final private Quaternionf rotation;
    @Shadow private boolean thirdPerson;
    @Shadow protected abstract void setPos(double x, double y, double z);

    @Inject(method = "update", at = @At("TAIL"))
    private void avatar$onUpdateCamera(BlockView area, Entity focusedEntity, boolean thirdPerson, boolean inverseView, float tickDelta, CallbackInfo ci) {
        Camera camera = (Camera) (Object) this;
        Vec3d adjusted = AvatarCameraDirector.calculateCameraAdjustment(camera, focusedEntity, this.rotation, thirdPerson, tickDelta);
        if (adjusted != null) {
            this.setPos(adjusted.x, adjusted.y, adjusted.z);
        }
    }
}
