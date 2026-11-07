package com.avatarmod.elements.client;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.api.ClientModInitializer;

public class AvatarElementsClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        AvatarElementsMod.LOGGER.info("Avatar: Elements initializing (client)");
        // T1-2: KeyBindings.register() goes here
        // T1-8: HudRenderer.register() goes here
    }
}
