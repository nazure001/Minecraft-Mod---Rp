package com.avatarmod.elements.command;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.network.AvatarServerEvents;
import com.avatarmod.elements.network.SkillNetworking;
import com.avatarmod.elements.skill.ElementSlotMap;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.command.CommandRegistryAccess;
import net.minecraft.command.argument.EntityArgumentType;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.SpawnReason;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.passive.IronGolemEntity;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.command.CommandManager;
import net.minecraft.server.command.ServerCommandSource;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.text.Text;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

import static net.minecraft.server.command.CommandManager.argument;
import static net.minecraft.server.command.CommandManager.literal;

public final class AvatarCommands {

    public static void register() {
        CommandRegistrationCallback.EVENT.register(AvatarCommands::registerCommands);
    }

    private static void registerCommands(CommandDispatcher<ServerCommandSource> dispatcher,
                                         CommandRegistryAccess registryAccess,
                                         CommandManager.RegistrationEnvironment environment) {
        dispatcher.register(literal("avatar")
                // /avatar bypass or /avatar unlimited_chi
                .then(literal("bypass")
                        .executes(ctx -> toggleSandboxBypass(ctx.getSource(), ctx.getSource().getPlayerOrThrow()))
                        .then(argument("target", EntityArgumentType.player())
                                .requires(source -> source.hasPermissionLevel(2))
                                .executes(ctx -> toggleSandboxBypass(ctx.getSource(), EntityArgumentType.getPlayer(ctx, "target")))))
                .then(literal("unlimited_chi")
                        .executes(ctx -> toggleSandboxBypass(ctx.getSource(), ctx.getSource().getPlayerOrThrow()))
                        .then(argument("target", EntityArgumentType.player())
                                .requires(source -> source.hasPermissionLevel(2))
                                .executes(ctx -> toggleSandboxBypass(ctx.getSource(), EntityArgumentType.getPlayer(ctx, "target")))))

                // /avatar element <FIRE|AIR|WATER|EARTH|NON_BENDER>
                .then(literal("element")
                        .then(argument("name", StringArgumentType.word())
                                .suggests((context, builder) -> {
                                    for (String elem : ElementSlotMap.ELEMENTS) {
                                        builder.suggest(elem);
                                    }
                                    return builder.buildFuture();
                                })
                                .executes(ctx -> setElement(ctx.getSource(), ctx.getSource().getPlayerOrThrow(),
                                        StringArgumentType.getString(ctx, "name")))))

                // /avatar mastery <0..5>
                .then(literal("mastery")
                        .then(argument("level", IntegerArgumentType.integer(0, 5))
                                .executes(ctx -> setMastery(ctx.getSource(), ctx.getSource().getPlayerOrThrow(),
                                        IntegerArgumentType.getInteger(ctx, "level")))))

                // /avatar state [durationSeconds]
                .then(literal("state")
                        .executes(ctx -> triggerAvatarState(ctx.getSource(), ctx.getSource().getPlayerOrThrow(), 35))
                        .then(argument("seconds", IntegerArgumentType.integer(5, 300))
                                .executes(ctx -> triggerAvatarState(ctx.getSource(), ctx.getSource().getPlayerOrThrow(),
                                        IntegerArgumentType.getInteger(ctx, "seconds")))))

                // /avatar chi [amount]
                .then(literal("chi")
                        .then(argument("amount", IntegerArgumentType.integer(0, 1000))
                                .executes(ctx -> setChi(ctx.getSource(), ctx.getSource().getPlayerOrThrow(),
                                        IntegerArgumentType.getInteger(ctx, "amount")))))

                // /avatar spawn_boss <fire|air|water|earth>
                .then(literal("spawn_boss")
                        .requires(source -> source.hasPermissionLevel(2))
                        .then(argument("boss_type", StringArgumentType.word())
                                .suggests((context, builder) -> {
                                    builder.suggest("fire");
                                    builder.suggest("air");
                                    builder.suggest("water");
                                    builder.suggest("earth");
                                    return builder.buildFuture();
                                })
                                .executes(ctx -> spawnBoss(ctx.getSource(), StringArgumentType.getString(ctx, "boss_type")))))

                // /avatar boss_vs_boss <boss1> <boss2>
                .then(literal("boss_vs_boss")
                        .requires(source -> source.hasPermissionLevel(2))
                        .then(argument("boss1", StringArgumentType.word())
                                .suggests((context, builder) -> {
                                    builder.suggest("fire");
                                    builder.suggest("earth");
                                    builder.suggest("water");
                                    builder.suggest("air");
                                    return builder.buildFuture();
                                })
                                .then(argument("boss2", StringArgumentType.word())
                                        .suggests((context, builder) -> {
                                            builder.suggest("earth");
                                            builder.suggest("fire");
                                            builder.suggest("air");
                                            builder.suggest("water");
                                            return builder.buildFuture();
                                        })
                                        .executes(ctx -> triggerBossVsBoss(ctx.getSource(),
                                                StringArgumentType.getString(ctx, "boss1"),
                                                StringArgumentType.getString(ctx, "boss2"))))))
        );
    }

