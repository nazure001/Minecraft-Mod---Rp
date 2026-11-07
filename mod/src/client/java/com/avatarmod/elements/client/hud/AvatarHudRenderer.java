package com.avatarmod.elements.client.hud;

import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.render.RenderTickCounter;

/**
 * Renders the Avatar HUD overlay:
 *   - Chi bar: horizontal bar above hotbar, air-blue fill
 *   - Cooldown text: skill id + ticks remaining, shown when active
 *
 * Layout is intentionally simple for T1-8; visual polish in T2+.
 */
public final class AvatarHudRenderer {

    // Chi bar dimensions and position (relative to screen bottom-center)
    private static final int BAR_WIDTH  = 80;
    private static final int BAR_HEIGHT = 6;
    private static final int BAR_Y_OFFSET = 32; // pixels above bottom edge

    // Colors (ARGB)
    private static final int COLOR_BG       = 0xAA000000;
    private static final int COLOR_CHI_FILL = 0xFF5BB8E8; // air blue
    private static final int COLOR_CHI_LOW  = 0xFFE85B5B; // red when < 20%
    private static final int COLOR_BORDER   = 0xFF224466;
    private static final int COLOR_CD_TEXT  = 0xFFFFCC44;

    public static void register() {
        HudRenderCallback.EVENT.register(AvatarHudRenderer::render);
    }

    private static void render(DrawContext ctx, RenderTickCounter ticker) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null || client.options.hudHidden) return;
        // Don't render in F3 screen or inventory
        if (client.currentScreen != null) return;

        HudState.tickDisplay(ticker.getTickDelta(false));

        int screenW = ctx.getScaledWindowWidth();
        int screenH = ctx.getScaledWindowHeight();

        int barX = (screenW - BAR_WIDTH) / 2;
        int barY = screenH - BAR_Y_OFFSET - BAR_HEIGHT;

        drawChiBar(ctx, barX, barY);

        if (HudState.hasCooldown()) {
            drawCooldown(ctx, screenW, barY - 10);
        }
    }

    private static void drawChiBar(DrawContext ctx, int x, int y) {
        // Background
        ctx.fill(x - 1, y - 1, x + BAR_WIDTH + 1, y + BAR_HEIGHT + 1, COLOR_BORDER);
        ctx.fill(x, y, x + BAR_WIDTH, y + BAR_HEIGHT, COLOR_BG);

        // Fill
        float fraction = HudState.getDisplayChiFraction();
        int fillW = Math.round(BAR_WIDTH * fraction);
        if (fillW > 0) {
            int color = fraction < 0.2f ? COLOR_CHI_LOW : COLOR_CHI_FILL;
            ctx.fill(x, y, x + fillW, y + BAR_HEIGHT, color);
        }

        // Chi text (chi/max), right-aligned above bar
        String chiText = HudState.getCurrentChi() + "/" + HudState.getMaxChi();
        int textX = x + BAR_WIDTH - MinecraftClient.getInstance().textRenderer.getWidth(chiText);
        ctx.drawText(MinecraftClient.getInstance().textRenderer,
                chiText, textX, y - 9, 0xFFCCDDEE, true);
    }

    private static void drawCooldown(DrawContext ctx, int screenW, int y) {
        String raw = HudState.getActiveCooldownSkillId();
        // Show only the last segment of the skill id (e.g. "fire_jab" from "avatar:fire_jab")
        String name = raw.contains(":") ? raw.substring(raw.indexOf(':') + 1) : raw;
        float seconds = HudState.getCooldownTicksRemaining() / 20f;
        String text = name + " §r§7(" + String.format("%.1fs", seconds) + ")";

        int textW = MinecraftClient.getInstance().textRenderer.getWidth(text);
        ctx.drawText(MinecraftClient.getInstance().textRenderer,
                text, (screenW - textW) / 2, y, COLOR_CD_TEXT, true);
    }

    private AvatarHudRenderer() {}
}
