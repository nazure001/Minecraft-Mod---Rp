package com.avatarmod.elements.skill;

import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.impl.WaterJetSkill;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WaterJetSkillTest {

    @BeforeAll
    static void setUp() {
        try {
            SkillRegistry.populate();
        } catch (Throwable t) {
            // If FabricLoader is not available in unit test classpath, load directly from resource
            try (var is = WaterJetSkillTest.class.getResourceAsStream("/data/avatar_elements/skill_definitions.json")) {
                if (is != null) {
                    var json = com.google.gson.JsonParser.parseReader(new java.io.InputStreamReader(is, java.nio.charset.StandardCharsets.UTF_8));
                    for (SkillDefinition def : SkillConfigParser.parseSkills("bundled", json)) {
                        java.lang.reflect.Method m = SkillRegistry.class.getDeclaredMethod("register", SkillDefinition.class);
                        m.setAccessible(true);
                        m.invoke(null, def);
                    }
                }
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    @Test
    void definitionLoadedAndMatchesContract() {
        Optional<SkillDefinition> optDef = SkillRegistry.get("avatar:water_jet");
        assertTrue(optDef.isPresent(), "avatar:water_jet must be registered");

        SkillDefinition def = optDef.get();
        assertEquals(SkillDefinition.Element.WATER, def.element());
        assertEquals(10, def.chiCost());
        assertEquals(0, def.chiPerTick());
        assertEquals(15, def.cooldownTicks());
        assertEquals(2, def.windupTicks());
        assertEquals(30, def.activeTicks());
        assertEquals(6, def.recoveryTicks());
        assertEquals(1.5f, def.damage());
        assertEquals(10.0f, def.range());
        assertEquals(0.4f, def.knockback());
        assertEquals(SkillDefinition.HitboxShape.LINE, def.hitboxShape());
        assertFalse(def.cancelOnHit());
    }

    @Test
    void elementSlotMappingAssignsWaterJet() {
        assertEquals("avatar:water_jet", ElementSlotMap.getSkillId("WATER", 1),
                "WATER slot 1 (X) must map to avatar:water_jet");
    }

    @Test
    void chiConsumptionCadence() {
        assertFalse(WaterJetSkill.shouldConsumeChi(0));
        assertFalse(WaterJetSkill.shouldConsumeChi(1));
        assertFalse(WaterJetSkill.shouldConsumeChi(2));
        assertTrue(WaterJetSkill.shouldConsumeChi(3));
        assertFalse(WaterJetSkill.shouldConsumeChi(4));
        assertFalse(WaterJetSkill.shouldConsumeChi(5));
        assertTrue(WaterJetSkill.shouldConsumeChi(6));

        // Total chi cost for 30 active ticks at 1 chi / 3 ticks
        assertEquals(10, WaterJetSkill.calculateTotalChiCost(30));
    }

    @Test
    void damageIntervalCadence() {
        assertFalse(WaterJetSkill.shouldDealDamage(0));
        assertFalse(WaterJetSkill.shouldDealDamage(1));
        assertFalse(WaterJetSkill.shouldDealDamage(2));
        assertTrue(WaterJetSkill.shouldDealDamage(3));
        assertFalse(WaterJetSkill.shouldDealDamage(4));
        assertTrue(WaterJetSkill.shouldDealDamage(6));
        assertTrue(WaterJetSkill.shouldDealDamage(30));
    }

    @Test
    void pushKnockbackCalculation() {
        Vec3d lookEast = new Vec3d(1.0, 0.0, 0.0);
        Vec3d push = WaterJetSkill.calculatePushVector(lookEast, 0.4);

        assertEquals(0.4, push.x, 1e-5);
        assertTrue(push.y > 0.0, "Should apply upward lift");
        assertEquals(0.0, push.z, 1e-5);

        Vec3d lookNorth = new Vec3d(0.0, 0.0, -1.0);
        Vec3d pushNorth = WaterJetSkill.calculatePushVector(lookNorth, 0.5);
        assertEquals(0.0, pushNorth.x, 1e-5);
        assertTrue(pushNorth.y > 0.0);
        assertEquals(-0.5, pushNorth.z, 1e-5);
    }

    @Test
    void timelineProgressionCycle() {
        SkillDefinition def = SkillRegistry.get("avatar:water_jet").orElseThrow();
        SkillTimeline timeline = new SkillTimeline(
                def.id(), def.windupTicks(), def.activeTicks(), def.recoveryTicks());

        timeline.start();
        assertEquals(SkillTimeline.Phase.WINDUP, timeline.phase());

        // 2 windup ticks
        timeline.tick();
        assertEquals(SkillTimeline.Phase.WINDUP, timeline.phase());
        timeline.tick();
        assertEquals(SkillTimeline.Phase.ACTIVE, timeline.phase());

        // 30 active ticks
        for (int i = 1; i < 30; i++) {
            timeline.tick();
            assertEquals(SkillTimeline.Phase.ACTIVE, timeline.phase());
        }
        timeline.tick();
        assertEquals(SkillTimeline.Phase.RECOVERY, timeline.phase());

        // 6 recovery ticks
        for (int i = 1; i < 6; i++) {
            timeline.tick();
            assertEquals(SkillTimeline.Phase.RECOVERY, timeline.phase());
        }
        timeline.tick();
        assertEquals(SkillTimeline.Phase.IDLE, timeline.phase());
        assertTrue(timeline.isIdle());
    }

    @Test
    void lineTargetingIntersection() {
        Vec3d origin = new Vec3d(0.0, 1.6, 0.0);
        Vec3d look = new Vec3d(0.0, 0.0, 1.0);
        double range = 10.0;
        Vec3d end = origin.add(look.multiply(range));
        double padding = WaterJetSkill.STREAM_PADDING;

        // Target directly in stream path at 5 blocks distance
        Box targetInPath = new Box(-0.4, 1.0, 4.5, 0.4, 2.2, 5.5);
        assertTrue(SkillTargeting.intersectsSegment(origin, end, targetInPath, padding));

        // Target behind caster
        Box targetBehind = new Box(-0.4, 1.0, -3.0, 0.4, 2.2, -2.0);
        assertFalse(SkillTargeting.intersectsSegment(origin, end, targetBehind, padding));

        // Target beyond maximum range
        Box targetTooFar = new Box(-0.4, 1.0, 12.0, 0.4, 2.2, 13.0);
        assertFalse(SkillTargeting.intersectsSegment(origin, end, targetTooFar, padding));

        // Target laterally far off to the side (5 blocks to the right)
        Box targetToSide = new Box(4.5, 1.0, 5.0, 5.5, 2.2, 6.0);
        assertFalse(SkillTargeting.intersectsSegment(origin, end, targetToSide, padding));
    }
}