    private static int toggleSandboxBypass(ServerCommandSource source, ServerPlayerEntity player) {
        PlayerBendingData data = PlayerBendingData.get(player);
        data.toggleSandboxBypass();
        boolean active = data.isSandboxBypass();

        if (active) {
            data.setChi(data.getMaxChi());
            source.sendFeedback(() -> Text.literal("§a[Avatar Creative] Mode Percobaan Sandbox AKTIF: Unlimited Chi, Zero Cooldown, Instant Mastery Bypass!"), true);
        } else {
            source.sendFeedback(() -> Text.literal("§e[Avatar Creative] Mode Percobaan Sandbox NONAKTIF. Aturan survival normal dipulihkan."), true);
        }
        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        return 1;
    }

    private static int setElement(ServerCommandSource source, ServerPlayerEntity player, String elemInput) {
        String match = null;
        for (String elem : ElementSlotMap.ELEMENTS) {
            if (elem.equalsIgnoreCase(elemInput)) {
                match = elem;
                break;
            }
        }
        if (match == null) {
            source.sendError(Text.literal("§cElemen tidak dikenal: " + elemInput + ". Pilihan: FIRE, AIR, WATER, EARTH, NON_BENDER"));
            return 0;
        }

        PlayerBendingData data = PlayerBendingData.get(player);
        data.setActiveElement(match);
        String finalMatch = match;
        source.sendFeedback(() -> Text.literal("§a[Avatar] Elemen aktif disetel ke: §e" + finalMatch), true);
        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        return 1;
    }

    private static int setMastery(ServerCommandSource source, ServerPlayerEntity player, int level) {
        PlayerBendingData data = PlayerBendingData.get(player);
        data.setMasteryLevel(level);
        source.sendFeedback(() -> Text.literal("§a[Avatar] Tingkat Mastery disetel ke: §eTier " + level), true);
        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        return 1;
    }

    private static int triggerAvatarState(ServerCommandSource source, ServerPlayerEntity player, int seconds) {
        AvatarServerEvents.triggerAvatarState(player, seconds * 20, false);
        source.sendFeedback(() -> Text.literal("§6[Avatar] Membangkitkan Avatar State selama " + seconds + " detik!"), true);
        return 1;
    }

    private static int setChi(ServerCommandSource source, ServerPlayerEntity player, int amount) {
        PlayerBendingData data = PlayerBendingData.get(player);
        data.setChi(amount);
        source.sendFeedback(() -> Text.literal("§b[Avatar] Chi disetel ke: " + amount), true);
        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        return 1;
    }

    private static int spawnBoss(ServerCommandSource source, String bossType) {
        ServerPlayerEntity player = source.getPlayer();
        ServerWorld world = source.getWorld();
        Vec3d spawnPos = player != null ? player.getPos().add(player.getRotationVector().multiply(5))
                : source.getPosition();

        IronGolemEntity boss = createElementalBoss(world, bossType, spawnPos);
        if (boss != null) {
            world.spawnEntity(boss);
            source.sendFeedback(() -> Text.literal("§6[Avatar Arena] Mini-Boss " + boss.getCustomName().getString() + " berhasil di-spawn!"), true);
            return 1;
        }
        return 0;
    }

