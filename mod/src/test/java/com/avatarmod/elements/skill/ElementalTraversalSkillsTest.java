package com.avatarmod.elements.skill;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Validates the Elemental Traversal and Mobility Suite across all 4 elements:
 * 1. Fire Jet (avatar:fire_jet) — Sustained 3D rocket flight in look direction.
 * 2. Air Scooter (avatar:air_scooter) — Sustained compressed air sphere gliding.
 * 3. Water Surf & Ice Scooter (avatar:water_surf) — Adaptive water wave surfing / frosted ice skating.
 * 4. Earth Tunnel & Surfing (avatar:earth_tunnel) — Subterranean 3x3 rock excavation & earth wave surfing.
 */
class ElementalTraversalSkillsTest {

    private static List<SkillDefinition> loadTestSkills() {
        try (var is = ElementalTraversalSkillsTest.class.getResourceAsStream("/data/avatar_elements/skill_definitions.json")) {
            assertNotNull(is, "Bundled skill_definitions.json not found");
            return SkillConfigParser.parseSkills("test skills",
                    com.google.gson.JsonParser.parseReader(new java.io.InputStreamReader(is, java.nio.charset.StandardCharsets.UTF_8)));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    @DisplayName("Verify all 4 elemental traversal skills are mapped to Slot 4 (tombol B)")
    void testSlot4TraversalMapping() {
        assertEquals("avatar:fire_jet", ElementSlotMap.getSkillId("FIRE", 4),
                "Fire slot 4 must map to fire_jet");
        assertEquals("avatar:air_scooter", ElementSlotMap.getSkillId("AIR", 4),
                "Air slot 4 must map to air_scooter");
        assertEquals("avatar:water_surf", ElementSlotMap.getSkillId("WATER", 4),
                "Water slot 4 must map to water_surf");
        assertEquals("avatar:earth_tunnel", ElementSlotMap.getSkillId("EARTH", 4),
                "Earth slot 4 must map to earth_tunnel");
    }

    @Test
    @DisplayName("Verify water_surf skill definition schema and hold-release parameters")
    void testWaterSurfDefinition() {
        List<SkillDefinition> skills = loadTestSkills();
        SkillDefinition waterSurf = skills.stream()
                .filter(s -> "avatar:water_surf".equals(s.id()))
                .findFirst()
                .orElse(null);

        assertNotNull(waterSurf, "avatar:water_surf must be registered in bundled skill definitions");
        assertEquals(SkillDefinition.Element.WATER, waterSurf.element());
        assertTrue(waterSurf.isHoldRelease(), "water_surf must support hold-release channeling");
        assertEquals(80, waterSurf.maxChargeTicks(), "water_surf must allow up to 80 hold ticks (4s)");
        assertEquals(1, waterSurf.windupTicks());
        assertEquals(18, waterSurf.activeTicks());
        assertEquals(1, waterSurf.recoveryTicks());
        assertEquals(15, waterSurf.chiCost());
        assertEquals(25, waterSurf.cooldownTicks());
        int totalTicks = waterSurf.windupTicks() + waterSurf.activeTicks() + waterSurf.recoveryTicks();
        assertEquals(20, totalTicks);
        assertEquals(1.0, totalTicks * 0.05, 1e-4, "PAL animation duration must be exactly 1.0s");
    }

    @Test
    @DisplayName("Verify earth_tunnel skill definition schema and hold-release parameters")
    void testEarthTunnelDefinition() {
        List<SkillDefinition> skills = loadTestSkills();
        SkillDefinition earthTunnel = skills.stream()
                .filter(s -> "avatar:earth_tunnel".equals(s.id()))
                .findFirst()
                .orElse(null);

        assertNotNull(earthTunnel, "avatar:earth_tunnel must be registered in bundled skill definitions");
        assertEquals(SkillDefinition.Element.EARTH, earthTunnel.element());
        assertTrue(earthTunnel.isHoldRelease(), "earth_tunnel must support hold-release channeling");
        assertEquals(80, earthTunnel.maxChargeTicks(), "earth_tunnel must allow up to 80 hold ticks (4s)");
        assertEquals(1, earthTunnel.windupTicks());
        assertEquals(18, earthTunnel.activeTicks());
        assertEquals(1, earthTunnel.recoveryTicks());
        assertEquals(15, earthTunnel.chiCost());
        assertEquals(25, earthTunnel.cooldownTicks());
        int earthTicks = earthTunnel.windupTicks() + earthTunnel.activeTicks() + earthTunnel.recoveryTicks();
        assertEquals(20, earthTicks);
        assertEquals(1.0, earthTicks * 0.05, 1e-4, "PAL animation duration must be exactly 1.0s");
    }

    @Test
    @DisplayName("Verify fire_jet and air_scooter support sustained hold-release flight")
    void testSustainedFlightHoldParameters() {
        List<SkillDefinition> skills = loadTestSkills();

        SkillDefinition fireJet = skills.stream()
                .filter(s -> "avatar:fire_jet".equals(s.id()))
                .findFirst()
                .orElseThrow();
        assertTrue(fireJet.isHoldRelease(), "fire_jet must support hold-release channeling");
        assertEquals(80, fireJet.maxChargeTicks());
        int fireTicks = fireJet.windupTicks() + fireJet.activeTicks() + fireJet.recoveryTicks();
        assertEquals(21, fireTicks);
        assertEquals(1.05, fireTicks * 0.05, 1e-4);

        SkillDefinition airScooter = skills.stream()
                .filter(s -> "avatar:air_scooter".equals(s.id()))
                .findFirst()
                .orElseThrow();
        assertTrue(airScooter.isHoldRelease(), "air_scooter must support hold-release channeling");
        assertEquals(80, airScooter.maxChargeTicks());
        int airTicks = airScooter.windupTicks() + airScooter.activeTicks() + airScooter.recoveryTicks();
        assertEquals(20, airTicks);
        assertEquals(1.0, airTicks * 0.05, 1e-4);
    }

    @Test
    @DisplayName("Verify weapon affinity multipliers for traversal speed")
    void testWeaponAffinitySpeedMultipliers() {
        // Null or non-weapon stack defaults to 1.0x
        assertEquals(1.0f, ElementalInteractions.getWeaponSpeedMultiplier(null, "FIRE"));
        assertEquals(1.0f, ElementalInteractions.getWeaponSpeedMultiplier(null, "WATER"));
        assertEquals(1.0f, ElementalInteractions.getWeaponSpeedMultiplier(null, "EARTH"));
        assertEquals(1.0f, ElementalInteractions.getWeaponSpeedMultiplier(null, "AIR"));
    }
}
