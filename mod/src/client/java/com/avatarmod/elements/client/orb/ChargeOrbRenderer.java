package com.avatarmod.elements.client.orb;

import com.mojang.blaze3d.platform.GlStateManager;
import com.mojang.blaze3d.systems.RenderSystem;
import com.avatarmod.elements.client.vfx.KnuckleVfxHelper;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.client.render.*;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.math.MathHelper;
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
            // Skip self only in 1st person — FirstPersonOrbRenderer handles that view
            if (player == mc.player && mc.options.getPerspective().isFirstPerson()) continue;

            // Orb position: use KnuckleVfxHelper to follow right arm/knuckle in 3rd-person, fallback to body yaw offset
            float tickDelta = ctx.tickCounter() != null ? ctx.tickCounter().getTickDelta(false) : 1.0f;
            Vec3d pos;
            if (player instanceof AbstractClientPlayerEntity acp) {
                pos = KnuckleVfxHelper.getKnucklePosition(acp, tickDelta);
            } else {
                float bodyYaw = MathHelper.lerpAngleDegrees(tickDelta, player.prevBodyYaw, player.bodyYaw);
                float yawRad = -(float) Math.toRadians(bodyYaw);
                Vec3d rotatedOffset = new Vec3d(HAND_OFFSET_X, 0.0, HAND_OFFSET_Z).rotateY(yawRad);
                Vec3d playerPos = player.getLerpedPos(tickDelta);
                pos = playerPos.add(rotatedOffset.x, HAND_OFFSET_Y, rotatedOffset.z);
            }

            float radius = computeRadius(state);
            float[] color = elementColor(state.skillId());

            matrices.push();
            matrices.translate(pos.x - camPos.x, pos.y - camPos.y, pos.z - camPos.z);

            renderElementalOrb(matrices, state.skillId(), radius, color[0], color[1], color[2], color[3]);

            matrices.pop();
        }
    }

    private static float computeRadius(ChargeOrbClientState.OrbState state) {
        boolean holdCharged = "avatar:fire_blast".equals(state.skillId())
                || "avatar:boulder_launch".equals(state.skillId());
        int maxTicks = holdCharged ? 40 : CHARGE_MAX_TICKS;
        float baseR = holdCharged ? 0.22f : BASE_RADIUS;
        float maxR  = holdCharged ? 0.55f : MAX_RADIUS;
        float t = Math.min(1f, state.interpolatedTicks() / maxTicks);
        return baseR + (maxR - baseR) * t;
    }

    /** RGBA color based on skill element. */
    private static float[] elementColor(String skillId) {
        if (skillId == null) return new float[]{1f, 0.4f, 0.1f, 0.85f};
        return switch (skillId) {
            case "avatar:fire_jab", "avatar:fire_blast", "avatar:fire_jet", "avatar:flame_sweep" ->
                    new float[]{1f, 0.35f, 0.05f, 0.40f};   // orange-red
            case "avatar:air_blast", "avatar:air_vortex" ->
                    new float[]{0.8f, 0.95f, 1f, 0.60f};    // pale blue-white
            case "avatar:water_whip" ->
                    new float[]{0.1f, 0.5f, 1f, 0.75f};     // deep blue
            case "avatar:earth_boulder", "avatar:earth_wall", "avatar:boulder_launch", "avatar:earth_pillar" ->
                    new float[]{0.55f, 0.4f, 0.2f, 0.85f};  // earthy brown
            default -> new float[]{1f, 0.4f, 0.1f, 0.85f};
        };
    }

    private static void renderElementalOrb(MatrixStack matrices, String skillId, float r,
                                           float red, float green, float blue, float alpha) {
        boolean isEarth = "avatar:earth_boulder".equals(skillId)
                || "avatar:earth_wall".equals(skillId)
                || "avatar:boulder_launch".equals(skillId)
                || "avatar:earth_pillar".equals(skillId);
        boolean isFire = "avatar:fire_jab".equals(skillId)
                || "avatar:fire_blast".equals(skillId)
                || "avatar:fire_jet".equals(skillId)
                || "avatar:flame_sweep".equals(skillId);

        Matrix4f mat = matrices.peek().getPositionMatrix();
        long time = System.currentTimeMillis();

        if (isEarth) {
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE_MINUS_SRC_ALPHA);
            RenderSystem.disableCull();
            RenderSystem.enableDepthTest();
            RenderSystem.setShader(GameRenderer::getPositionColorProgram);

            BufferBuilder buf = Tessellator.getInstance().begin(
                    VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

            renderRockyBoulder3rd(buf, mat, r);

            BufferRenderer.drawWithGlobalProgram(buf.end());

            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        } else if (isFire) {
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE);
            RenderSystem.disableCull();
            RenderSystem.disableDepthTest();
            RenderSystem.setShader(GameRenderer::getPositionColorProgram);

            BufferBuilder buf = Tessellator.getInstance().begin(
                    VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

            renderDynamicFlame3rd(buf, mat, r, time);

            BufferRenderer.drawWithGlobalProgram(buf.end());

            RenderSystem.enableDepthTest();
            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        } else {
            renderOrb(matrices, r, red, green, blue, alpha);
        }
    }

    private static void renderDynamicFlame3rd(BufferBuilder buf, Matrix4f mat, float r, long time) {
        int stacks = 10;
        int slices = 14;

        // Core flame
        renderSphereLayer(buf, mat, r * 0.45f, 1.0f, 0.95f, 0.60f, 0.95f, 8, 12);

        // Licking flame tendrils
        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;

            for (int j = 0; j < slices; j++) {
                double theta0 = 2 * Math.PI * j / slices;
                double theta1 = 2 * Math.PI * (j + 1) / slices;

                float wave0 = 1.0f + 0.32f * (float) Math.sin(time * 0.012f + i * 1.6f + j * 2.1f);
                float wave1 = 1.0f + 0.32f * (float) Math.sin(time * 0.012f + (i + 1) * 1.6f + (j + 1) * 2.1f);

                float lift0 = (float) Math.max(0, Math.sin(phi0)) * r * 0.5f;
                float lift1 = (float) Math.max(0, Math.sin(phi1)) * r * 0.5f;

                float r0 = r * wave0 * (float) Math.cos(phi0);
                float r1 = r * wave1 * (float) Math.cos(phi1);
                float y0 = r * wave0 * (float) Math.sin(phi0) + lift0;
                float y1 = r * wave1 * (float) Math.sin(phi1) + lift1;

                float x00 = (float) (r0 * Math.cos(theta0));
                float z00 = (float) (r0 * Math.sin(theta0));
                float x10 = (float) (r1 * Math.cos(theta0));
                float z10 = (float) (r1 * Math.sin(theta0));
                float x01 = (float) (r0 * Math.cos(theta1));
                float z01 = (float) (r0 * Math.sin(theta1));
                float x11 = (float) (r1 * Math.cos(theta1));
                float z11 = (float) (r1 * Math.sin(theta1));

                buf.vertex(mat, x00, y0, z00).color(1.0f, 0.38f, 0.04f, 0.70f);
                buf.vertex(mat, x10, y1, z10).color(1.0f, 0.38f, 0.04f, 0.70f);
                buf.vertex(mat, x11, y1, z11).color(1.0f, 0.38f, 0.04f, 0.70f);
                buf.vertex(mat, x01, y0, z01).color(1.0f, 0.38f, 0.04f, 0.70f);
            }
        }
    }

    private static void renderRockyBoulder3rd(BufferBuilder buf, Matrix4f mat, float r) {
        int stacks = 10;
        int slices = 12;

        for (int i = 0; i < stacks; i++) {
            double phi0 = Math.PI * i / stacks - Math.PI / 2.0;
            double phi1 = Math.PI * (i + 1) / stacks - Math.PI / 2.0;

            for (int j = 0; j < slices; j++) {
                double theta0 = 2 * Math.PI * j / slices;
                double theta1 = 2 * Math.PI * (j + 1) / slices;

                float facet0 = 1.0f + 0.18f * (float) Math.sin(i * 3.3f + j * 4.9f);
                float facet1 = 1.0f + 0.18f * (float) Math.sin((i + 1) * 3.3f + (j + 1) * 4.9f);

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

    /**
     * Renders a 3D volumetric UV-sphere with inner glowing core and smooth outer falloff shell.
     */
    private static void renderOrb(MatrixStack matrices, float r,
                                   float red, float green, float blue, float alpha) {
        RenderSystem.enableBlend();
        RenderSystem.blendFunc(GlStateManager.SrcFactor.SRC_ALPHA, GlStateManager.DstFactor.ONE); // additive glow
        RenderSystem.disableCull();
        RenderSystem.disableDepthTest();
        RenderSystem.setShader(GameRenderer::getPositionColorProgram);

        BufferBuilder buf = Tessellator.getInstance().begin(
                VertexFormat.DrawMode.QUADS, VertexFormats.POSITION_COLOR);

        Matrix4f mat = matrices.peek().getPositionMatrix();

        int stacks = 12;
        int slices = 16;

        // 1. Inner core: bright hot center
        renderSphereLayer(buf, mat, r * 0.55f, 1.0f, 0.95f, 0.85f, Math.min(1.0f, alpha * 1.6f), stacks, slices);

        // 2. Outer shell: element-tinted soft halo
        renderSphereLayer(buf, mat, r, red, green, blue, alpha * 0.75f, stacks, slices);

        BufferRenderer.drawWithGlobalProgram(buf.end());

        RenderSystem.enableDepthTest();
        RenderSystem.enableCull();
        RenderSystem.disableBlend();
    }

    private static void renderSphereLayer(BufferBuilder buf, Matrix4f mat, float r,
                                          float red, float green, float blue, float alpha,
                                          int stacks, int slices) {
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

    private ChargeOrbRenderer() {}
}
