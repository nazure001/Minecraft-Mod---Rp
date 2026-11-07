package com.avatarmod.elements.network;

import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;

public final class AvatarServerEvents {

    public static void register() {
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            AvatarNetworking.onPlayerDisconnect(handler.player.getUuid());
            SkillNetworking.onPlayerDisconnect(handler.player.getUuid());
        });
    }

    private AvatarServerEvents() {}
}
