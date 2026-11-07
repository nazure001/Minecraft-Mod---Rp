package com.avatarmod.elements.client.network;

import com.avatarmod.elements.client.orb.ChargeOrbClientState;
import com.avatarmod.elements.network.SkillPackets;
import com.avatarmod.elements.network.TestActionPackets;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;

public final class ClientNetworkHandler {

    public static void register() {
        ClientPlayNetworking.registerGlobalReceiver(
                SkillPackets.S2CPhaseSync.ID,
                (payload, context) -> {
                    context.client().execute(() ->
                            ChargeOrbClientState.update(
                                    payload.casterUuid(),
                                    payload.skillId(),
                                    payload.phase(),
                                    payload.ticksIn(),
                                    payload.castSerial()
                            )
                    );
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
