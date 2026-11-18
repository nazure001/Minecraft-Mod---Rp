package com.avatarmod.elements.skill;

import net.minecraft.entity.Entity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.hit.HitResult;
import net.minecraft.world.RaycastContext;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

public final class SkillTargeting {

    public static boolean isWithinRange(Vec3d origin, Box targetBounds, double range) {
        double x = clamp(origin.x, targetBounds.minX, targetBounds.maxX);
        double y = clamp(origin.y, targetBounds.minY, targetBounds.maxY);
        double z = clamp(origin.z, targetBounds.minZ, targetBounds.maxZ);
        return origin.squaredDistanceTo(x, y, z) <= range * range;
    }

    public static boolean intersectsSegment(Vec3d start, Vec3d end, Box targetBounds, double padding) {
        double minX = targetBounds.minX - padding;
        double minY = targetBounds.minY - padding;
        double minZ = targetBounds.minZ - padding;
        double maxX = targetBounds.maxX + padding;
        double maxY = targetBounds.maxY + padding;
        double maxZ = targetBounds.maxZ + padding;
        double dx = end.x - start.x;
        double dy = end.y - start.y;
        double dz = end.z - start.z;
        double tMin = 0.0;
        double tMax = 1.0;

        if (Math.abs(dx) < 1.0e-7) {
            if (start.x < minX || start.x > maxX) return false;
        } else {
            double t1 = (minX - start.x) / dx;
            double t2 = (maxX - start.x) / dx;
            tMin = Math.max(tMin, Math.min(t1, t2));
            tMax = Math.min(tMax, Math.max(t1, t2));
            if (tMin > tMax) return false;
        }

        if (Math.abs(dy) < 1.0e-7) {
            if (start.y < minY || start.y > maxY) return false;
        } else {
            double t1 = (minY - start.y) / dy;
            double t2 = (maxY - start.y) / dy;
            tMin = Math.max(tMin, Math.min(t1, t2));
            tMax = Math.min(tMax, Math.max(t1, t2));
            if (tMin > tMax) return false;
        }

        if (Math.abs(dz) < 1.0e-7) {
            return start.z >= minZ && start.z <= maxZ && tMin <= tMax;
        }

        double t1 = (minZ - start.z) / dz;
        double t2 = (maxZ - start.z) / dz;
        tMin = Math.max(tMin, Math.min(t1, t2));
        tMax = Math.min(tMax, Math.max(t1, t2));
        return tMin <= tMax;
    }

    public static boolean hasLineOfSight(ServerWorld world, Vec3d start, Box targetBounds, Entity source) {
        Vec3d center = targetBounds.getCenter();
        if (start.squaredDistanceTo(center) < 1.0e-7) return true;
        if (world.raycast(new RaycastContext(
                start, center, RaycastContext.ShapeType.COLLIDER,
                RaycastContext.FluidHandling.NONE, source
        )).getType() == HitResult.Type.MISS) {
            return true;
        }
        Vec3d closest = closestPoint(start, targetBounds);
        if (start.squaredDistanceTo(closest) < 1.0e-7) return true;
        return world.raycast(new RaycastContext(
                start, closest, RaycastContext.ShapeType.COLLIDER,
                RaycastContext.FluidHandling.NONE, source
        )).getType() == HitResult.Type.MISS;
    }

    public static Box segmentBounds(Vec3d start, Vec3d end, double padding) {
        return new Box(
                Math.min(start.x, end.x) - padding,
                Math.min(start.y, end.y) - padding,
                Math.min(start.z, end.z) - padding,
                Math.max(start.x, end.x) + padding,
                Math.max(start.y, end.y) + padding,
                Math.max(start.z, end.z) + padding
        );
    }

    private static double clamp(double value, double min, double max) {
        return Math.max(min, Math.min(value, max));
    }

    private static Vec3d closestPoint(Vec3d point, Box bounds) {
        return new Vec3d(
                clamp(point.x, bounds.minX, bounds.maxX),
                clamp(point.y, bounds.minY, bounds.maxY),
                clamp(point.z, bounds.minZ, bounds.maxZ)
        );
    }

    private SkillTargeting() {}
}
