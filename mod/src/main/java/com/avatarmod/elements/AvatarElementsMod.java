package com.avatarmod.elements;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.item.AvatarItems;
import com.avatarmod.elements.skill.SkillRegistry;
import com.avatarmod.elements.network.AvatarNetworking;
import com.avatarmod.elements.network.AvatarServerEvents;
import com.avatarmod.elements.network.SkillNetworking;
import net.fabricmc.api.ModInitializer;
import net.minecraft.util.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AvatarElementsMod implements ModInitializer {
    public static final String MOD_ID = "avatar_elements";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    public static Identifier id(String path) {
        return Identifier.of(MOD_ID, path);
    }

    @Override
    public void onInitialize() {
        LOGGER.info("Avatar: Elements initializing (common)");
        LOGGER.debug("Bending attachment: {}", PlayerBendingData.ATTACHMENT);
        SkillRegistry.populate();
        AvatarItems.register();
        AvatarNetworking.registerPayloads();
        AvatarNetworking.registerServerReceivers();
        SkillNetworking.registerPayloads();
        SkillNetworking.registerServerReceivers();
        AvatarServerEvents.register();
    }
}
