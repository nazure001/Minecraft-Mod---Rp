package com.avatarmod.elements;

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AvatarElementsMod implements ModInitializer {

    public static final String MOD_ID = "avatar_elements";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("Avatar: Elements initializing (common)");
        // T1-2: KeyBindings registered in client entry point
        // T1-3: Networking packets registered here (C2S/S2C)
        // T1-4: PlayerBendingData AttachmentType registered here
        // T1-5: SkillTimeline / SkillRegistry registered here
    }
}
