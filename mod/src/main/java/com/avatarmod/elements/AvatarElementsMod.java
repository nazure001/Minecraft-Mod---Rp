package com.avatarmod.elements;

import com.avatarmod.elements.network.AvatarNetworking;
import com.avatarmod.elements.network.AvatarServerEvents;
import com.avatarmod.elements.network.SkillNetworking;
import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AvatarElementsMod implements ModInitializer {
    public static final String MOD_ID = "avatar_elements";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("Avatar: Elements initializing (common)");
        AvatarNetworking.registerPayloads();
        AvatarNetworking.registerServerReceivers();
        SkillNetworking.registerPayloads();
        SkillNetworking.registerServerReceivers();
        AvatarServerEvents.register();
    }
}
