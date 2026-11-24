package com.avatarmod.elements.item;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.entity.AvatarEntities;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.item.SpawnEggItem;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public final class AvatarItems {

    public static final Item AIR_STAFF = new AirStaffItem();
    public static final Item DUAL_SWORDS = new DualSwordsItem();
    public static final Item EARTH_HAMMER = new EarthHammerItem();
    public static final Item WAR_FAN = new WarFanItem();
    public static final Item WATER_SPEAR = new WaterSpearItem();
    public static final Item AVATAR_SCROLL = new AvatarScrollItem();

    public static final Item SHIRSHU_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.SHIRSHU, 0x2A231D, 0x826E5C, new Item.Settings()
    );
    public static final Item VAATU_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.VAATU_SPIRIT_TITAN, 0x1E0528, 0x8C1111, new Item.Settings()
    );
    public static final Item FLYING_BISON_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.FLYING_BISON, 0xD2C5B5, 0x8C522B, new Item.Settings()
    );
    public static final Item PLATYPUS_BEAR_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.PLATYPUS_BEAR, 0x483321, 0x2A1B0E, new Item.Settings()
    );
    public static final Item PHOENIX_KING_OZAI_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.PHOENIX_KING_OZAI, 0x8C1800, 0xF5A623, new Item.Settings()
    );
    public static final Item WINGED_LEMUR_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.WINGED_LEMUR, 0xFAF0E6, 0x4A3728, new Item.Settings()
    );
    public static final Item TURTLE_DUCK_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.TURTLE_DUCK, 0x2E6B41, 0xF3C053, new Item.Settings()
    );
    public static final Item OTTER_PENGUIN_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.OTTER_PENGUIN, 0x223547, 0xFAF8F5, new Item.Settings()
    );
    public static final Item DAI_LI_AGENT_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.DAI_LI_AGENT, 0x2B472B, 0x5C4D3C, new Item.Settings()
    );
    public static final Item FIRE_NATION_SPEARMAN_SPAWN_EGG = new SpawnEggItem(
            AvatarEntities.FIRE_NATION_SPEARMAN, 0x4A1313, 0xD4AF37, new Item.Settings()
    );

    public static final ItemGroup MAIN_GROUP = FabricItemGroup.builder()
            .icon(() -> new ItemStack(AIR_STAFF))
            .displayName(Text.translatable("itemGroup.avatar_elements.main"))
            .entries((ctx, entries) -> {
                entries.add(AIR_STAFF);
                entries.add(DUAL_SWORDS);
                entries.add(EARTH_HAMMER);
                entries.add(WAR_FAN);
                entries.add(WATER_SPEAR);
                entries.add(AVATAR_SCROLL);
                entries.add(SHIRSHU_SPAWN_EGG);
                entries.add(VAATU_SPAWN_EGG);
                entries.add(FLYING_BISON_SPAWN_EGG);
                entries.add(PLATYPUS_BEAR_SPAWN_EGG);
                entries.add(PHOENIX_KING_OZAI_SPAWN_EGG);
                entries.add(WINGED_LEMUR_SPAWN_EGG);
                entries.add(TURTLE_DUCK_SPAWN_EGG);
                entries.add(OTTER_PENGUIN_SPAWN_EGG);
                entries.add(DAI_LI_AGENT_SPAWN_EGG);
                entries.add(FIRE_NATION_SPEARMAN_SPAWN_EGG);
            })
            .build();

    public static void register() {
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "air_staff"), AIR_STAFF);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "dual_swords"), DUAL_SWORDS);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "earth_hammer"), EARTH_HAMMER);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "war_fan"), WAR_FAN);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "water_spear"), WATER_SPEAR);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "avatar_scroll"), AVATAR_SCROLL);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "shirshu_spawn_egg"), SHIRSHU_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "vaatu_spirit_titan_spawn_egg"), VAATU_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "flying_bison_spawn_egg"), FLYING_BISON_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "platypus_bear_spawn_egg"), PLATYPUS_BEAR_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "phoenix_king_ozai_spawn_egg"), PHOENIX_KING_OZAI_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "winged_lemur_spawn_egg"), WINGED_LEMUR_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "turtle_duck_spawn_egg"), TURTLE_DUCK_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "otter_penguin_spawn_egg"), OTTER_PENGUIN_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "dai_li_agent_spawn_egg"), DAI_LI_AGENT_SPAWN_EGG);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "fire_nation_spearman_spawn_egg"), FIRE_NATION_SPEARMAN_SPAWN_EGG);
        Registry.register(Registries.ITEM_GROUP,
                Identifier.of(AvatarElementsMod.MOD_ID, "main"), MAIN_GROUP);
    }

    private AvatarItems() {}
}
