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

        // --- Animated Flipbook Sequences ---
        reg.register(AvatarParticles.FLAME_BURST, AvatarAnimatedParticle.createFactory(12, 0.65f, true));
        reg.register(AvatarParticles.IMPACT_FLASH, AvatarAnimatedParticle.createFactory(8, 0.40f, true));
        reg.register(AvatarParticles.SMOKE_EXPANSION, AvatarAnimatedParticle.createFactory(16, 0.70f, false));
        reg.register(AvatarParticles.SMALL_SPLASH, AvatarAnimatedParticle.createFactory(10, 0.45f, false));
        reg.register(AvatarParticles.CRACKLE, AvatarAnimatedParticle.createFactory(8, 0.50f, true));

        // --- Micro-particles & Sprites ---
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
    }

    private AvatarClientParticles() {}
}
