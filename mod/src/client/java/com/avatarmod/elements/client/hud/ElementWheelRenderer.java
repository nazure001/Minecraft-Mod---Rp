package com.avatarmod.elements.client.hud;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.render.RenderTickCounter;

/**
 * Element selector: press R to cycle FIRE→AIR→WATER→EARTH→FIRE.
 * Renders current element as a small overlay in the bottom-left corner.
 * No mouse wheel tracking — Minecraft captures mouse during gameplay.
 */
public final class ElementWheelRenderer {

    private static final String[] ELEMENTS = {"FIRE", "AIR", "WATER", "EARTH"};
    private static final int[] COLORS = {
            0xFFBD4B36, // FIRE
            0xFFBE8B35, // AIR
            0xFF3D82A8, // WATER
            0xFF687E3C, // EARTH
    };

    private static int currentIndex = 0; // FIRE is default

    /** Set active element directly (e.g. on server sync). */
    public static void setElement(String element) {
        for (int i = 0; i < ELEMENTS.length; i++) {
            if (ELEMENTS[i].equals(element)) {
                currentIndex = i;
                return;
            }
        }
    }

    public static String getCurrentElement() {
        return ELEMENTS[currentIndex];
    }

    public static int getCurrentColor() {
        return COLORS[currentIndex];
    }

    /**
     * Renders the locally selected element as a compact parchment badge.
     */
    public static void renderCurrentElement(DrawContext context) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null || client.options.hudHidden) return;

        String label = "◆ " + ELEMENTS[currentIndex];
        int color = COLORS[currentIndex];
        int x = 6;
        int y = client.getWindow().getScaledHeight() - 20;
        int labelWidth = client.textRenderer.getWidth(label);
        context.fill(x, y - 3, x + labelWidth + 10, y + 11, 0xFF4A3423);
        context.fill(x + 1, y - 2, x + labelWidth + 9, y + 10, 0xE8D8C39A);
        context.fill(x + 2, y - 1, x + 4, y + 9, color);
        context.drawTextWithShadow(client.textRenderer, label, x + 7, y, 0xFF38291E);
    }

    private ElementWheelRenderer() {}
}
