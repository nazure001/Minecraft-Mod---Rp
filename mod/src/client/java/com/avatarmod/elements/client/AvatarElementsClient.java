package com.avatarmod.elements.client;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.client.anim.AvatarAnimations;
import com.avatarmod.elements.client.hud.AvatarHudRenderer;
import com.avatarmod.elements.client.hud.ElementWheelRenderer;
import com.avatarmod.elements.client.input.AvatarKeyBindings;
import com.avatarmod.elements.client.network.ClientNetworkHandler;
import com.avatarmod.elements.client.network.SkillClientHandler;
import com.avatarmod.elements.client.orb.ChargeOrbRenderer;
import com.avatarmod.elements.client.orb.FirstPersonOrbRenderer;
import com.avatarmod.elements.network.SkillPackets;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;

public class AvatarElementsClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        AvatarElementsMod.LOGGER.info("Avatar: Elements initializing (client)");
        AvatarAnimations.register();
        AvatarKeyBindings.register();
        ClientNetworkHandler.register();
        SkillClientHandler.register();
        AvatarHudRenderer.register();
        ChargeOrbRenderer.register();
        FirstPersonOrbRenderer.register();

        // Show current element in action bar (simple HUD)
        HudRenderCallback.EVENT.register((context, tickCounter) -> {
            ElementWheelRenderer.renderCurrentElement(context);
        });

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;

            // --- Element wheel: press R once → cycle to next element ---
            if (drainPressed(AvatarKeyBindings.ELEMENT_WHEEL)) {
                String next = ElementWheelRenderer.cycleElement();
                ClientPlayNetworking.send(new SkillPackets.C2SSetElement(next));
            }

            // --- Skill slot keys (Z/X/C/V) ---
            // Drain OS key-repeat events but send only ONE cast per tick.
            if (drainPressed(AvatarKeyBindings.SLOT_1)) SkillClientHandler.sendSlotCast(0);
            if (drainPressed(AvatarKeyBindings.SLOT_2)) SkillClientHandler.sendSlotCast(1);
            if (drainPressed(AvatarKeyBindings.SLOT_3)) SkillClientHandler.sendSlotCast(2);
            if (drainPressed(AvatarKeyBindings.SLOT_4)) SkillClientHandler.sendSlotCast(3);
        });
    }

    /** Drain all queued key-press events; return true if at least one was queued. */
    private static boolean drainPressed(net.minecraft.client.option.KeyBinding key) {
        boolean any = false;
        while (key.wasPressed()) any = true;
        return any;
    }

}
