package com.avatarmod.elements.client;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.client.hud.AvatarHudRenderer;
import com.avatarmod.elements.client.hud.ElementWheelRenderer;
import com.avatarmod.elements.client.input.AvatarKeyBindings;
import com.avatarmod.elements.client.network.ClientNetworkHandler;
import com.avatarmod.elements.client.network.SkillClientHandler;
import com.avatarmod.elements.network.SkillPackets;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.util.InputUtil;

public class AvatarElementsClient implements ClientModInitializer {

    private static boolean wheelWasOpen = false;

    @Override
    public void onInitializeClient() {
        AvatarElementsMod.LOGGER.info("Avatar: Elements initializing (client)");
        AvatarKeyBindings.register();
        ClientNetworkHandler.register();
        SkillClientHandler.register();
        AvatarHudRenderer.register();

        // Wheel render (only when R is held)
        HudRenderCallback.EVENT.register((context, tickCounter) -> {
            if (isWheelOpen()) {
                ElementWheelRenderer.render(context, tickCounter);
            }
        });

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;

            // --- Element wheel (hold R) ---
            boolean wheelOpen = isWheelOpen();
            if (!wheelOpen && wheelWasOpen) {
                // Key just released — send selected element to server
                String chosen = ElementWheelRenderer.getHovered();
                ClientPlayNetworking.send(new SkillPackets.C2SSetElement(chosen));
            }
            wheelWasOpen = wheelOpen;

            // --- Skill slot keys (Z/X/C/V) ---
            if (wheelOpen) return; // ignore slot presses while wheel is open

            while (AvatarKeyBindings.SLOT_1.wasPressed()) {
                SkillClientHandler.sendSlotCast(0);
            }
            while (AvatarKeyBindings.SLOT_2.wasPressed()) {
                SkillClientHandler.sendSlotCast(1);
            }
            while (AvatarKeyBindings.SLOT_3.wasPressed()) {
                SkillClientHandler.sendSlotCast(2);
            }
            while (AvatarKeyBindings.SLOT_4.wasPressed()) {
                SkillClientHandler.sendSlotCast(3);
            }
        });
    }

    private static boolean isWheelOpen() {
        var client = net.minecraft.client.MinecraftClient.getInstance();
        if (client.getWindow() == null) return false;
        return InputUtil.isKeyPressed(client.getWindow().getHandle(),
                net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper
                        .getBoundKeyOf(AvatarKeyBindings.ELEMENT_WHEEL).getCode());
    }
}
