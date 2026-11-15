package com.avatarmod.elements.client.particle;

import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.minecraft.client.particle.ParticleTextureSheet;
import net.minecraft.client.particle.SpriteBillboardParticle;
import net.minecraft.client.particle.SpriteProvider;
import net.minecraft.client.world.ClientWorld;
import net.minecraft.particle.SimpleParticleType;

/**
 * Single-sprite custom particle with smooth opacity fade.
 * Used for micro-particles like flame_tongue, ember, gust_curl, droplet, splash, foam, dust, stone_chip, frost, spark.
 */
public class AvatarSpriteParticle extends SpriteBillboardParticle {
    private final boolean emissive;

    public AvatarSpriteParticle(ClientWorld world, double x, double y, double z,
                                double vx, double vy, double vz,
                                SpriteProvider spriteProvider,
                                int maxAge, float scale, boolean emissive) {
        super(world, x, y, z, vx, vy, vz);
        this.emissive = emissive;
        this.maxAge = Math.max(4, maxAge);
        this.scale = scale;
        this.collidesWithWorld = false;
        this.velocityX = vx;
        this.velocityY = vy;
        this.velocityZ = vz;
        this.setSprite(spriteProvider);
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

        // Smooth quadratic fade out
        float progress = (float) this.age / (float) this.maxAge;
        this.alpha = Math.max(0.0f, 1.0f - progress * progress);

        this.move(this.velocityX, this.velocityY, this.velocityZ);
        this.velocityX *= 0.90;
        this.velocityY *= 0.90;
        this.velocityZ *= 0.90;
    }

    public static ParticleFactoryRegistry.PendingParticleFactory<SimpleParticleType> createFactory(
            int maxAge, float scale, boolean emissive) {
        return spriteProvider -> (type, world, x, y, z, vx, vy, vz) ->
                new AvatarSpriteParticle(world, x, y, z, vx, vy, vz, spriteProvider, maxAge, scale, emissive);
    }
}
