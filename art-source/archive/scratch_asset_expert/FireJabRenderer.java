package com.avatarmod.elements.client.vfx;

import com.avatarmod.elements.AvatarElementsMod;
import com.mojang.blaze3d.systems.RenderSystem;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.*;
import net.minecraft.client.world.ClientWorld;
import net.minecraft.util.Arm;
import net.minecraft.util.math.Vec3d;
import org.joml.Matrix4f;
import org.joml.Quaternionf;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class FireJabRenderer {
    private static final int FRAME_COUNT = 5;
    private static final long DURATION = 400_000_000L;
    private static final Map<UUID, Cast> casts = new HashMap<>();
    private static Vertex[][] frames;

    private record Vertex(float x, float y, float z, int r, int g, int b) {}
    private record Cast(ClientWorld world, int serial, long start, Vec3d origin, Quaternionf rotation) {}

    public static void register() {
        frames = load();
        WorldRenderEvents.AFTER_ENTITIES.register(FireJabRenderer::render);
    }

    public static void start(UUID uuid, int serial) {
        var world = MinecraftClient.getInstance().world;
        if (frames == null || world == null) return;
        var player = world.getPlayerByUuid(uuid);
        var previous = casts.get(uuid);
        if (player == null || (previous != null && previous.world == world && previous.serial == serial)) return;
        Vec3d look = player.getRotationVec(1);
        Vec3d side = Vec3d.fromPolar(0, player.getYaw() + 90)
                .multiply(player.getMainArm() == Arm.LEFT ? -0.29 : 0.29);
        Vec3d origin = player.getEyePos().add(0, -0.38, 0).add(side).add(look.multiply(0.45));
        Quaternionf rotation = new Quaternionf().rotationTo(0, 0, 1, (float)look.x, (float)look.y, (float)look.z);
        casts.put(uuid, new Cast(world, serial, System.nanoTime(), origin, rotation));
    }

    private static void render(WorldRenderContext context) {
        long now = System.nanoTime();
        casts.values().removeIf(c -> c.world != context.world() || now - c.start >= DURATION);
        if (casts.isEmpty()) return;
        var matrices = context.matrixStack();
        if (matrices == null) return;

        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.depthMask(false);
        RenderSystem.disableCull();
        RenderSystem.setShader(GameRenderer::getPositionColorProgram);
        try {
            for (Cast cast : casts.values()) {
                matrices.push();
                Vec3d offset = cast.origin.subtract(context.camera().getPos());
                matrices.translate(offset.x, offset.y, offset.z);
                matrices.multiply(cast.rotation);
                draw(matrices.peek().getPositionMatrix(), (float)(now - cast.start) / DURATION);
                matrices.pop();
            }
        } finally {
            RenderSystem.depthMask(true);
            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        }
    }

    private static void draw(Matrix4f matrix, float progress) {
        float frame = progress * (FRAME_COUNT - 1);
        int first = Math.min((int) frame, FRAME_COUNT - 2);
        float fraction = frame - first;
        int alpha = Math.round(255 * Math.min(1, (1 - progress) * 3));
        var buf = Tessellator.getInstance().begin(VertexFormat.DrawMode.TRIANGLES, VertexFormats.POSITION_COLOR);
        for (int i = 0; i < frames[first].length; i++) {
            Vertex a = frames[first][i];
            Vertex b = frames[first + 1][i];
            buf.vertex(matrix, a.x + (b.x - a.x) * fraction, a.y + (b.y - a.y) * fraction,
                    a.z + (b.z - a.z) * fraction).color(a.r, a.g, a.b, alpha);
        }
        BufferRenderer.drawWithGlobalProgram(buf.end());
    }

    private static Vertex[][] load() {
        try (var stream = FireJabRenderer.class.getResourceAsStream("/assets/avatar_elements/vfx/fire_jab.bin")) {
            if (stream == null) throw new IOException("Missing Fire Jab mesh");
            var in = new DataInputStream(stream);
            int count = in.readInt();
            if (count <= 0 || count > 10000 || count % 3 != 0) throw new IOException("Invalid Fire Jab mesh");
            Vertex[][] result = new Vertex[FRAME_COUNT][count];
            for (Vertex[] frame : result) {
                for (int i = 0; i < count; i++) {
                    frame[i] = new Vertex(in.readFloat(), in.readFloat(), in.readFloat(),
                            in.readUnsignedByte(), in.readUnsignedByte(), in.readUnsignedByte());
                }
            }
            return result;
        } catch (IOException e) {
            AvatarElementsMod.LOGGER.error("Could not load Fire Jab VFX", e);
            return null;
        }
    }

    private FireJabRenderer() {}
}
