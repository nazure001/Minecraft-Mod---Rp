package com.avatarmod.elements.client.particle;

import com.avatarmod.elements.particle.AvatarParticles;
import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;

/**
 * Client particle factory registration.
 * Registers custom high-fidelity flipbook and micro-particles from avatar_elements asset pack.
 */
public final class AvatarClientParticles {

    public static void registerClientFactories() {
        ParticleFactoryRegistry reg = ParticleFactoryRegistry.getInstance();

        // --- Legacy Animated Flipbook Sequences ---
        reg.register(AvatarParticles.FLAME_BURST, AvatarAnimatedParticle.createFactory(12, 0.65f, true));
        reg.register(AvatarParticles.IMPACT_FLASH, AvatarAnimatedParticle.createFactory(8, 0.40f, true));
        reg.register(AvatarParticles.SMOKE_EXPANSION, AvatarAnimatedParticle.createFactory(16, 0.70f, false));
        reg.register(AvatarParticles.SMALL_SPLASH, AvatarAnimatedParticle.createFactory(10, 0.45f, false));
        reg.register(AvatarParticles.CRACKLE, AvatarAnimatedParticle.createFactory(8, 0.50f, true));

        // --- Legacy Micro-particles & Sprites ---
        reg.register(AvatarParticles.FLAME_TONGUE, AvatarSpriteParticle.createFactory(10, 0.45f, true));
        reg.register(AvatarParticles.EMBER, AvatarSpriteParticle.createFactory(16, 0.25f, true));
        reg.register(AvatarParticles.SMOKE_PUFF, AvatarSpriteParticle.createFactory(14, 0.40f, false));
        reg.register(AvatarParticles.GUST_CURL, AvatarSpriteParticle.createFactory(12, 0.55f, false));
        reg.register(AvatarParticles.DROPLET, AvatarSpriteParticle.createFactory(12, 0.30f, false));
        reg.register(AvatarParticles.SPLASH, AvatarSpriteParticle.createFactory(10, 0.40f, false));
        reg.register(AvatarParticles.FOAM, AvatarSpriteParticle.createFactory(14, 0.35f, false));
        reg.register(AvatarParticles.DUST, AvatarSpriteParticle.createFactory(16, 0.40f, false));
        reg.register(AvatarParticles.STONE_CHIP, AvatarSpriteParticle.createFactory(12, 0.30f, false));
        reg.register(AvatarParticles.FROST, AvatarSpriteParticle.createFactory(14, 0.35f, true));
        reg.register(AvatarParticles.SPARK, AvatarSpriteParticle.createFactory(8, 0.30f, true));

        // --- V3 Production High-Fidelity Animated Flipbooks ---
        // Fire & Sub-Elements
        reg.register(AvatarParticles.FIRE_ARC_SLASH, AvatarAnimatedParticle.createFactory(10, 0.85f, true));
        reg.register(AvatarParticles.FIRE_COMET, AvatarAnimatedParticle.createFactory(12, 0.90f, true));
        reg.register(AvatarParticles.BLUE_FLAME, AvatarAnimatedParticle.createFactory(14, 0.70f, true));
        reg.register(AvatarParticles.FIRE_EMBER, AvatarAnimatedParticle.createFactory(16, 0.35f, true));
        reg.register(AvatarParticles.FIRE_SHOCKWAVE, AvatarAnimatedParticle.createFactory(12, 1.20f, true));
        reg.register(AvatarParticles.COMBUSTION_CHARGE, AvatarAnimatedParticle.createFactory(16, 0.75f, true));
        reg.register(AvatarParticles.OZAI_METEOR, AvatarAnimatedParticle.createFactory(16, 1.40f, true));
        reg.register(AvatarParticles.LAVA_SPARK, AvatarAnimatedParticle.createFactory(12, 0.40f, true));
        reg.register(AvatarParticles.LAVA_SPLASH, AvatarAnimatedParticle.createFactory(12, 0.60f, true));

        // Air & Traversal
        reg.register(AvatarParticles.AIR_RING, AvatarAnimatedParticle.createFactory(12, 1.00f, false));
        reg.register(AvatarParticles.AIR_GUST_SWIRL, AvatarAnimatedParticle.createFactory(12, 0.75f, false));
        reg.register(AvatarParticles.AIR_PRESSURE_BURST, AvatarAnimatedParticle.createFactory(10, 1.10f, false));
        reg.register(AvatarParticles.AIR_TORNADO_WISP, AvatarAnimatedParticle.createFactory(16, 0.80f, false));
        reg.register(AvatarParticles.AIR_FLIGHT_TRAIL, AvatarAnimatedParticle.createFactory(12, 0.60f, false));

        // Water, Ice & Healing
        reg.register(AvatarParticles.WATER_WHIP_SPLASH, AvatarAnimatedParticle.createFactory(12, 0.80f, false));
        reg.register(AvatarParticles.WATER_DROPLET, AvatarAnimatedParticle.createFactory(14, 0.40f, false));
        reg.register(AvatarParticles.WATER_HEALING_AURA, AvatarAnimatedParticle.createFactory(18, 0.65f, true));
        reg.register(AvatarParticles.ICE_BURST, AvatarAnimatedParticle.createFactory(10, 0.90f, true));
        reg.register(AvatarParticles.ICE_SHARD, AvatarAnimatedParticle.createFactory(12, 0.60f, false));

        // Earth & Metal
        reg.register(AvatarParticles.EARTH_SEISMIC_WAVE, AvatarAnimatedParticle.createFactory(14, 1.20f, false));
        reg.register(AvatarParticles.EARTH_STOMP_DUST, AvatarAnimatedParticle.createFactory(16, 0.90f, false));
        reg.register(AvatarParticles.EARTH_CHUNK, AvatarAnimatedParticle.createFactory(14, 0.65f, false));
        reg.register(AvatarParticles.METAL_SPARK, AvatarAnimatedParticle.createFactory(8, 0.45f, true));

        // Lightning
        reg.register(AvatarParticles.LIGHTNING_ARC, AvatarAnimatedParticle.createFactory(8, 0.75f, true));
        reg.register(AvatarParticles.LIGHTNING_BRANCH, AvatarAnimatedParticle.createFactory(10, 0.95f, true));

        // Chi, Spirit & Cosmic
        reg.register(AvatarParticles.BLOOD_CHI_FILAMENT, AvatarAnimatedParticle.createFactory(14, 0.60f, true));
        reg.register(AvatarParticles.AVATAR_CHI, AvatarAnimatedParticle.createFactory(16, 0.70f, true));
        reg.register(AvatarParticles.AVATAR_STATE_CHI, AvatarAnimatedParticle.createFactory(20, 0.90f, true));
        reg.register(AvatarParticles.HEALING_MOTE, AvatarAnimatedParticle.createFactory(16, 0.50f, true));
        reg.register(AvatarParticles.SPIRIT_MOTE, AvatarAnimatedParticle.createFactory(18, 0.55f, true));
        reg.register(AvatarParticles.VAATU_VOID_ENERGY, AvatarAnimatedParticle.createFactory(16, 0.85f, true));
        reg.register(AvatarParticles.PLANT_VINE_CHI, AvatarAnimatedParticle.createFactory(14, 0.60f, false));
    }

    private AvatarClientParticles() {}
}
