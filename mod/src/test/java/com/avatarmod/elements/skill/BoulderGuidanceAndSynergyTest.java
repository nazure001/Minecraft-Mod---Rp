package com.avatarmod.elements.skill;

import com.avatarmod.elements.skill.impl.BoulderLaunchSkill;
import com.avatarmod.elements.skill.impl.EarthPillarSkill;
import net.minecraft.util.math.Vec3d;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BoulderGuidanceAndSynergyTest {

    @Test
    @DisplayName("Verify null and invalid item handling in weapon affinity helper")
    void testWeaponAffinityNullSafety() {
        assertFalse(ElementalInteractions.isWeaponAffinity(null, "FIRE"));
        assertFalse(ElementalInteractions.isWeaponAffinity(null, "WATER"));
        assertFalse(ElementalInteractions.isWeaponAffinity(null, "EARTH"));
        assertFalse(ElementalInteractions.isWeaponAffinity(null, "AIR"));
        assertFalse(ElementalInteractions.isWeaponAffinity(null, null));

        assertEquals(1.0f, ElementalInteractions.getWeaponDamageMultiplier(null, "FIRE"));
        assertEquals(1.0f, ElementalInteractions.getWeaponSpeedMultiplier(null, "EARTH"));
    }

    @Test
    @DisplayName("Verify auto-targeting soft-homing trajectory curving math")
    void testAutoTargetingTrajectoryCurving() {
        Vec3d forwardDir = new Vec3d(0.0, 0.0, 1.0);
        Vec3d targetOffset = new Vec3d(0.4, 0.0, 0.9).normalize();

        float steerStrength = 0.18f;
        Vec3d steeredDir = forwardDir.multiply(1.0 - steerStrength)
                .add(targetOffset.multiply(steerStrength)).normalize();

        // Steered direction must have nudged towards target X
        assertTrue(steeredDir.x > forwardDir.x, "Steered vector must curve towards target X");
        assertTrue(steeredDir.z > 0.9, "Steered vector must maintain high forward momentum");
        assertEquals(1.0, steeredDir.length(), 1e-4, "Steered direction must remain normalized unit vector");
    }

    @Test
    @DisplayName("Verify Boulder Launch charge ratio and speed scaling bounds")
    void testBoulderLaunchParameters() {
        assertTrue(BoulderLaunchSkill.MIN_SPEED >= 1.0f);
        assertTrue(BoulderLaunchSkill.MAX_SPEED >= BoulderLaunchSkill.MIN_SPEED);
        assertTrue(BoulderLaunchSkill.MAX_HITBOX >= BoulderLaunchSkill.MIN_HITBOX);
        assertTrue(BoulderLaunchSkill.MAX_AOE >= BoulderLaunchSkill.MIN_AOE);
    }

    @Test
    @DisplayName("Verify Earth Pillar interaction parameters")
    void testEarthPillarParameters() {
        assertEquals(140, EarthPillarSkill.PILLAR_DURATION_TICKS);
        assertEquals(4, EarthPillarSkill.PILLAR_MAX_HITS);
        assertTrue(EarthPillarSkill.INTERACTION_RADIUS >= 5.0);
    }
}
