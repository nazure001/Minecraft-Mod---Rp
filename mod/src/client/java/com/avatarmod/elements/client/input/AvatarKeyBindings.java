package com.avatarmod.elements.client.input;

import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import org.lwjgl.glfw.GLFW;

public final class AvatarKeyBindings {

    // --- Skill slots (Z/X/C/V) ---
    public static final KeyBinding SLOT_1 = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.avatar_elements.slot_1", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_Z,
            "category.avatar_elements.general"));

    public static final KeyBinding SLOT_2 = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.avatar_elements.slot_2", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_X,
            "category.avatar_elements.general"));

    public static final KeyBinding SLOT_3 = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.avatar_elements.slot_3", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_C,
            "category.avatar_elements.general"));

    public static final KeyBinding SLOT_4 = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.avatar_elements.slot_4", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_V,
            "category.avatar_elements.general"));

    // --- Element wheel (hold R) ---
    public static final KeyBinding ELEMENT_WHEEL = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.avatar_elements.element_wheel", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_R,
            "category.avatar_elements.general"));

    public static void register() {
        // Registration happens via KeyBindingHelper above.
    }

    private AvatarKeyBindings() {}
}
