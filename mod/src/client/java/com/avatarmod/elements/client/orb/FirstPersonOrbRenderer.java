package com.avatarmod.elements.client.orb;

import com.mojang.blaze3d.systems.RenderSystem;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.*;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.math.RotationAxis;
import org.joml.Matrix4f;

/**
 * Renders the charge orb for the LOCAL player in first-person viewmodel space.
 * Registered via WorldRenderEvents.LAST so it draws over the world but under the HUD.
 *
 * Position: offset to the right hand, natural digenggam, does not cover crosshair.
 */
public final class FirstPersonOrbRenderer {

    // Offset in view/camera space: right, down, forward
    private static final float OFF_X =  0.55f;   // right hand side
    private static final float OFF_Y = -0.45f;   // below center
    private static final float OFF_Z = -0.70f;   // forward (into screen)

    private static final float BASE_RADIUS = 0.055f;
    private static final float MAX_RADIUS  = 0.090f;
    private static final int   CHARGE_MAX_TICKS = 10;

    public static void register() {
        WorldRenderEvents.LAST.register(FirstPersonOrbRenderer::render);
    }

    private static void render(WorldRenderContext ctx) {
        MinecraftClient mc = MinecraftClient.getInstance();
        if (mc.player == null || mc.options.getPerspective().isFirstPerson() == false) return;

        // Hide orb when inventory / screen is open
        if (mc.currentScreen != null) return;

        ChargeOrbClientState.OrbState state =
                ChargeOrbClientState.get(mc.player.getUuid());
        if (state == null || !state.isVisible()) return;

        float[] color = elementColor(state.skillId());
        float radius = computeRadius(state);

        // Build a fresh viewmodel matrix: starts from identity, applies head yaw/pitch
        MatrixStack matrices = new MatrixStack();

        // Slight sway using player's body yaw delta (optional, skipped for MVP)
        matrices.translate(OFF_X, OFF_Y, OFF_Z);

        // Face the camera (billboard-ish): no rotation — sphere looks same from all angles

        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.disableCull();
        RenderSystem.disableDepthTest();

        // Switch to projection that matches the hand/item render (narrower FOV, no clip)
        // For now we render into the same projection; a GameRenderer mixin would be more
        // accurate but adds complexity. This gives a good-enough in-hand feel.
        BufferBuilder buf = Tessellator.getInstance().begin(
                VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

        Matrix4f projMat = RenderSystem.getProjectionMatrix();
        Matrix4f modelMat = matrices.peek().getPositionMatrix();

        renderSphere(buf, modelMat, radius, color[0], color[1], color[2], color[3]);

        // We need to draw with the current projection; use drawWithGlobalProgram
        RenderSystem.setShader(GameRenderer::getPositionColorProgram);
        BufferRenderer.drawWithGlobalProgram(buf.end());

        RenderSystem.enableDepthTest();
        RenderSystem.enableCull();
        RenderSystem.disableBlend();
    }

    private static float computeRadius(ChargeOrbClientState.OrbState state) {
        float t = Math.min(1f, state.interpolatedTicks() / CHARGE_MAX_TICKS);
        return BASE_RADIUS + (MAX_RADIUS - BASE_RADIUS) * t;
    }

    private static float[] elementColor(String skillId) {
        if (skillId == null) return new float[]{1f, 0.4f, 0.1f, 0.85f};
        return switch (skillId) {
            case "avatar:fire_jab", "avatar:fire_jet", "avatar:flame_sweep" ->
                    new float[]{1f, 0.35f, 0.05f, 0.85f};
            case "avatar:air_blast", "avatar:air_vortex" ->
                    new float[]{0.8f, 0.95f, 1f, 0.60f};
            case "avatar:water_whip" ->
                    new float[]{0.1f, 0.5f, 1f, 0.75f};
            case "avatar:earth_boulder", "avatar:earth_wall" ->
                    new float[]{0.55f, 0.4f, 0.2f, 0.90f};
            default -> new float[]{1f, 0.4f, 0.1f, 0.85f};
        };
    }

    private static void renderSphere(BufferBuilder buf, Matrix4f mat,
                                      float r, float red, float green, float blue, float alpha) {
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
    }

    private FirstPersonOrbRenderer() {}
}
