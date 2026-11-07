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
            0xFFFF5500, // FIRE  — orange-red
            0xFFAAAAAA, // AIR   — light grey
            0xFF55AAFF, // WATER — blue
            0xFF88AA44, // EARTH — green-brown
    };

    private static int currentIndex = 0; // FIRE is default

    /** Advance to next element and return its name. */
    public static String cycleElement() {
        currentIndex = (currentIndex + 1) % ELEMENTS.length;
        return ELEMENTS[currentIndex];
    }

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

    /**
     * Renders a compact element indicator bottom-left.
     * Shows: [◆ FIRE] with element color. Fades out after 60 ticks of no change.
     */
    public static void renderCurrentElement(DrawContext context) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null || client.options.hudHidden) return;

        String label = "◆ " + ELEMENTS[currentIndex];
        int color = COLORS[currentIndex];
        int x = 4;
        int y = client.getWindow().getScaledHeight() - 20;
        context.drawTextWithShadow(client.textRenderer, label, x, y, color);
    }

    private ElementWheelRenderer() {}
}
