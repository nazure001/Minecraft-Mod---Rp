package com.avatarmod.elements.client.network;

import com.avatarmod.elements.client.hud.HudState;
import com.avatarmod.elements.network.SkillPackets;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;

public final class SkillClientHandler {

    public static void register() {
        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CSkillResult.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        if (client.player == null) return;
                        if (payload.allowed()) {
                            // Suppress spammy actionbar notifications on every cast; only log in debug mode
                            if (Boolean.getBoolean("avatar.debug.network")) {
                                client.player.sendMessage(
                                        Text.literal("§a[Avatar] " + payload.skillId() + " — OK"), true);
                            }
                        } else {
                            // Rate limited is an internal throttle; never display "Terlalu cepat" error spam
                            if (payload.denyReason() == SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED) {
                                return;
                            }
                            String reason = switch (payload.denyReason()) {
                                case COOLDOWN -> {
                                    float sec = payload.cooldownTicks() / 20.0f;
                                    yield sec >= 1.0f ? String.format(java.util.Locale.ROOT, "Cooldown: %.1fs", sec)
                                                      : "Cooldown: " + payload.cooldownTicks() + " tik";
                                }
                                case NOT_ENOUGH_CHI -> "Chi tidak cukup";
                                case WRONG_MASTERY -> "Mastery tidak cukup";
                                default -> null;
                            };
                            if (reason != null) {
                                client.player.sendMessage(
                                        Text.literal("§c[Avatar] " + reason), true);
                            }
                        }
                    });
                });

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CHudUpdate.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        HudState.update(
                                payload.currentChi(),
                                payload.maxChi(),
                                payload.activeCooldownSkillId(),
                                payload.cooldownTicksRemaining());
                    });
                });

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CSyncElement.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        com.avatarmod.elements.client.hud.ElementWheelRenderer.setElement(payload.element());
                    });
                });

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CSyncBosses.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        com.avatarmod.elements.client.hud.HudState.updateDefeatedBosses(payload.bossesCommaSeparated());
                    });
                });

        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CPillarAction.ID,
                (payload, context) -> {
                    MinecraftClient client = context.client();
                    client.execute(() -> {
                        com.avatarmod.elements.client.vfx.CinematicVfxController.onPillarAction(
                                payload.casterUuid(), payload.actionType(),
                                payload.x(), payload.y(), payload.z(),
                                payload.dirX(), payload.dirY(), payload.dirZ()
                        );
                    });
                });
    }

    public static void sendPillarInteract(int actionType) {
        ClientPlayNetworking.send(new SkillPackets.C2SPillarInteract(actionType));
    }

    public static void sendSkillInput(String skillId) {
        ClientPlayNetworking.send(new SkillPackets.C2SSkillInput(skillId));
    }

    public static void sendSlotCast(int slotIndex) {
        ClientPlayNetworking.send(new SkillPackets.C2SSlotCast(slotIndex));
    }

    public static void selectElement(String element) {
        ClientPlayNetworking.send(new SkillPackets.C2SSelectElement(element));
    }

    public static void sendHoldStart(int slotIndex, String skillId) {
        ClientPlayNetworking.send(new SkillPackets.C2SHoldStart(slotIndex, skillId));
    }

    public static void sendHoldRelease(int slotIndex, String skillId) {
        ClientPlayNetworking.send(new SkillPackets.C2SHoldRelease(slotIndex, skillId));
    }

    private SkillClientHandler() {}
}
