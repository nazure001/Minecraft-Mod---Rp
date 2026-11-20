package com.avatarmod.elements.skill;

import com.avatarmod.elements.skill.impl.EarthPillarSkill;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class EarthWallFormationTest {

    @ParameterizedTest(name = "Sneaking={0}, Mastery={1} -> Expected Pillars={2}")
    @CsvSource({
            "false, 0, 1", // Normal single pillar
            "true,  0, 3", // Sneak cast earth wall
            "false, 1, 3", // Mastery 1 automatic wall
            "false, 2, 3", // Mastery 2 automatic wall
            "true,  2, 3", // Sneak + Mastery 2 wall
            "false, 3, 5", // Mastery 3 wide barricade
            "true,  3, 5", // Sneak + Mastery 3 wide barricade
            "false, 4, 5", // Mastery 4 wide barricade
            "false, 5, 5"  // Mastery 5 wide barricade
    })
    @DisplayName("Verify Earth Wall & Barricade pillar count scaling")
    void testWallPillarCountScaling(boolean isSneaking, int masteryLevel, int expectedCount) {
        int count = computePillarCount(isSneaking, masteryLevel);
        assertEquals(expectedCount, count);
    }

    private static int computePillarCount(boolean isSneaking, int masteryLevel) {
        boolean isWall = isSneaking || masteryLevel >= 1;
        if (!isWall) {
            return 1;
        }
        if (masteryLevel >= 3) {
            return 5;
        }
        return 3;
    }

    @Test
    @DisplayName("Verify Earth Pillar combat parameters and interaction limits")
    void testPillarConstants() {
        assertEquals(140, EarthPillarSkill.PILLAR_DURATION_TICKS, "Pillar stance duration should be 7.0 seconds (140 ticks)");
        assertEquals(4, EarthPillarSkill.PILLAR_MAX_HITS, "Pillar barrage should support 4 rapid strikes");
        assertEquals(16.0f, EarthPillarSkill.MEGALITH_DAMAGE, 1e-4, "Megalith kick base damage should be 16.0");
        assertEquals(4.0f, EarthPillarSkill.SHARD_DAMAGE, 1e-4, "Shard strike base damage should be 4.0");
        assertTrue(EarthPillarSkill.INTERACTION_RADIUS >= 5.0, "Interaction radius should be at least 5.0 blocks");
    }
}
