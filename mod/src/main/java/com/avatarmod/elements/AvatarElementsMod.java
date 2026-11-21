package com.avatarmod.elements;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.entity.FireBlastProjectileEntity;
import com.avatarmod.elements.item.AvatarItems;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillRegistry;
import com.avatarmod.elements.sound.ModSounds;
import com.avatarmod.elements.network.AvatarNetworking;
import com.avatarmod.elements.network.AvatarServerEvents;
import com.avatarmod.elements.network.SkillNetworking;
import net.fabricmc.api.ModInitializer;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.SpawnGroup;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AvatarElementsMod implements ModInitializer {
    public static final String MOD_ID = "avatar_elements";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    public static Identifier id(String path) {
        return Identifier.of(MOD_ID, path);
    }

    public static final EntityType<FireBlastProjectileEntity> FIRE_BLAST_PROJECTILE = Registry.register(
            Registries.ENTITY_TYPE,
            id("fire_blast_projectile"),
            EntityType.Builder.<FireBlastProjectileEntity>create(FireBlastProjectileEntity::new, SpawnGroup.MISC)
                    .dimensions(0.5f, 0.5f)
                    .maxTrackingRange(4)
                    .trackingTickInterval(10)
                    .build()
    );

    @Override
    public void onInitialize() {
        LOGGER.info("Avatar: Elements initializing (common)");
        LOGGER.debug("Bending attachment: {}", PlayerBendingData.ATTACHMENT);
        SkillRegistry.populate();
        AvatarItems.register();
        AvatarParticles.init();
        ModSounds.init();
        AvatarNetworking.registerPayloads();
        AvatarNetworking.registerServerReceivers();
        SkillNetworking.registerPayloads();
        SkillNetworking.registerServerReceivers();
        AvatarServerEvents.register();
        com.avatarmod.elements.command.AvatarCommands.register();
    }
}
