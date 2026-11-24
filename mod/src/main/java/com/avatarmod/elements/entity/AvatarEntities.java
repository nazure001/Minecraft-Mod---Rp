package com.avatarmod.elements.entity;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.entity.boss.PhoenixKingOzaiEntity;
import com.avatarmod.elements.entity.boss.VaatuSpiritTitanEntity;
import com.avatarmod.elements.entity.mob.*;
import com.avatarmod.elements.entity.pet.FlyingBisonEntity;
import com.avatarmod.elements.entity.pet.WingedLemurEntity;
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

    public static final EntityType<FlyingBisonEntity> FLYING_BISON = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("flying_bison"),
            EntityType.Builder.<FlyingBisonEntity>create(FlyingBisonEntity::new, SpawnGroup.CREATURE)
                    .dimensions(3.0f, 2.6f)
                    .maxTrackingRange(10)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<PlatypusBearEntity> PLATYPUS_BEAR = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("platypus_bear"),
            EntityType.Builder.<PlatypusBearEntity>create(PlatypusBearEntity::new, SpawnGroup.MONSTER)
                    .dimensions(1.9f, 1.6f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<PhoenixKingOzaiEntity> PHOENIX_KING_OZAI = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("phoenix_king_ozai"),
            EntityType.Builder.<PhoenixKingOzaiEntity>create(PhoenixKingOzaiEntity::new, SpawnGroup.MONSTER)
                    .dimensions(0.9f, 2.2f)
                    .maxTrackingRange(10)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<WingedLemurEntity> WINGED_LEMUR = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("winged_lemur"),
            EntityType.Builder.<WingedLemurEntity>create(WingedLemurEntity::new, SpawnGroup.CREATURE)
                    .dimensions(0.6f, 0.7f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<TurtleDuckEntity> TURTLE_DUCK = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("turtle_duck"),
            EntityType.Builder.<TurtleDuckEntity>create(TurtleDuckEntity::new, SpawnGroup.CREATURE)
                    .dimensions(0.7f, 0.5f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<OtterPenguinEntity> OTTER_PENGUIN = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("otter_penguin"),
            EntityType.Builder.<OtterPenguinEntity>create(OtterPenguinEntity::new, SpawnGroup.CREATURE)
                    .dimensions(0.8f, 1.0f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<DaiLiAgentEntity> DAI_LI_AGENT = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("dai_li_agent"),
            EntityType.Builder.<DaiLiAgentEntity>create(DaiLiAgentEntity::new, SpawnGroup.MONSTER)
                    .dimensions(0.6f, 1.9f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static final EntityType<FireNationSpearmanEntity> FIRE_NATION_SPEARMAN = Registry.register(
            Registries.ENTITY_TYPE,
            AvatarElementsMod.id("fire_nation_spearman"),
            EntityType.Builder.<FireNationSpearmanEntity>create(FireNationSpearmanEntity::new, SpawnGroup.MONSTER)
                    .dimensions(0.6f, 1.9f)
                    .maxTrackingRange(8)
                    .trackingTickInterval(3)
                    .build()
    );

    public static void init() {
        FabricDefaultAttributeRegistry.register(SHIRSHU, ShirshuEntity.createShirshuAttributes());
        FabricDefaultAttributeRegistry.register(VAATU_SPIRIT_TITAN, VaatuSpiritTitanEntity.createVaatuAttributes());
        FabricDefaultAttributeRegistry.register(FLYING_BISON, FlyingBisonEntity.createBisonAttributes());
        FabricDefaultAttributeRegistry.register(PLATYPUS_BEAR, PlatypusBearEntity.createPlatypusBearAttributes());
        FabricDefaultAttributeRegistry.register(PHOENIX_KING_OZAI, PhoenixKingOzaiEntity.createOzaiAttributes());
        FabricDefaultAttributeRegistry.register(WINGED_LEMUR, WingedLemurEntity.createLemurAttributes());
        FabricDefaultAttributeRegistry.register(TURTLE_DUCK, TurtleDuckEntity.createTurtleDuckAttributes());
        FabricDefaultAttributeRegistry.register(OTTER_PENGUIN, OtterPenguinEntity.createOtterPenguinAttributes());
        FabricDefaultAttributeRegistry.register(DAI_LI_AGENT, DaiLiAgentEntity.createDaiLiAttributes());
        FabricDefaultAttributeRegistry.register(FIRE_NATION_SPEARMAN, FireNationSpearmanEntity.createSpearmanAttributes());
    }

    private AvatarEntities() {}
}
