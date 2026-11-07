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

    public static void register() {
        // Registration happens via KeyBindingHelper above; this method exists so
        // AvatarElementsClient can call it explicitly to trigger class loading.
    }

    private AvatarKeyBindings() {}
}
