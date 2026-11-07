package com.avatarmod.elements.client;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.client.hud.AvatarHudRenderer;
import com.avatarmod.elements.client.input.AvatarKeyBindings;
import com.avatarmod.elements.client.network.ClientNetworkHandler;
import com.avatarmod.elements.client.network.SkillClientHandler;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;

public class AvatarElementsClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        AvatarElementsMod.LOGGER.info("Avatar: Elements initializing (client)");
        AvatarKeyBindings.register();
        ClientNetworkHandler.register();
        SkillClientHandler.register();
        AvatarHudRenderer.register();

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;
            // T1-2 test action (key R)
            while (AvatarKeyBindings.TEST_ACTION.wasPressed()) {
                ClientNetworkHandler.sendTestAction();
            }
            // T1-3 skill input test (key G → fire_jab)
            while (AvatarKeyBindings.SKILL_FIRE_JAB.wasPressed()) {
                SkillClientHandler.sendSkillInput("avatar:fire_jab");
            }
            // T2-6 air staff combo (key H)
            while (AvatarKeyBindings.SKILL_AIR_STAFF.wasPressed()) {
                SkillClientHandler.sendSkillInput("avatar:air_staff_attack");
            }
            // T2-7 air vortex (key V)
            while (AvatarKeyBindings.SKILL_AIR_VORTEX.wasPressed()) {
                SkillClientHandler.sendSkillInput("avatar:air_vortex");
            }
        });
    }
}
