package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class AvatarNetworking {

    // Minimum ticks between test actions per player (20 ticks = 1 second)
    private static final int RATE_LIMIT_TICKS = 20;

    private static final Map<UUID, Long> lastActionTick = new HashMap<>();

    public static void registerPayloads() {
        PayloadTypeRegistry.playC2S().register(
                TestActionPackets.C2STestAction.ID,
                TestActionPackets.C2STestAction.CODEC);
        PayloadTypeRegistry.playS2C().register(
                TestActionPackets.S2CAck.ID,
                TestActionPackets.S2CAck.CODEC);
    }

    public static void registerServerReceivers() {
        ServerPlayNetworking.registerGlobalReceiver(
                TestActionPackets.C2STestAction.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    long currentTick = player.getServerWorld().getTime();
                    UUID uuid = player.getUuid();

                    long lastTick = lastActionTick.getOrDefault(uuid, -RATE_LIMIT_TICKS - 1L);
                    long ticksSinceLast = currentTick - lastTick;

                    if (ticksSinceLast < RATE_LIMIT_TICKS) {
                        int remaining = (int) (RATE_LIMIT_TICKS - ticksSinceLast);
                        AvatarElementsMod.LOGGER.debug(
                                "Rate-limited test action for {} ({} ticks remaining)",
                                player.getName().getString(), remaining);
                        ServerPlayNetworking.send(player,
                                new TestActionPackets.S2CAck(false, remaining));
                        return;
                    }

                    lastActionTick.put(uuid, currentTick);
                    AvatarElementsMod.LOGGER.info(
                            "Test action received from {}", player.getName().getString());
                    player.sendMessage(
                            Text.literal("[Avatar] Server: test action acknowledged."), false);
                    ServerPlayNetworking.send(player,
                            new TestActionPackets.S2CAck(true, 0));
                });
    }

    /** Call on player disconnect to free memory. */
    public static void onPlayerDisconnect(UUID uuid) {
        lastActionTick.remove(uuid);
    }

    private AvatarNetworking() {}
}
