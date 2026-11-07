package com.avatarmod.elements.client.hud;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.render.RenderTickCounter;
import net.minecraft.client.util.math.MatrixStack;

/**
 * Renders the element selection wheel when the ELEMENT_WHEEL key is held.
 * Layout: AIR=top, WATER=left, FIRE=right, EARTH=bottom.
 * Hovered element is determined by mouse cursor angle from screen center.
 * On key release, the hovered element is returned (caller sends C2SSetElement).
 */
public final class ElementWheelRenderer {

    // Element order matches ELEMENTS[] in ElementSlotMap
    private static final String[] WHEEL_ELEMENTS = {"AIR", "WATER", "FIRE", "EARTH"};
    // Degree ranges: AIR=315..45, WATER=45..135 (clockwise from top would be: top=AIR, right=FIRE, bottom=EARTH, left=WATER)
    // Actually use atan2: angle 0=right, 90=down, -90=up, ±180=left
    // Sectors: AIR = angle < -45 || angle > 135 (top), FIRE = -45..45 (right), EARTH = 45..135 (bottom), WATER = -(135..45) (left)

    private static final int[] COLORS = {
            0xFFAAAAAA, // AIR — light grey
            0xFF55AAFF, // WATER — blue
            0xFFFF5500, // FIRE — orange-red
            0xFF88AA44, // EARTH — green-brown
    };

    private static String hoveredElement = "FIRE";

    public static String getHovered() { return hoveredElement; }

    public static void render(DrawContext context, RenderTickCounter tickCounter) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null) return;

        int sw = client.getWindow().getScaledWidth();
        int sh = client.getWindow().getScaledHeight();
        int cx = sw / 2;
        int cy = sh / 2;

        // Determine hovered element from mouse position
        double mx = client.mouse.getX() * sw / client.getWindow().getWidth();
        double my = client.mouse.getY() * sh / client.getWindow().getHeight();
        double dx = mx - cx;
        double dy = my - cy;
        hoveredElement = angleToElement(dx, dy);

        int radius = 60;
        // Draw background overlay
        context.fill(cx - radius - 20, cy - radius - 20, cx + radius + 20, cy + radius + 20,
                0x88000000);

        // Draw 4 element labels
        int[][] positions = {
                {cx, cy - radius},      // AIR — top
                {cx - radius, cy},      // WATER — left
                {cx + radius, cy},      // FIRE — right
                {cx, cy + radius},      // EARTH — bottom
        };

        for (int i = 0; i < 4; i++) {
            String name = WHEEL_ELEMENTS[i];
            boolean hovered = name.equals(hoveredElement);
            int color = hovered ? 0xFFFFFFFF : COLORS[i];
            int x = positions[i][0] - client.textRenderer.getWidth(name) / 2;
            int y = positions[i][1] - 4;
            if (hovered) {
                // Highlight background
                context.fill(x - 4, y - 2, x + client.textRenderer.getWidth(name) + 4, y + 10,
                        COLORS[i] & 0x00FFFFFF | 0xAA000000);
            }
            context.drawText(client.textRenderer, name, x, y, color, true);
        }

        // Center label
        String centerText = "[" + hoveredElement + "]";
        context.drawCenteredTextWithShadow(client.textRenderer, centerText, cx, cy - 4, 0xFFFFFFFF);
    }

    private static String angleToElement(double dx, double dy) {
        if (Math.abs(dx) < 5 && Math.abs(dy) < 5) return hoveredElement; // dead zone
        double angle = Math.toDegrees(Math.atan2(dy, dx)); // -180..180, 0=right, 90=down
        if (angle >= -45 && angle < 45) return "FIRE";
        if (angle >= 45 && angle < 135) return "EARTH";
        if (angle >= 135 || angle < -135) return "WATER";
        return "AIR"; // -135..-45
    }

    private ElementWheelRenderer() {}
}
