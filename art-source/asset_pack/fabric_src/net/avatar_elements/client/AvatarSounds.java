package net.avatar_elements.client;

import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.sound.SoundEvent;
import net.minecraft.util.Identifier;

/**
 * Fabric 1.21.1 SoundEvent Registry matching assets/avatar_elements/sounds.json.
 */
public final class AvatarSounds {
    public static final String MOD_ID = "avatar_elements";

    public static final SoundEvent FIRE_JAB_CAST = register("fire.fire_jab_cast");
    public static final SoundEvent FLAME_SWEEP_SLASH = register("fire.flame_sweep_slash");
    public static final SoundEvent FIRE_JET_DASH = register("fire.fire_jet_dash");
    public static final SoundEvent FIRE_BLAST_CHARGE_START = register("fire.fire_blast_charge_start");
    public static final SoundEvent FIRE_BLAST_CHARGE_LOOP = register("fire.fire_blast_charge_loop");
    public static final SoundEvent FIRE_BLAST_RELEASE = register("fire.fire_blast_release");
    public static final SoundEvent FIRE_BLAST_IMPACT = register("fire.fire_blast_impact");
    public static final SoundEvent FIRE_CANCEL_FIZZLE = register("fire.fire_cancel_fizzle");
    public static final SoundEvent LIGHTNING_CRACKLE = register("lightning.lightning_crackle");
    public static final SoundEvent AIR_STAFF_SWING = register("air.air_staff_swing");
    public static final SoundEvent AIR_VORTEX_LOOP = register("air.air_vortex_loop");
    public static final SoundEvent WATER_WHIP_LASH = register("water.water_whip_lash");
    public static final SoundEvent WATER_SPLASH_IMPACT = register("water.water_splash_impact");
    public static final SoundEvent EARTH_BOULDER_LAUNCH = register("earth.earth_boulder_launch");
    public static final SoundEvent EARTH_IMPACT_HEAVY = register("earth.earth_impact_heavy");
    public static final SoundEvent UI_SCROLL_OPEN = register("ui.ui_scroll_open");
    public static final SoundEvent UI_BUTTON_CLICK = register("ui.ui_button_click");

    private static SoundEvent register(String path) {
        Identifier id = Identifier.of(MOD_ID, path);
        return Registry.register(Registries.SOUND_EVENT, id, SoundEvent.of(id));
    }

    public static void init() {}
}
