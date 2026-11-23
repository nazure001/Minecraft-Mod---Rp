package com.avatarmod.elements.entity;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.entity.boss.VaatuSpiritTitanEntity;
import com.avatarmod.elements.entity.mob.ShirshuEntity;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.SpawnGroup;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;

public final class AvatarEntities {

    public static final EntityType<ShirshuEntity> SHIRSHU = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("shirshu"),
            EntityType.Builder.<ShirshuEntity>create(ShirshuEntity::new, SpawnGroup.MONSTER)
                    .dimensions(1.8f, 1.4f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<VaatuSpiritTitanEntity> VAATU_SPIRIT_TITAN = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("vaatu_spirit_titan"),
            EntityType.Builder.<VaatuSpiritTitanEntity>create(VaatuSpiritTitanEntity::new, SpawnGroup.MONSTER)
                    .dimensions(3.2f, 4.5f)
                    .maxTrackingRange(10)
                    .trackingTickInterval(3)
                    .build()
    );

    public static void init() {
        FabricDefaultAttributeRegistry.register(SHIRSHU, ShirshuEntity.createShirshuAttributes());
        FabricDefaultAttributeRegistry.register(VAATU_SPIRIT_TITAN, VaatuSpiritTitanEntity.createVaatuAttributes());
    }

    private AvatarEntities() {}
}
