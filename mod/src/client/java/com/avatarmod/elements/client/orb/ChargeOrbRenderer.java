package com.avatarmod.elements.client.orb;

import com.mojang.blaze3d.systems.RenderSystem;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.*;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.math.Vec3d;
import org.joml.Matrix4f;

import java.util.Map;
import java.util.UUID;

/**
 * Renders the charge orb on other players (3rd person / spectator view).
 * Registered via WorldRenderEvents.AFTER_ENTITIES.
 *
 * Fire element only for now; other elements use the same geometry with different colors.
 */
public final class ChargeOrbRenderer {

    // Orb appears at hand position offset from player center
    private static final double HAND_OFFSET_X = 0.35;
    private static final double HAND_OFFSET_Y = 0.9;
    private static final double HAND_OFFSET_Z = 0.2;

    private static final float BASE_RADIUS = 0.18f;
    private static final float MAX_RADIUS  = 0.30f;
    private static final int   CHARGE_MAX_TICKS = 10; // ticks until full size

    public static void register() {
        WorldRenderEvents.AFTER_ENTITIES.register(ChargeOrbRenderer::render);
    }

    private static void render(WorldRenderContext ctx) {
        Map<UUID, ChargeOrbClientState.OrbState> all = ChargeOrbClientState.all();
        if (all.isEmpty()) return;

        MinecraftClient mc = MinecraftClient.getInstance();
        if (mc.world == null) return;

        Camera camera = ctx.camera();
        Vec3d camPos = camera.getPos();

        MatrixStack matrices = ctx.matrixStack();

        for (Map.Entry<UUID, ChargeOrbClientState.OrbState> entry : all.entrySet()) {
            ChargeOrbClientState.OrbState state = entry.getValue();
            if (!state.isVisible()) continue;

            PlayerEntity player = mc.world.getPlayerByUuid(entry.getKey());
            if (player == null) continue;
            // Skip self — handled by FirstPersonOrbRenderer
            if (player == mc.player) continue;

            // Orb position: right-hand approximate world position
            Vec3d pos = player.getPos()
                    .add(HAND_OFFSET_X, HAND_OFFSET_Y, HAND_OFFSET_Z);

            float radius = computeRadius(state);
            float[] color = elementColor(state.skillId());

            matrices.push();
            matrices.translate(pos.x - camPos.x, pos.y - camPos.y, pos.z - camPos.z);

            renderOrb(matrices, radius, color[0], color[1], color[2], color[3]);

            matrices.pop();
        }
    }

    private static float computeRadius(ChargeOrbClientState.OrbState state) {
        float t = Math.min(1f, state.interpolatedTicks() / CHARGE_MAX_TICKS);
        return BASE_RADIUS + (MAX_RADIUS - BASE_RADIUS) * t;
    }

    /** RGBA color based on skill element. */
    private static float[] elementColor(String skillId) {
        if (skillId == null) return new float[]{1f, 0.4f, 0.1f, 0.85f};
        return switch (skillId) {
            case "avatar:fire_jab", "avatar:fire_jet", "avatar:flame_sweep" ->
                    new float[]{1f, 0.35f, 0.05f, 0.85f};   // orange-red
            case "avatar:air_blast", "avatar:air_vortex" ->
                    new float[]{0.8f, 0.95f, 1f, 0.60f};    // pale blue-white
            case "avatar:water_whip" ->
                    new float[]{0.1f, 0.5f, 1f, 0.75f};     // deep blue
            case "avatar:earth_boulder", "avatar:earth_wall" ->
                    new float[]{0.55f, 0.4f, 0.2f, 0.90f};  // brown
            default -> new float[]{1f, 0.4f, 0.1f, 0.85f};
        };
    }

    /**
     * Renders a UV-sphere using immediate-mode quads.
     * Kept simple (12×8 segments) for MVP — no shader, no texture.
     */
    private static void renderOrb(MatrixStack matrices, float r,
                                   float red, float green, float blue, float alpha) {
        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.disableCull();
        RenderSystem.disableDepthTest();

        BufferBuilder buf = Tessellator.getInstance().begin(
                VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

        Matrix4f mat = matrices.peek().getPositionMatrix();

        int stacks = 8;
        int slices = 12;

        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;

            double y0 = r * Math.sin(phi0);
            double y1 = r * Math.sin(phi1);
            double r0 = r * Math.cos(phi0);
            double r1 = r * Math.cos(phi1);

            for (int j = 0; j < slices; j++) {
                double theta0 = 2 * Math.PI * j / slices;
                double theta1 = 2 * Math.PI * (j + 1) / slices;

                float x00 = (float) (r0 * Math.cos(theta0));
                float z00 = (float) (r0 * Math.sin(theta0));
                float x10 = (float) (r1 * Math.cos(theta0));
                float z10 = (float) (r1 * Math.sin(theta0));
                float x01 = (float) (r0 * Math.cos(theta1));
                float z01 = (float) (r0 * Math.sin(theta1));
                float x11 = (float) (r1 * Math.cos(theta1));
                float z11 = (float) (r1 * Math.sin(theta1));

                buf.vertex(mat, x00, (float) y0, z00).color(red, green, blue, alpha);
                buf.vertex(mat, x10, (float) y1, z10).color(red, green, blue, alpha);
                buf.vertex(mat, x11, (float) y1, z11).color(red, green, blue, alpha);
                buf.vertex(mat, x01, (float) y0, z01).color(red, green, blue, alpha);
            }
        }

        BufferRenderer.drawWithGlobalProgram(buf.end());

        RenderSystem.enableDepthTest();
        RenderSystem.enableCull();
        RenderSystem.disableBlend();
    }

    private ChargeOrbRenderer() {}
}
