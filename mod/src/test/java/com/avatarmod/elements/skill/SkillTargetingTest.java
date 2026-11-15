package com.avatarmod.elements.skill;

import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SkillTargetingTest {

    @Test
    void segmentIntersectsTargetBoundsAlongAllAxes() {
        Vec3d start = Vec3d.ZERO;
        Vec3d end = new Vec3d(0, 0, 8);

        assertTrue(SkillTargeting.intersectsSegment(start, end,
                new Box(-0.3, -0.3, 3, 0.3, 0.3, 3.6), 0));
        assertTrue(SkillTargeting.intersectsSegment(start, end,
                new Box(-0.3, 0.5, 3, 0.3, 0.8, 3.6), 0.6));
    }

    @Test
    void segmentRejectsTargetsBehindOutsideItsPaddingOrPastItsEnd() {
        Vec3d start = Vec3d.ZERO;
        Vec3d end = new Vec3d(0, 0, 8);

        assertFalse(SkillTargeting.intersectsSegment(start, end,
                new Box(-0.3, -0.3, -2, 0.3, 0.3, -1), 0.5));
        assertFalse(SkillTargeting.intersectsSegment(start, end,
                new Box(2, -0.3, 3, 2.3, 0.3, 3.5), 0.5));
        assertFalse(SkillTargeting.intersectsSegment(start, end,
                new Box(-0.3, -0.3, 8.6, 0.3, 0.3, 9), 0));
    }

    @Test
    void rangeUsesNearestPointOnBoundsRatherThanOnlyEntityCenter() {
        Vec3d origin = Vec3d.ZERO;

        assertTrue(SkillTargeting.isWithinRange(origin,
                new Box(-0.5, -0.5, 2.4, 0.5, 0.5, 3.4), 2.5));
        assertFalse(SkillTargeting.isWithinRange(origin,
                new Box(-0.5, -0.5, 2.6, 0.5, 0.5, 3.6), 2.5));
    }

    @Test
    void segmentBoundsContainThePaddedPath() {
        Box bounds = SkillTargeting.segmentBounds(
                new Vec3d(1, 2, 3), new Vec3d(1, 6, 8), 0.5);

        assertTrue(bounds.contains(new Vec3d(1.4, 4, 7.5)));
        assertFalse(bounds.contains(new Vec3d(1.6, 4, 7.5)));
    }
}