    private static int triggerBossVsBoss(ServerCommandSource source, String type1, String type2) {
        ServerWorld world = source.getWorld();
        Vec3d center = source.getPosition();

        Vec3d pos1 = center.add(-6, 0, 0);
        Vec3d pos2 = center.add(6, 0, 0);

        IronGolemEntity boss1 = createElementalBoss(world, type1, pos1);
        IronGolemEntity boss2 = createElementalBoss(world, type2, pos2);

        if (boss1 == null || boss2 == null) {
            source.sendError(Text.literal("§cGagal membuat bos untuk pertarungan Boss vs Boss!"));
            return 0;
        }

        world.spawnEntity(boss1);
        world.spawnEntity(boss2);

        // Set rivalry: force both entities to target each other
        boss1.setTarget(boss2);
        boss2.setTarget(boss1);

        // Spawn arena ground sparks
        for (int i = 0; i < 30; i++) {
            world.spawnParticles(ParticleTypes.SOUL_FIRE_FLAME, center.x, center.y + 0.1, center.z, 2, 4.0, 0.2, 4.0, 0.05);
            world.spawnParticles(ParticleTypes.FLASH, center.x, center.y + 1.0, center.z, 1, 0, 0, 0, 0);
        }

        source.sendFeedback(() -> Text.literal("§4§l[ARENA BATTLE] §e" + boss1.getCustomName().getString()
                + " §cVS §b" + boss2.getCustomName().getString() + " §4DIMULAI!"), true);
        return 1;
    }

    private static IronGolemEntity createElementalBoss(ServerWorld world, String type, Vec3d pos) {
        IronGolemEntity golem = EntityType.IRON_GOLEM.create(world);
        if (golem == null) return null;

        golem.refreshPositionAndAngles(pos.x, pos.y, pos.z, 0f, 0f);

        // Max health & stats scaling for raid boss durability
        var healthAttr = golem.getAttributeInstance(EntityAttributes.GENERIC_MAX_HEALTH);
        if (healthAttr != null) healthAttr.setBaseValue(300.0);
        golem.setHealth(300.0f);

        var attackAttr = golem.getAttributeInstance(EntityAttributes.GENERIC_ATTACK_DAMAGE);
        if (attackAttr != null) attackAttr.setBaseValue(18.0);

        var speedAttr = golem.getAttributeInstance(EntityAttributes.GENERIC_MOVEMENT_SPEED);
        if (speedAttr != null) speedAttr.setBaseValue(0.32);

        String normalized = type.toLowerCase(java.util.Locale.ROOT);
        switch (normalized) {
            case "fire" -> {
                golem.setCustomName(Text.literal("§c§l[Boss] Fire Lord Ozai"));
                golem.setCustomNameVisible(true);
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.FIRE_RESISTANCE, 999999, 0, false, false));
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.GLOWING, 999999, 0, false, false));
            }
            case "water" -> {
                golem.setCustomName(Text.literal("§9§l[Boss] Master Pakku"));
                golem.setCustomNameVisible(true);
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.REGENERATION, 999999, 1, false, false));
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.DOLPHINS_GRACE, 999999, 0, false, false));
            }
            case "earth" -> {
                golem.setCustomName(Text.literal("§2§l[Boss] King Bumi"));
                golem.setCustomNameVisible(true);
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.RESISTANCE, 999999, 1, false, false));
                var armorAttr = golem.getAttributeInstance(EntityAttributes.GENERIC_ARMOR);
                if (armorAttr != null) armorAttr.setBaseValue(12.0);
            }
            case "air" -> {
                golem.setCustomName(Text.literal("§f§l[Boss] Monk Gyatso"));
                golem.setCustomNameVisible(true);
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.SPEED, 999999, 2, false, false));
                golem.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOW_FALLING, 999999, 0, false, false));
            }
            default -> {
                golem.setCustomName(Text.literal("§5§l[Boss] Corrupted Elemental Titan"));
                golem.setCustomNameVisible(true);
            }
        }

        return golem;
    }

    private AvatarCommands() {}
}
