package com.avatarmod.elements.network;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDispatcher;
import com.avatarmod.elements.skill.impl.BoulderLaunchSkill;
import com.avatarmod.elements.skill.impl.EarthBoulderSkill;
import com.avatarmod.elements.skill.impl.EarthPillarSkill;
import com.avatarmod.elements.skill.impl.FireBlastSkill;
import com.avatarmod.elements.skill.impl.FireGuardSkill;
import net.fabricmc.fabric.api.entity.event.v1.ServerEntityWorldChangeEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.player.AttackBlockCallback;
import net.fabricmc.fabric.api.event.player.AttackEntityCallback;
import net.fabricmc.fabric.api.networking.v1.EntityTrackingEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.damage.DamageTypes;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.ActionResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public final class AvatarServerEvents {

    public static void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayerEntity player = handler.player;
            PlayerBendingData data = PlayerBendingData.get(player);
            SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        });

        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            AvatarNetworking.onPlayerDisconnect(handler.player.getUuid());
            SkillNetworking.onPlayerDisconnect(handler.player.getUuid());
            FireBlastSkill.clearFireball(handler.player.getUuid());
            EarthPillarSkill.clear(handler.player.getUuid());
            LAST_AVATAR_STATE_REFLEX.remove(handler.player.getUuid());
        });

        // Tick chi regen + cooldowns for every online player each server tick
        ServerEntityEvents.ENTITY_LOAD.register((entity, world) -> {
            // We hook per-tick via ServerTickEvents instead — see below.
        });

        net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents.END_SERVER_TICK.register(server -> {
            for (ServerPlayerEntity player : server.getPlayerManager().getPlayerList()) {
                PlayerBendingData.tick(player);
                SkillDispatcher.tick(player);
            }
            FireBlastSkill.tickAllFireballs(server);
            EarthBoulderSkill.tickAllBoulders(server);
            BoulderLaunchSkill.tickAllBoulders(server);
            EarthPillarSkill.tickAllPillars(server);
            SkillNetworking.tickElementCycleCooldowns();
        });

        SkillNetworking.registerSlotCastReceiver();
        SkillNetworking.registerCycleElementReceiver();
        SkillNetworking.registerSelectElementReceiver();

        // Earth Pillar manipulation: attack/interact with standing pillar via block or entity swing
        AttackBlockCallback.EVENT.register((player, world, hand, pos, direction) -> {
            if (player instanceof ServerPlayerEntity serverPlayer) {
                if (EarthPillarSkill.hasNearbyPillar(serverPlayer, 5.0)) {
                    boolean handled;
                    if (serverPlayer.isSneaking() || serverPlayer.isSprinting()) {
                        handled = EarthPillarSkill.kickPillar(serverPlayer);
                    } else {
                        handled = EarthPillarSkill.strikePillar(serverPlayer);
                    }
                    if (handled) {
                        return ActionResult.SUCCESS;
                    }
                }
            }
            return ActionResult.PASS;
        });

        AttackEntityCallback.EVENT.register((player, world, hand, entity, hitResult) -> {
            if (player instanceof ServerPlayerEntity serverPlayer) {
                if (EarthPillarSkill.hasNearbyPillar(serverPlayer, 5.0)) {
                    boolean handled;
                    if (serverPlayer.isSneaking() || serverPlayer.isSprinting()) {
                        handled = EarthPillarSkill.kickPillar(serverPlayer);
                    } else {
                        handled = EarthPillarSkill.strikePillar(serverPlayer);
                    }
                    if (handled) {
                        return ActionResult.SUCCESS;
                    }
                }
            }
            return ActionResult.PASS;
        });

        // Damage filter: Fire Guard active blocking & Emergency Avatar State survival reflex
        ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
            if (!(entity instanceof ServerPlayerEntity player)) return true;
            if (FireGuardSkill.shouldBlockDamage(player, source)) return false;
            if (shouldTriggerEmergencyAvatarState(player, source, amount)) {
                triggerEmergencyAvatarState(player);
                return false;
            }
            return true;
        });

        // Boss defeat listener: awards progression and unlocks sub-bending in Skill Tree
        ServerLivingEntityEvents.AFTER_DEATH.register((entity, damageSource) -> {
            if (entity.getCustomName() == null) return;
            String name = entity.getCustomName().getString();
            if (!name.contains("[Boss]")) return;

            ServerPlayerEntity killer = null;
            if (damageSource.getAttacker() instanceof ServerPlayerEntity p) {
                killer = p;
            }

            String bossElement = null;
            if (name.contains("Ozai") || name.contains("Fire")) {
                bossElement = "FIRE";
            } else if (name.contains("Pakku") || name.contains("Water")) {
                bossElement = "WATER";
            } else if (name.contains("Bumi") || name.contains("Earth")) {
                bossElement = "EARTH";
            } else if (name.contains("Gyatso") || name.contains("Air")) {
                bossElement = "AIR";
            } else {
                bossElement = "NON_BENDER";
            }

            // Award to killer or nearby players within 32 blocks of boss defeat
            Box rewardBox = Box.of(entity.getPos(), 64, 64, 64);
            List<ServerPlayerEntity> nearby = entity.getServer().getPlayerManager().getPlayerList().stream()
                    .filter(p -> p.getWorld() == entity.getWorld() && rewardBox.contains(p.getPos()))
                    .toList();

            for (ServerPlayerEntity p : nearby) {
                PlayerBendingData data = PlayerBendingData.get(p);
                boolean isNew = data.addDefeatedBoss(bossElement);
                if (isNew) {
                    p.sendMessage(Text.literal("§6§l[AVATAR PROGRESSION] §aAnda telah mengalahkan " + name + "!"), false);
                    p.sendMessage(Text.literal("§b§l[SKILL TREE UNLOCKED] §eCabang Sub-Bending " + bossElement + " kini terbuka di Pohon Keterampilan [K]!"), false);
                    p.getServerWorld().playSound(null, p.getBlockPos(),
                            SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundCategory.PLAYERS, 1.5f, 1.0f);
                    SkillNetworking.sendHudUpdate(p, data, data.getActiveSkillId());
                }
            }
        });

        ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
            FireBlastSkill.clearFireball(newPlayer.getUuid());
            EarthPillarSkill.clear(newPlayer.getUuid());
            // Cancel any in-flight skill and broadcast IDLE so orbs clear on all clients
            PlayerBendingData data = PlayerBendingData.get(newPlayer);
            if (!data.getTimeline().isIdle()) {
                data.getTimeline().cancel();
                SkillNetworking.broadcastOrbReset(newPlayer);
            }
            SkillNetworking.sendHudUpdate(newPlayer, data, data.getActiveSkillId());
        });

        // Cancel in-flight skill timelines and broadcast orb reset on dimension/world switch
        ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD.register((player, origin, destination) -> {
            FireBlastSkill.clearFireball(player.getUuid());
            EarthPillarSkill.clear(player.getUuid());
            PlayerBendingData data = PlayerBendingData.get(player);
            if (!data.getTimeline().isIdle()) {
                data.getTimeline().cancel();
                SkillNetworking.broadcastOrbReset(player);
            }
        });

        // A player who starts tracking a caster mid-cast receives current phase immediately
        EntityTrackingEvents.START_TRACKING.register((trackedEntity, trackingPlayer) -> {
            if (trackedEntity instanceof ServerPlayerEntity otherPlayer) {
                SkillNetworking.syncOrbStateToNewWatcher(trackingPlayer, otherPlayer);
            }
        });

        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayerEntity joining = handler.player;
            for (ServerPlayerEntity other : server.getPlayerManager().getPlayerList()) {
                if (other == joining) continue;
                SkillNetworking.syncOrbStateToNewWatcher(joining, other);
            }
        });
    }

    private static final Map<UUID, Long> LAST_AVATAR_STATE_REFLEX = new ConcurrentHashMap<>();
    private static final long AVATAR_STATE_COOLDOWN_TICKS = 6000L; // 5 minutes cooldown

    public static boolean shouldTriggerEmergencyAvatarState(ServerPlayerEntity player, DamageSource source, float incomingDamage) {
        if (player.isCreative() || player.isSpectator()) return false;
        if (source.isOf(DamageTypes.OUT_OF_WORLD)) return false;

        // Triggers if health would drop to <= 2.0 (lethal or near-fatal <= 1 heart)
        if (player.getHealth() - incomingDamage > 2.0f) return false;

        long currentTick = player.getServerWorld().getTime();
        long lastTrigger = LAST_AVATAR_STATE_REFLEX.getOrDefault(player.getUuid(), -AVATAR_STATE_COOLDOWN_TICKS);
        return (currentTick - lastTrigger) >= AVATAR_STATE_COOLDOWN_TICKS;
    }

    public static void triggerEmergencyAvatarState(ServerPlayerEntity player) {
        long currentTick = player.getServerWorld().getTime();
        LAST_AVATAR_STATE_REFLEX.put(player.getUuid(), currentTick);
        triggerAvatarState(player, 700, true);
    }

    public static void triggerAvatarState(ServerPlayerEntity player, int durationTicks, boolean emergency) {
        ServerWorld world = player.getServerWorld();
        Vec3d pos = player.getPos().add(0, 1.0, 0);

        // 1. Refill health & Chi completely
        player.setHealth(player.getMaxHealth());
        PlayerBendingData data = PlayerBendingData.get(player);
        data.regenChi(data.getMaxChi());
        data.enterAvatarState(durationTicks);

        // 2. Grant Avatar State god-tier empowerment status effects for full duration (35s)
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.RESISTANCE, durationTicks, 3, false, false, true)); // Resistance IV
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.REGENERATION, durationTicks, 2, false, false, true)); // Regen III
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.SPEED, durationTicks, 2, false, false, true)); // Speed III
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.STRENGTH, durationTicks, 2, false, false, true)); // Strength III
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.FIRE_RESISTANCE, durationTicks, 0, false, false, true));
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.JUMP_BOOST, durationTicks, 1, false, false, true));
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOW_FALLING, durationTicks, 0, false, false, true));
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.GLOWING, durationTicks, 0, false, false, true));

        // 3. Cataclysmic 4-Element Shockwave: knockback all hostile & living entities in 10-block radius
        double shockRadius = 10.0;
        Box shockBox = Box.of(pos, shockRadius * 2, shockRadius * 2, shockRadius * 2);
        List<LivingEntity> enemies = world.getEntitiesByClass(
                LivingEntity.class, shockBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(pos) <= shockRadius * shockRadius
        );

        DamageSource shockSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : enemies) {
            e.damage(shockSource, 12.0f);
            Vec3d diff = e.getPos().subtract(player.getPos());
            Vec3d knockDir = diff.lengthSquared() < 0.001 ? new Vec3d(0, 0, 1) : diff.normalize();
            e.addVelocity(knockDir.x * 2.8, 0.95, knockDir.z * 2.8);
            e.velocityModified = true;
        }

        // 4. Epic Visual Spectacle: Celestial Beacon Light Column shooting into the heavens
        for (int y = 0; y < 48; y += 2) {
            world.spawnParticles(ParticleTypes.END_ROD, pos.x, pos.y + y, pos.z, 6, 0.45, 0.7, 0.45, 0.06);
            world.spawnParticles(ParticleTypes.FLASH, pos.x, pos.y + y, pos.z, 1, 0.2, 0.2, 0.2, 0.0);
        }

        // Concentric 4-Element Orbital Tempest
        // Fire Sphere & Outward Shockwave
        world.spawnParticles(ParticleTypes.EXPLOSION_EMITTER, pos.x, pos.y, pos.z, 2, 0, 0, 0, 0);
        world.spawnParticles(ParticleTypes.FLAME, pos.x, pos.y + 0.5, pos.z, 120, 3.5, 1.2, 3.5, 0.25);
        world.spawnParticles(AvatarParticles.FLAME_BURST, pos.x, pos.y + 0.5, pos.z, 40, 2.8, 1.0, 2.8, 0.12);
        // Water Ring
        world.spawnParticles(ParticleTypes.SPLASH, pos.x, pos.y + 1.2, pos.z, 120, 3.5, 0.8, 3.5, 0.35);
        world.spawnParticles(AvatarParticles.DROPLET, pos.x, pos.y + 1.2, pos.z, 60, 3.0, 0.6, 3.0, 0.15);
        // Air Ascending Vortex
        world.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y, pos.z, 80, 2.5, 2.5, 2.5, 0.35);
        world.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 70, 3.0, 1.8, 3.0, 0.2);
        // Earth Megalith Ring
        world.spawnParticles(AvatarParticles.STONE_CHIP, pos.x, pos.y - 0.2, pos.z, 80, 3.2, 0.6, 3.2, 0.22);
        world.spawnParticles(new BlockStateParticleEffect(
                ParticleTypes.BLOCK, net.minecraft.block.Blocks.DEEPSLATE.getDefaultState()),
                pos.x, pos.y - 0.2, pos.z, 90, 3.5, 0.6, 3.5, 0.3);

        // 5. Cataclysmic Sound Layering
        BlockPos bp = player.getBlockPos();
        world.playSound(null, bp, SoundEvents.BLOCK_BEACON_ACTIVATE, SoundCategory.PLAYERS, 3.0f, 1.1f);
        world.playSound(null, bp, SoundEvents.ENTITY_LIGHTNING_BOLT_THUNDER, SoundCategory.PLAYERS, 2.5f, 0.85f);
        world.playSound(null, bp, SoundEvents.ENTITY_WARDEN_SONIC_BOOM, SoundCategory.PLAYERS, 2.0f, 1.05f);
        world.playSound(null, bp, SoundEvents.ENTITY_ENDER_DRAGON_GROWL, SoundCategory.PLAYERS, 1.8f, 1.25f);
        world.playSound(null, bp, SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 2.2f, 0.6f);

        // 6. Broadcast cinematic announcement
        String title = emergency ? "§b§l[AVATAR STATE] §6Emergency Survival Reflex Awakened!"
                                 : "§b§l[AVATAR STATE] §6Transcendence Awakened via Ancient Scroll!";
        player.sendMessage(Text.literal(title), false);
        world.getServer().getPlayerManager().broadcast(
                Text.literal("§6§l" + player.getName().getString() + " §bentered the transcendent §6§lAVATAR STATE§r!"), false);

        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
    }

    private AvatarServerEvents() {}
}
