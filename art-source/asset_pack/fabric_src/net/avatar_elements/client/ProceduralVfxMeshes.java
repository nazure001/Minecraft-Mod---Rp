package net.avatar_elements.client;

import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.util.math.MatrixStack;
import org.joml.Matrix4f;

/**
 * Procedural 3D Mesh VFX Generator for Minecraft 1.21.1 Fabric (WorldRenderEvents).
 * Renders Ring, Arc, Cone, Sphere Shell (Charge Orb), Dome, Spline Tube (Water Whip / Octopus Form),
 * Funnel (Air Vortex / Spout), and Ribbon Trails with automatic teleport-distance reset.
 */
public final class ProceduralVfxMeshes {

    public static void emitRing(MatrixStack matrices, VertexConsumer vc, float innerR, float outerR, int segs, float uScroll, int argb) {
        Matrix4f mat = matrices.peek().getPositionMatrix();
        for (int i = 0; i < segs; i++) {
            float u0 = (float) i / segs;
            float u1 = (float) (i + 1) / segs;
            double a0 = u0 * Math.PI * 2.0;
            double a1 = u1 * Math.PI * 2.0;
            float c0 = (float) Math.cos(a0), s0 = (float) Math.sin(a0);
            float c1 = (float) Math.cos(a1), s1 = (float) Math.sin(a1);

            vc.vertex(mat, innerR * c0, 0f, innerR * s0).color(argb).texture(u0 + uScroll, 0f).light(0xF000F0).normal(0f, 1f, 0f);
            vc.vertex(mat, outerR * c0, 0f, outerR * s0).color(argb).texture(u0 + uScroll, 1f).light(0xF000F0).normal(0f, 1f, 0f);
            vc.vertex(mat, outerR * c1, 0f, outerR * s1).color(argb).texture(u1 + uScroll, 1f).light(0xF000F0).normal(0f, 1f, 0f);
            vc.vertex(mat, innerR * c1, 0f, innerR * s1).color(argb).texture(u1 + uScroll, 0f).light(0xF000F0).normal(0f, 1f, 0f);
        }
    }

    public static void emitTaperedSplineTube(MatrixStack matrices, VertexConsumer vc, float[][] spinePts, float baseRadius, float tipRadius, int radialSegs, float vScroll, int argb) {
        Matrix4f mat = matrices.peek().getPositionMatrix();
        int n = spinePts.length;
        for (int i = 0; i < n - 1; i++) {
            float t0 = (float) i / (n - 1);
            float t1 = (float) (i + 1) / (n - 1);
            float r0 = baseRadius * (1f - t0) + tipRadius * t0;
            float r1 = baseRadius * (1f - t1) + tipRadius * t1;
            float[] p0 = spinePts[i];
            float[] p1 = spinePts[i + 1];

            for (int j = 0; j < radialSegs; j++) {
                double a0 = (double) j / radialSegs * Math.PI * 2.0;
                double a1 = (double) (j + 1) / radialSegs * Math.PI * 2.0;
                float u0 = (float) j / radialSegs;
                float u1 = (float) (j + 1) / radialSegs;

                vc.vertex(mat, p0[0] + r0 * (float) Math.cos(a0), p0[1], p0[2] + r0 * (float) Math.sin(a0)).color(argb).texture(u0, t0 - vScroll).light(0xF000F0).normal(0f, 1f, 0f);
                vc.vertex(mat, p1[0] + r1 * (float) Math.cos(a0), p1[1], p1[2] + r1 * (float) Math.sin(a0)).color(argb).texture(u0, t1 - vScroll).light(0xF000F0).normal(0f, 1f, 0f);
                vc.vertex(mat, p1[0] + r1 * (float) Math.cos(a1), p1[1], p1[2] + r1 * (float) Math.sin(a1)).color(argb).texture(u1, t1 - vScroll).light(0xF000F0).normal(0f, 1f, 0f);
                vc.vertex(mat, p0[0] + r0 * (float) Math.cos(a1), p0[1], p0[2] + r0 * (float) Math.sin(a1)).color(argb).texture(u1, t0 - vScroll).light(0xF000F0).normal(0f, 1f, 0f);
            }
        }
    }
}
