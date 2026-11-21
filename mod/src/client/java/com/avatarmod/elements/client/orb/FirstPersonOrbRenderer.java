package com.avatarmod.elements.client.orb;

import com.mojang.blaze3d.platform.GlStateManager;
import com.mojang.blaze3d.systems.RenderSystem;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.*;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.math.Vec3d;
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
        if (mc.player == null || !mc.options.getPerspective().isFirstPerson()) return;
        if (mc.currentScreen != null) return;

        ChargeOrbClientState.OrbState state =
                ChargeOrbClientState.get(mc.player.getUuid());
        if (state == null || !state.isVisible()) return;

        float[] color = elementColor(state.skillId());
        float radius = computeRadius(state);

        // Use the world render context's matrix stack (already camera-relative).
        // Translate to player eye position, rotate by player yaw so OFF_X/Z are
        // in front-of-player space, then apply hand offset.
        MatrixStack matrices = ctx.matrixStack();
        Camera camera = ctx.camera();
        Vec3d camPos = camera.getPos();

        // Player eye position relative to camera
        Vec3d eyePos = mc.player.getEyePos();

        matrices.push();
        matrices.translate(eyePos.x - camPos.x, eyePos.y - camPos.y, eyePos.z - camPos.z);
        // Rotate so +X is to the player's right, -Z is forward
        matrices.multiply(RotationAxis.POSITIVE_Y.rotationDegrees(-mc.player.getYaw()));
        matrices.multiply(RotationAxis.POSITIVE_X.rotationDegrees(mc.player.getPitch()));
        matrices.translate(OFF_X, OFF_Y, OFF_Z);

        boolean isEarth = "avatar:earth_boulder".equals(state.skillId())
                || "avatar:earth_wall".equals(state.skillId())
                || "avatar:boulder_launch".equals(state.skillId())
                || "avatar:earth_pillar".equals(state.skillId());
        boolean isFire = "avatar:fire_jab".equals(state.skillId())
                || "avatar:fire_blast".equals(state.skillId())
                || "avatar:fire_jet".equals(state.skillId())
                || "avatar:flame_sweep".equals(state.skillId());

        long time = System.currentTimeMillis();

        if (isEarth) {
            // Earth: Opaque/semi-opaque rocky megalith with rugged faceted boulder surface
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE_MINUS_SRC_ALPHA);
            RenderSystem.disableCull();
            RenderSystem.enableDepthTest();
            RenderSystem.setShader(GameRenderer::getPositionColorProgram);

            BufferBuilder buf = Tessellator.getInstance().begin(
                    VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

            renderRockyBoulder(buf, matrices.peek().getPositionMatrix(), radius);

            BufferRenderer.drawWithGlobalProgram(buf.end());

            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        } else if (isFire) {
            // Fire: Turbulent roaring flame corona licking around hand with dynamic flame tongues
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE); // additive fire glow
            RenderSystem.disableCull();
            RenderSystem.disableDepthTest();
            RenderSystem.setShader(GameRenderer::getPositionColorProgram);

            BufferBuilder buf = Tessellator.getInstance().begin(
                    VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

            renderDynamicFlame(buf, matrices.peek().getPositionMatrix(), radius, time);

            BufferRenderer.drawWithGlobalProgram(buf.end());

            RenderSystem.enableDepthTest();
            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        } else {
            // Other elements (Air, Water): Stylized luminous elemental sphere
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE);
            RenderSystem.disableCull();
            RenderSystem.disableDepthTest();
            RenderSystem.setShader(GameRenderer::getPositionColorProgram);

            BufferBuilder buf = Tessellator.getInstance().begin(
                    VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

            // 1. Inner core: bright hot center
            renderSphere(buf, matrices.peek().getPositionMatrix(),
                    radius * 0.55f, 1.0f, 0.95f, 0.85f, Math.min(1.0f, color[3] * 1.6f));

            // 2. Outer shell: element-tinted soft halo
            renderSphere(buf, matrices.peek().getPositionMatrix(),
                    radius, color[0], color[1], color[2], color[3] * 0.75f);

            BufferRenderer.drawWithGlobalProgram(buf.end());

            RenderSystem.enableDepthTest();
            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        }

        matrices.pop();
    }

    private static float computeRadius(ChargeOrbClientState.OrbState state) {
        boolean holdCharged = "avatar:fire_blast".equals(state.skillId())
                || "avatar:boulder_launch".equals(state.skillId());
        int maxTicks = holdCharged ? 40 : CHARGE_MAX_TICKS;
        float baseR = holdCharged ? 0.08f : BASE_RADIUS;
        float maxR  = holdCharged ? 0.22f : MAX_RADIUS;
        float t = Math.min(1f, state.interpolatedTicks() / maxTicks);
        return baseR + (maxR - baseR) * t;
    }

    private static float[] elementColor(String skillId) {
        if (skillId == null) return new float[]{1f, 0.4f, 0.1f, 0.85f};
        return switch (skillId) {
            case "avatar:fire_jab", "avatar:fire_blast", "avatar:fire_jet", "avatar:flame_sweep" ->
                    new float[]{1f, 0.35f, 0.05f, 0.40f};
            case "avatar:air_blast", "avatar:air_vortex" ->
                    new float[]{0.8f, 0.95f, 1f, 0.60f};
            case "avatar:water_whip" ->
                    new float[]{0.1f, 0.5f, 1f, 0.75f};
            case "avatar:earth_boulder", "avatar:earth_wall", "avatar:boulder_launch", "avatar:earth_pillar" ->
                    new float[]{0.55f, 0.4f, 0.2f, 0.85f};
            default -> new float[]{1f, 0.4f, 0.1f, 0.85f};
        };
    }

    /**
     * Renders an authentic dynamic fire aura with flickering flame tongues rising in +Y.
     */
    private static void renderDynamicFlame(BufferBuilder buf, Matrix4f mat, float r, long time) {
        int stacks = 8;
        int slices = 12;

        // 1. Hot white-yellow molten core
        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;
            float r0 = r * 0.45f * (float) Math.cos(phi0);
            float r1 = r * 0.45f * (float) Math.cos(phi1);
            float y0 = r * 0.45f * (float) Math.sin(phi0);
            float y1 = r * 0.45f * (float) Math.sin(phi1);

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

                buf.vertex(mat, x00, y0, z00).color(1.0f, 0.95f, 0.60f, 0.90f);
                buf.vertex(mat, x10, y1, z10).color(1.0f, 0.95f, 0.60f, 0.90f);
                buf.vertex(mat, x11, y1, z11).color(1.0f, 0.95f, 0.60f, 0.90f);
                buf.vertex(mat, x01, y0, z01).color(1.0f, 0.95f, 0.60f, 0.90f);
            }
        }

        // 2. Turbulent outer licking flame tongues (elongated upward in +Y and oscillating with time)
        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;

            for (int j = 0; j < slices; j++) {
                double theta0 = 2 * Math.PI * j / slices;
                double theta1 = 2 * Math.PI * (j + 1) / slices;

                float wave0 = 1.0f + 0.35f * (float) Math.sin(time * 0.012f + i * 1.8f + j * 2.2f);
                float wave1 = 1.0f + 0.35f * (float) Math.sin(time * 0.012f + (i + 1) * 1.8f + (j + 1) * 2.2f);

                // Upward flame stretch: higher phi (upper hemisphere) gets extra upward lift
                float flameLift0 = (float) Math.max(0, Math.sin(phi0)) * r * 0.6f;
                float flameLift1 = (float) Math.max(0, Math.sin(phi1)) * r * 0.6f;

                float r0 = r * wave0 * (float) Math.cos(phi0);
                float r1 = r * wave1 * (float) Math.cos(phi1);
                float y0 = r * wave0 * (float) Math.sin(phi0) + flameLift0;
                float y1 = r * wave1 * (float) Math.sin(phi1) + flameLift1;

                float x00 = (float) (r0 * Math.cos(theta0));
                float z00 = (float) (r0 * Math.sin(theta0));
                float x10 = (float) (r1 * Math.cos(theta0));
                float z10 = (float) (r1 * Math.sin(theta0));
                float x01 = (float) (r0 * Math.cos(theta1));
                float z01 = (float) (r0 * Math.sin(theta1));
                float x11 = (float) (r1 * Math.cos(theta1));
                float z11 = (float) (r1 * Math.sin(theta1));

                float red = 1.0f;
                float green = 0.35f + 0.25f * (float) Math.sin(theta0);
                float blue = 0.04f;
                float alpha = 0.65f;

                buf.vertex(mat, x00, y0, z00).color(red, green, blue, alpha);
                buf.vertex(mat, x10, y1, z10).color(red, green, blue, alpha);
                buf.vertex(mat, x11, y1, z11).color(red, green, blue, alpha);
                buf.vertex(mat, x01, y0, z01).color(red, green, blue, alpha);
            }
        }
    }

    /**
     * Renders a solid, faceted, geological boulder with earthen texture facets.
     */
    private static void renderRockyBoulder(BufferBuilder buf, Matrix4f mat, float r) {
        int stacks = 8;
        int slices = 10;

        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;

            for (int j = 0; j < slices; j++) {
                double theta0 = 2 * Math.PI * j / slices;
                double theta1 = 2 * Math.PI * (j + 1) / slices;

                // Geological rock facets: jagged perturbation
                float facet0 = 1.0f + 0.18f * (float) Math.sin(i * 3.1f + j * 4.7f);
                float facet1 = 1.0f + 0.18f * (float) Math.sin((i + 1) * 3.1f + (j + 1) * 4.7f);

                float r0 = r * facet0 * (float) Math.cos(phi0);
                float r1 = r * facet1 * (float) Math.cos(phi1);
                float y0 = r * facet0 * (float) Math.sin(phi0);
                float y1 = r * facet1 * (float) Math.sin(phi1);

                float x00 = (float) (r0 * Math.cos(theta0));
                float z00 = (float) (r0 * Math.sin(theta0));
                float x10 = (float) (r1 * Math.cos(theta0));
                float z10 = (float) (r1 * Math.sin(theta0));
                float x01 = (float) (r0 * Math.cos(theta1));
                float z01 = (float) (r0 * Math.sin(theta1));
                float x11 = (float) (r1 * Math.cos(theta1));
                float z11 = (float) (r1 * Math.sin(theta1));

                // Shading: upper facets lighter stone, lower facets darker deepslate/earth
                float shade = 0.55f + 0.45f * (float) Math.sin(phi0);
                float red   = (0.46f + 0.08f * ((i + j) % 2)) * shade;
                float green = (0.38f + 0.06f * ((i + j) % 2)) * shade;
                float blue  = (0.30f + 0.04f * ((i + j) % 2)) * shade;

                buf.vertex(mat, x00, y0, z00).color(red, green, blue, 1.0f);
                buf.vertex(mat, x10, y1, z10).color(red, green, blue, 1.0f);
                buf.vertex(mat, x11, y1, z11).color(red, green, blue, 1.0f);
                buf.vertex(mat, x01, y0, z01).color(red, green, blue, 1.0f);
            }
        }
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
