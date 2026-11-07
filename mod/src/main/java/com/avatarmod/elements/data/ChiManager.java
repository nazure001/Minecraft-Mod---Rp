package com.avatarmod.elements.data;

/**
 * Chi pool logic: regen, spend, clamp, and flat modifiers.
 *
 * State lives in PlayerBendingData; ChiManager holds the rules.
 * Modifiers (buff/debuff) are additive flat values — T2+ will push/pop them
 * per effect. For T1-7 the modifier list is not yet wired to any effect system;
 * the API is here so callers don't need to change when effects arrive.
 */
public final class ChiManager {

    // Base regen constants (match CONTENT_SPEC defaults)
    public static final int BASE_MAX_CHI    = 100;
    public static final int BASE_REGEN_RATE = 1;    // chi per regen interval
    public static final int REGEN_INTERVAL  = 4;    // server ticks between regen pulses

    // Flat modifiers (additive) — pushed/popped by effects in T2+
    private int regenRateModifier = 0;   // extra chi per regen pulse
    private int maxChiModifier    = 0;   // extra max chi
    private float costMultiplier  = 1.0f; // multiplied into chi costs

    // --- regen ---

    /**
     * Called by PlayerBendingData.tick() every REGEN_INTERVAL ticks.
     * Returns the chi actually added (may be 0 if already at max).
     */
    public int computeRegenPulse(int currentChi, int maxChi) {
        int effective = Math.max(0, BASE_REGEN_RATE + regenRateModifier);
        int headroom  = effectiveMax(maxChi) - currentChi;
        return Math.max(0, Math.min(effective, headroom));
    }

    // --- spend ---

    /**
     * Returns the actual chi to deduct for a skill with the given base cost,
     * after applying the cost multiplier and clamping to [0, currentChi].
     * Returns -1 if the player cannot afford the cost (chi check for callers).
     */
    public int computeCost(int baseCost, int currentChi) {
        int scaled = Math.max(0, Math.round(baseCost * costMultiplier));
        return currentChi >= scaled ? scaled : -1;
    }

    // --- max ---

    public int effectiveMax(int baseMax) {
        return Math.max(1, baseMax + maxChiModifier);
    }

    // --- clamp ---

    /** Ensure chi stays within [0, effectiveMax]. */
    public int clamp(int chi, int baseMax) {
        return Math.max(0, Math.min(chi, effectiveMax(baseMax)));
    }

    // --- modifier API (T2+) ---

    public void addRegenRate(int delta) { regenRateModifier += delta; }
    public void addMaxChi(int delta)    { maxChiModifier    += delta; }
    public void setCostMultiplier(float m) { costMultiplier = Math.max(0f, m); }

    public int getRegenRateModifier()  { return regenRateModifier; }
    public int getMaxChiModifier()     { return maxChiModifier; }
    public float getCostMultiplier()   { return costMultiplier; }
}
