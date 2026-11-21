package com.avatarmod.elements.client.network;

import com.avatarmod.elements.client.anim.AvatarAnimations;
import com.avatarmod.elements.client.orb.ChargeOrbClientState;
import com.avatarmod.elements.client.vfx.CinematicVfxController;
import com.avatarmod.elements.network.SkillPackets;
import com.avatarmod.elements.network.TestActionPackets;
import com.avatarmod.elements.skill.CastAnimationGate;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientWorldEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.text.Text;

public final class ClientNetworkHandler {

    private static final CastAnimationGate CAST_ANIMATION_GATE = new CastAnimationGate();

    public static void register() {
        ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> CAST_ANIMATION_GATE.clear());
        ClientPlayConnectionEvents.JOIN.register((handler, sender, client) -> CAST_ANIMATION_GATE.clear());
        ClientWorldEvents.AFTER_CLIENT_WORLD_CHANGE.register((client, world) -> CAST_ANIMATION_GATE.clear());

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CPhaseSync.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        ChargeOrbClientState.update(
                                payload.casterUuid(),
                                payload.skillId(),
                                payload.phase(),
                                payload.ticksIn(),
                                payload.castSerial()
                        );

                        // Route phase sync to client Display Entity Cinematic VFX controller
                        CinematicVfxController.onPhaseSync(
                                payload.casterUuid(),
                                payload.skillId(),
                                payload.phase(),
                                payload.ticksIn(),
                                payload.castSerial()
                        );

                        if (client.world != null) {
                            var player = client.world.getPlayerByUuid(payload.casterUuid());
                            if (player == null && client.player != null && client.player.getUuid().equals(payload.casterUuid())) {
                                player = client.player;
                            }
                            if (player instanceof AbstractClientPlayerEntity acp) {
                                if ("IDLE".equals(payload.phase())) {
                                    AvatarAnimations.stopAnimation(acp);
                                } else if (CAST_ANIMATION_GATE.shouldStart(
                                        payload.casterUuid(), payload.castSerial(), payload.phase())) {
                                    AvatarAnimations.triggerSkillAnimation(acp, payload.skillId(), payload.phase());
                                    if (acp == client.player) {
                                        client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                                        if ("ACTIVE".equals(payload.phase())) {
                                            if ("avatar:avatar_state".equals(payload.skillId())) {
                                                com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerCinematicOrbit(5.0f, 40);
                                                com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerShake(1.0f, 25);
                                            } else if (payload.skillId().contains("pillar") || payload.skillId().contains("boulder") || payload.skillId().contains("vortex")) {
                                                com.avatarmod.elements.client.camera.AvatarCameraDirector.triggerShake(0.5f, 10);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    });
                });

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CSkillPosition.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> CinematicVfxController.onSkillPosition(
                            payload.casterUuid(), payload.castSerial(),
                            payload.skillId(), payload.x(), payload.y(), payload.z()
                    ));
                });

        ClientPlayNetworking.registerGlobalReceiver(
                TestActionPackets.S2CAck.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        if (client.player == null) return;
                        if (payload.allowed()) {
                            client.player.sendMessage(
                                    Text.literal("§a[Avatar] Aksi berhasil!"), true);
                        } else {
                            client.player.sendMessage(
                                    Text.literal("§c[Avatar] Cooldown: " + payload.cooldownTicks() + " tik"), true);
                        }
                    });
                });
    }

    public static void sendTestAction() {
        ClientPlayNetworking.send(new TestActionPackets.C2STestAction());
    }

    private ClientNetworkHandler() {}
}
