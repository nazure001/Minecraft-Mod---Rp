package com.avatarmod.elements.particle;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

/**
 * Particle Type Registration for Avatar Elements.
 * Registers both classic micro-particles and V3 high-fidelity 16-frame/4-frame animated VFX flipbooks.
 */
public final class AvatarParticles {
    public static final String MOD_ID = AvatarElementsMod.MOD_ID;

    // --- Legacy Micro-Particles & Sprites ---
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

    // --- Legacy Flipbook Sequences ---
    public static final SimpleParticleType CRACKLE = register("crackle");
    public static final SimpleParticleType FLAME_BURST = register("flame_burst");
    public static final SimpleParticleType IMPACT_FLASH = register("impact_flash");
    public static final SimpleParticleType SMALL_SPLASH = register("small_splash");
    public static final SimpleParticleType SMOKE_EXPANSION = register("smoke_expansion");

    // --- V3 Production High-Fidelity Animated Flipbooks ---
    // Fire & Sub-Elements
    public static final SimpleParticleType FIRE_ARC_SLASH = register("fire_arc_slash");
    public static final SimpleParticleType FIRE_COMET = register("fire_comet");
    public static final SimpleParticleType BLUE_FLAME = register("blue_flame");
    public static final SimpleParticleType FIRE_EMBER = register("fire_ember");
    public static final SimpleParticleType FIRE_SHOCKWAVE = register("fire_shockwave");
    public static final SimpleParticleType COMBUSTION_CHARGE = register("combustion_charge");
    public static final SimpleParticleType OZAI_METEOR = register("ozai_meteor");
    public static final SimpleParticleType LAVA_SPARK = register("lava_spark");
    public static final SimpleParticleType LAVA_SPLASH = register("lava_splash");

    // Air & Traversal
    public static final SimpleParticleType AIR_RING = register("air_ring");
    public static final SimpleParticleType AIR_GUST_SWIRL = register("air_gust_swirl");
    public static final SimpleParticleType AIR_PRESSURE_BURST = register("air_pressure_burst");
    public static final SimpleParticleType AIR_TORNADO_WISP = register("air_tornado_wisp");
    public static final SimpleParticleType AIR_FLIGHT_TRAIL = register("air_flight_trail");

    // Water, Ice & Healing
    public static final SimpleParticleType WATER_WHIP_SPLASH = register("water_whip_splash");
    public static final SimpleParticleType WATER_DROPLET = register("water_droplet");
    public static final SimpleParticleType WATER_HEALING_AURA = register("water_healing_aura");
    public static final SimpleParticleType ICE_BURST = register("ice_burst");
    public static final SimpleParticleType ICE_SHARD = register("ice_shard");

    // Earth & Metal
    public static final SimpleParticleType EARTH_SEISMIC_WAVE = register("earth_seismic_wave");
    public static final SimpleParticleType EARTH_STOMP_DUST = register("earth_stomp_dust");
    public static final SimpleParticleType EARTH_CHUNK = register("earth_chunk");
    public static final SimpleParticleType METAL_SPARK = register("metal_spark");

    // Lightning
    public static final SimpleParticleType LIGHTNING_ARC = register("lightning_arc");
    public static final SimpleParticleType LIGHTNING_BRANCH = register("lightning_branch");

    // Chi, Spirit & Cosmic
    public static final SimpleParticleType BLOOD_CHI_FILAMENT = register("blood_chi_filament");
    public static final SimpleParticleType AVATAR_CHI = register("avatar_chi");
    public static final SimpleParticleType AVATAR_STATE_CHI = register("avatar_state_chi");
    public static final SimpleParticleType HEALING_MOTE = register("healing_mote");
    public static final SimpleParticleType SPIRIT_MOTE = register("spirit_mote");
    public static final SimpleParticleType VAATU_VOID_ENERGY = register("vaatu_void_energy");
    public static final SimpleParticleType PLANT_VINE_CHI = register("plant_vine_chi");

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
