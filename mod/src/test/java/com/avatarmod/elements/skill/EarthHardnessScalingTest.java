package com.avatarmod.elements.skill;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class EarthHardnessScalingTest {

    @ParameterizedTest(name = "Hardness {0} gives damage bonus {1}")
    @CsvSource({
            "0.5, 0.75",    // Dirt / Mud
            "0.8, 1.20",    // Sandstone
            "1.25, 1.875",  // Terracotta
            "1.5, 2.25",    // Stone
            "2.0, 3.00",    // Cobblestone
            "3.0, 4.50",    // Deepslate
            "4.5, 6.75",    // Reinforced Deepslate / Iron Ore
            "5.0, 7.50",    // Iron Block
            "10.0, 15.00",  // Crying Obsidian cap reached
            "50.0, 15.00",  // Obsidian capped at 15.0
            "-1.0, 7.50"    // Bedrock (unbreakable fallback 5.0 * 1.5)
    })
    @DisplayName("Verify Earth Hardness Damage bonus matches mathematical curve")
    void testHardnessDamageBonus(float hardness, float expectedBonus) {
        float actualBonus = ElementalInteractions.computeHardnessDamageBonus(hardness);
        assertEquals(expectedBonus, actualBonus, 1e-4);
    }

    @Test
    @DisplayName("Verify scaled damage formula: Base + Bonus")
    void testTotalScaledDamage() {
        float baseDamage = 5.0f;
        // Dirt
        assertEquals(5.75f, baseDamage + ElementalInteractions.computeHardnessDamageBonus(0.5f), 1e-4);
        // Stone
        assertEquals(7.25f, baseDamage + ElementalInteractions.computeHardnessDamageBonus(1.5f), 1e-4);
        // Deepslate
        assertEquals(9.50f, baseDamage + ElementalInteractions.computeHardnessDamageBonus(3.0f), 1e-4);
        // Obsidian capped
        assertEquals(20.00f, baseDamage + ElementalInteractions.computeHardnessDamageBonus(50.0f), 1e-4);
    }
}
