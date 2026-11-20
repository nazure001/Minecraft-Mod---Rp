package com.avatarmod.elements.network;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDispatcher;
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

        ServerWorld world = player.getServerWorld();
        Vec3d pos = player.getPos().add(0, 1.0, 0);

        // 1. Refill health & Chi completely
        player.setHealth(player.getMaxHealth());
        PlayerBendingData data = PlayerBendingData.get(player);
        data.regenChi(data.getMaxChi());

        // 2. Grant Avatar State empowerment status effects
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.RESISTANCE, 200, 3, false, false, true)); // 10s Resistance IV
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.REGENERATION, 200, 2, false, false, true)); // 10s Regen III
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.SPEED, 200, 1, false, false, true)); // 10s Speed II
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.GLOWING, 200, 0, false, false, true)); // 10s Glowing aura

        // 3. Cataclysmic 4-Element Shockwave: knockback all hostile & living entities in 8-block radius
        double shockRadius = 8.0;
        Box shockBox = Box.of(pos, shockRadius * 2, shockRadius * 2, shockRadius * 2);
        List<LivingEntity> enemies = world.getEntitiesByClass(
                LivingEntity.class, shockBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(pos) <= shockRadius * shockRadius
        );

        DamageSource shockSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : enemies) {
            e.damage(shockSource, 8.0f);
            Vec3d diff = e.getPos().subtract(player.getPos());
            Vec3d knockDir = diff.lengthSquared() < 0.001 ? new Vec3d(0, 0, 1) : diff.normalize();
            e.addVelocity(knockDir.x * 2.2, 0.75, knockDir.z * 2.2);
            e.velocityModified = true;
        }

        // 4. Four Elements Sphere & Ring Particles
        // Fire
        world.spawnParticles(ParticleTypes.EXPLOSION_EMITTER, pos.x, pos.y, pos.z, 1, 0, 0, 0, 0);
        world.spawnParticles(ParticleTypes.FLAME, pos.x, pos.y, pos.z, 60, 2.5, 1.0, 2.5, 0.15);
        world.spawnParticles(AvatarParticles.FLAME_BURST, pos.x, pos.y, pos.z, 20, 2.0, 0.8, 2.0, 0.08);
        // Water
        world.spawnParticles(ParticleTypes.SPLASH, pos.x, pos.y, pos.z, 60, 2.5, 1.0, 2.5, 0.2);
        world.spawnParticles(AvatarParticles.DROPLET, pos.x, pos.y, pos.z, 40, 2.0, 0.8, 2.0, 0.1);
        // Air
        world.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y, pos.z, 40, 2.0, 1.2, 2.0, 0.2);
        world.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 40, 2.0, 1.0, 2.0, 0.15);
        world.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 30, 1.5, 0.8, 1.5, 0.08);
        // Earth
        world.spawnParticles(AvatarParticles.STONE_CHIP, pos.x, pos.y, pos.z, 40, 2.0, 0.8, 2.0, 0.15);
        world.spawnParticles(new BlockStateParticleEffect(
                ParticleTypes.BLOCK, net.minecraft.block.Blocks.STONE.getDefaultState()),
                pos.x, pos.y, pos.z, 50, 2.0, 0.8, 2.0, 0.2);

        // 5. Epic sound layering
        BlockPos bp = player.getBlockPos();
        world.playSound(null, bp, SoundEvents.BLOCK_BEACON_ACTIVATE, SoundCategory.PLAYERS, 2.5f, 1.2f);
        world.playSound(null, bp, SoundEvents.ENTITY_LIGHTNING_BOLT_THUNDER, SoundCategory.PLAYERS, 2.0f, 0.9f);
        world.playSound(null, bp, SoundEvents.ENTITY_ENDER_DRAGON_GROWL, SoundCategory.PLAYERS, 1.5f, 1.3f);
        world.playSound(null, bp, SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 2.0f, 0.7f);

        // 6. Broadcast cinematic text
        player.sendMessage(Text.literal("§b§l[AVATAR STATE] §6Emergency Survival Reflex Activated!"), false);
        world.getServer().getPlayerManager().broadcast(
                Text.literal("§e" + player.getName().getString() + " §bentered the §6§lAVATAR STATE§r!"), false);

        SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
    }

    private AvatarServerEvents() {}
}
