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
                            client.player.sendMessage(
                                    Text.literal("§a[Avatar] " + payload.skillId() + " — OK"), true);
                        } else {
                            String reason = switch (payload.denyReason()) {
                                case COOLDOWN -> "Cooldown: " + payload.cooldownTicks() + " tik";
                                case NOT_ENOUGH_CHI -> "Chi tidak cukup";
                                case WRONG_MASTERY -> "Mastery tidak cukup";
                                case RATE_LIMITED -> "Terlalu cepat";
                                default -> "Ditolak";
                            };
                            client.player.sendMessage(
                                    Text.literal("§c[Avatar] " + payload.skillId() + " — " + reason), true);
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
    }

    public static void sendSkillInput(String skillId) {
        ClientPlayNetworking.send(new SkillPackets.C2SSkillInput(skillId));
    }

    public static void sendSlotCast(int slotIndex) {
        ClientPlayNetworking.send(new SkillPackets.C2SSlotCast(slotIndex));
    }

    private SkillClientHandler() {}
}
