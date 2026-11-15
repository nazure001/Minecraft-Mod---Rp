package com.avatarmod.elements.client.particle;

import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.minecraft.client.particle.ParticleTextureSheet;
import net.minecraft.client.particle.SpriteBillboardParticle;
import net.minecraft.client.particle.SpriteProvider;
import net.minecraft.client.world.ClientWorld;
import net.minecraft.particle.SimpleParticleType;

/**
 * Animated flipbook particle that advances sprite frames over its lifetime.
 * Used for burst sequences like flame_burst, impact_flash, smoke_expansion, crackle, small_splash.
 */
public class AvatarAnimatedParticle extends SpriteBillboardParticle {
    private final SpriteProvider spriteProvider;
    private final boolean emissive;

    public AvatarAnimatedParticle(ClientWorld world, double x, double y, double z,
                                  double vx, double vy, double vz,
                                  SpriteProvider spriteProvider,
                                  int maxAge, float scale, boolean emissive) {
        super(world, x, y, z, vx, vy, vz);
        this.spriteProvider = spriteProvider;
        this.emissive = emissive;
        this.maxAge = Math.max(6, maxAge);
        this.scale = scale;
        this.collidesWithWorld = false;
        this.velocityX = vx;
        this.velocityY = vy;
        this.velocityZ = vz;
        this.setSpriteForAge(spriteProvider);
    }

    @Override
    public ParticleTextureSheet getType() {
        return ParticleTextureSheet.PARTICLE_SHEET_TRANSLUCENT;
    }

    @Override
    public int getBrightness(float tint) {
        return emissive ? 0xF000F0 : super.getBrightness(tint);
    }

    @Override
    public void tick() {
        this.prevPosX = this.x;
        this.prevPosY = this.y;
        this.prevPosZ = this.z;

        if (this.age++ >= this.maxAge) {
            this.markDead();
            return;
        }

        this.setSpriteForAge(this.spriteProvider);
        this.move(this.velocityX, this.velocityY, this.velocityZ);
        this.velocityX *= 0.92;
        this.velocityY *= 0.92;
        this.velocityZ *= 0.92;
    }

    public static ParticleFactoryRegistry.PendingParticleFactory<SimpleParticleType> createFactory(
            int maxAge, float scale, boolean emissive) {
        return spriteProvider -> (type, world, x, y, z, vx, vy, vz) ->
                new AvatarAnimatedParticle(world, x, y, z, vx, vy, vz, spriteProvider, maxAge, scale, emissive);
    }
}
