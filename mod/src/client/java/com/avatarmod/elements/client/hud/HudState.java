package com.avatarmod.elements.client.hud;

/**
 * Client-side mirror of the last S2CHudUpdate received from the server.
 * Updated on the render thread via SkillClientHandler.
 */
public final class HudState {

    private static int currentChi = 0;
    private static int maxChi     = 100;
    private static String activeCooldownSkillId = "";
    private static int cooldownTicksRemaining   = 0;

    // Smooth chi interpolation: lerp toward server value each frame
    private static float displayChi = 0f;

    public static void update(int chi, int max, String skillId, int cdTicks) {
        currentChi = chi;
        maxChi     = max > 0 ? max : 1;
        activeCooldownSkillId = skillId != null ? skillId : "";
        cooldownTicksRemaining = cdTicks;
    }

    /** Call once per render frame to advance the smooth chi bar. */
    public static void tickDisplay(float tickDelta) {
        float target = currentChi;
        displayChi += (target - displayChi) * Math.min(1f, 0.15f + tickDelta * 0.1f);
    }

    public static float getDisplayChiFraction() {
        return maxChi > 0 ? Math.max(0f, Math.min(1f, displayChi / maxChi)) : 0f;
    }

    public static int getCurrentChi()  { return currentChi; }
    public static int getMaxChi()      { return maxChi; }
    public static int getCooldownTicksRemaining() { return cooldownTicksRemaining; }
    public static String getActiveCooldownSkillId() { return activeCooldownSkillId; }
    public static boolean hasCooldown() {
        return cooldownTicksRemaining > 0 && !activeCooldownSkillId.isEmpty();
    }

    private HudState() {}
}
