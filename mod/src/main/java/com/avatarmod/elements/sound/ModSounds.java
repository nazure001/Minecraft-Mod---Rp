package com.avatarmod.elements.sound;

import com.avatarmod.elements.AvatarElementsMod;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.sound.SoundEvent;
import net.minecraft.util.Identifier;

public final class ModSounds {

    public static final Identifier FIRE_RELEASE_ID = Identifier.of(AvatarElementsMod.MOD_ID, "fire.release");
    public static final SoundEvent FIRE_RELEASE = SoundEvent.of(FIRE_RELEASE_ID);

    public static final Identifier FIRE_JAB_STRIKE_ID = Identifier.of(AvatarElementsMod.MOD_ID, "skill.fire.fire_jab.strike");
    public static final SoundEvent FIRE_JAB_STRIKE = SoundEvent.of(FIRE_JAB_STRIKE_ID);

    public static void init() {
        register();
        AvatarSounds.init();
    }

    public static void register() {
        Registry.register(Registries.SOUND_EVENT, FIRE_RELEASE_ID, FIRE_RELEASE);
        Registry.register(Registries.SOUND_EVENT, FIRE_JAB_STRIKE_ID, FIRE_JAB_STRIKE);
    }

    private ModSounds() {}
}
