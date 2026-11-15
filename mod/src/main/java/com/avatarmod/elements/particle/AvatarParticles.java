package com.avatarmod.elements.particle;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

/**
 * Particle Type Registration for Avatar Elements.
 * Registers 11 micro-particles and 5 flipbook sequences.
 */
public final class AvatarParticles {
    public static final String MOD_ID = AvatarElementsMod.MOD_ID;

    public static final SimpleParticleType EMBER = register("ember");
    public static final SimpleParticleType FLAME_TONGUE = register("flame_tongue");
    public static final SimpleParticleType SMOKE_PUFF = register("smoke_puff");
    public static final SimpleParticleType GUST_CURL = register("gust_curl");
    public static final SimpleParticleType DROPLET = register("droplet");
    public static final SimpleParticleType SPLASH = register("splash");
    public static final SimpleParticleType FOAM = register("foam");
    public static final SimpleParticleType DUST = register("dust");
    public static final SimpleParticleType STONE_CHIP = register("stone_chip");
    public static final SimpleParticleType FROST = register("frost");
    public static final SimpleParticleType SPARK = register("spark");

    public static final SimpleParticleType CRACKLE = register("crackle");
    public static final SimpleParticleType FLAME_BURST = register("flame_burst");
    public static final SimpleParticleType IMPACT_FLASH = register("impact_flash");
    public static final SimpleParticleType SMALL_SPLASH = register("small_splash");
    public static final SimpleParticleType SMOKE_EXPANSION = register("smoke_expansion");

    private static SimpleParticleType register(String name) {
        return Registry.register(
                Registries.PARTICLE_TYPE,
                Identifier.of(MOD_ID, name),
                FabricParticleTypes.simple()
        );
    }

    public static void init() {
        // Triggers static initialization
    }

    private AvatarParticles() {}
}
