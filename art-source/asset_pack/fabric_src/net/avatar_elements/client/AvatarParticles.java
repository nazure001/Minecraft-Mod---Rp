package net.avatar_elements.client;

import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.client.particle.EndRodParticle;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

/**
 * Fabric 1.21.1 Particle Type & Client Factory Registration for Avatar Elements.
 * Registers all 11 micro-particles and 5 flipbook sequences.
 */
public final class AvatarParticles {
    public static final String MOD_ID = "avatar_elements";

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

    public static void registerClientFactories() {
        ParticleFactoryRegistry reg = ParticleFactoryRegistry.getInstance();
        reg.register(EMBER, EndRodParticle.Factory::new);
        reg.register(FLAME_TONGUE, EndRodParticle.Factory::new);
        reg.register(SMOKE_PUFF, EndRodParticle.Factory::new);
        reg.register(GUST_CURL, EndRodParticle.Factory::new);
        reg.register(DROPLET, EndRodParticle.Factory::new);
        reg.register(SPLASH, EndRodParticle.Factory::new);
        reg.register(FOAM, EndRodParticle.Factory::new);
        reg.register(DUST, EndRodParticle.Factory::new);
        reg.register(STONE_CHIP, EndRodParticle.Factory::new);
        reg.register(FROST, EndRodParticle.Factory::new);
        reg.register(SPARK, EndRodParticle.Factory::new);

        reg.register(CRACKLE, EndRodParticle.Factory::new);
        reg.register(FLAME_BURST, EndRodParticle.Factory::new);
        reg.register(IMPACT_FLASH, EndRodParticle.Factory::new);
        reg.register(SMALL_SPLASH, EndRodParticle.Factory::new);
        reg.register(SMOKE_EXPANSION, EndRodParticle.Factory::new);
    }
}
