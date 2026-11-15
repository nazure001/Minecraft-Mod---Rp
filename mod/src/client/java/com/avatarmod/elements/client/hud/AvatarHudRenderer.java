package com.avatarmod.elements.client.hud;

import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.render.RenderTickCounter;

import java.util.Locale;

/**
 * Renders a compact parchment-style overlay above the vanilla hotbar.
 */
public final class AvatarHudRenderer {

    private static final int PANEL_WIDTH = 96;
    private static final int PANEL_HEIGHT = 18;
    private static final int BAR_INSET = 6;
    private static final int BAR_HEIGHT = 4;

    private static final int COLOR_PARCHMENT = 0xE8D8C39A;
    private static final int COLOR_INK = 0xFF38291E;
    private static final int COLOR_FRAME = 0xFF4A3423;
    private static final int COLOR_BAR_BG = 0xFF755E45;
    private static final int COLOR_CHI_LOW = 0xFFB63F36;

    public static void register() {
        HudRenderCallback.EVENT.register(AvatarHudRenderer::render);
    }

    private static void render(DrawContext ctx, RenderTickCounter ticker) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null || client.options.hudHidden) return;
        // Don't render in F3 screen or inventory
        if (client.currentScreen != null) return;

        HudState.tickDisplay(ticker.getTickDelta(false));

        int screenH = ctx.getScaledWindowHeight();

        ElementWheelRenderer.renderCurrentElement(ctx);

        // Position HUD cleanly in bottom-left above element badge to keep center screen unobstructed
        int panelX = 6;
        int panelY = screenH - 42;
        int accent = ElementWheelRenderer.getCurrentColor();

        drawChiPanel(ctx, panelX, panelY, accent);

        if (HudState.hasCooldown()) {
            drawCooldown(ctx, panelX, panelY - 14, accent);
        }
    }

    private static void drawChiPanel(DrawContext ctx, int x, int y, int accent) {
        MinecraftClient client = MinecraftClient.getInstance();
        int barWidth = PANEL_WIDTH - BAR_INSET * 2;

        ctx.fill(x, y, x + PANEL_WIDTH, y + PANEL_HEIGHT, COLOR_FRAME);
        ctx.fill(x + 1, y + 1, x + PANEL_WIDTH - 1, y + PANEL_HEIGHT - 1, COLOR_PARCHMENT);
        ctx.fill(x + 2, y + 2, x + 3, y + PANEL_HEIGHT - 2, accent);

        String chiText = "Chi " + HudState.getCurrentChi() + "/" + HudState.getMaxChi();
        ctx.drawTextWithShadow(client.textRenderer, chiText, x + 6, y + 3, COLOR_INK);

        int barX = x + BAR_INSET;
        int barY = y + PANEL_HEIGHT - BAR_HEIGHT - 3;
        ctx.fill(barX, barY, barX + barWidth, barY + BAR_HEIGHT, COLOR_BAR_BG);
        float fraction = HudState.getDisplayChiFraction();
        int fillW = Math.round(barWidth * fraction);
        if (fillW > 0) {
            int color = fraction < 0.2f ? COLOR_CHI_LOW : accent;
            ctx.fill(barX, barY, barX + fillW, barY + BAR_HEIGHT, color);
        }
    }

    private static void drawCooldown(DrawContext ctx, int x, int y, int accent) {
        MinecraftClient client = MinecraftClient.getInstance();
        String raw = HudState.getActiveCooldownSkillId();
        String name = raw.contains(":") ? raw.substring(raw.indexOf(':') + 1) : raw;
        name = name.replace('_', ' ');
        float seconds = HudState.getCooldownTicksRemaining() / 20f;
        String text = name + " · " + String.format(Locale.ROOT, "%.1fs", seconds);

        int textW = client.textRenderer.getWidth(text);
        int panelWidth = textW + 10;
        ctx.fill(x, y, x + panelWidth, y + 11, COLOR_FRAME);
        ctx.fill(x + 1, y + 1, x + panelWidth - 1, y + 10, COLOR_PARCHMENT);
        ctx.fill(x + 2, y + 2, x + 3, y + 9, accent);
        ctx.drawTextWithShadow(client.textRenderer, text, x + 6, y + 2, COLOR_INK);
    }

    private AvatarHudRenderer() {}
}
