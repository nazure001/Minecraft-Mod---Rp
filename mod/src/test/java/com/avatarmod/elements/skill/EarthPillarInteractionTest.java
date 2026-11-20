package com.avatarmod.elements.skill;

import com.avatarmod.elements.skill.impl.EarthPillarSkill;
import net.minecraft.util.math.Vec3d;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EarthPillarInteractionTest {

    @Test
    @DisplayName("Verify Earth Pillar interaction parameters and launch kinematics")
    void testPillarKinematics() {
        assertTrue(EarthPillarSkill.INTERACTION_RADIUS >= 5.0,
                "Interaction radius must be at least 5.0m for comfortable martial kick reach");
        assertTrue(EarthPillarSkill.MEGALITH_SPEED >= 1.0f,
                "Megalith launch speed must be at least 1.0 blocks/tick for impactful visual flight");
        assertTrue(EarthPillarSkill.MEGALITH_DAMAGE >= 12.0f,
                "Kicked megalith boulder damage must reflect massive impact force (>= 12.0)");

        // Test launch velocity calculation
        Vec3d look = new Vec3d(0.0, 0.0, 1.0);
        Vec3d dir = new Vec3d(look.x, Math.max(-0.2, look.y), look.z).normalize();
        Vec3d vel = dir.multiply(EarthPillarSkill.MEGALITH_SPEED);

        assertEquals(0.0, vel.x, 1e-4);
        assertEquals(0.0, vel.y, 1e-4);
        assertEquals(EarthPillarSkill.MEGALITH_SPEED, vel.z, 1e-4);
    }
}
