package com.avatarmod.elements.client.input;

import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import org.lwjgl.glfw.GLFW;

public final class AvatarKeyBindings {

    public static final KeyBinding TEST_ACTION = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.test_action",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_R,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_FIRE_JAB = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_fire_jab",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_G,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_FLAME_SWEEP = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_flame_sweep",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_Z,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_FIRE_JET = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_fire_jet",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_J,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_FIRE_GUARD = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_fire_guard",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_K,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_AIR_STAFF = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_air_staff",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_H,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_AIR_VORTEX = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_air_vortex",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_V,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_WATER_WHIP = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_water_whip",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_C,
                    "category.avatar_elements.general"
            )
    );

    public static final KeyBinding SKILL_EARTH_BOULDER = KeyBindingHelper.registerKeyBinding(
            new KeyBinding(
                    "key.avatar_elements.skill_earth_boulder",
                    InputUtil.Type.KEYSYM,
                    GLFW.GLFW_KEY_B,
                    "category.avatar_elements.general"
            )
    );

    public static void register() {
        // Registration happens via KeyBindingHelper above; this method exists so
        // AvatarElementsClient can call it explicitly to trigger class loading.
    }

    private AvatarKeyBindings() {}
}
