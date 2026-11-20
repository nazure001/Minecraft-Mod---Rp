package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Earth Boulder — projectile that travels in look direction each tick.
 * Hits first entity in path; detonates on block collision or after lifetime.
 * Scales damage and particles dynamically based on extracted block hardness!
 */
public final class EarthBoulderSkill {

    private static final float SPEED = 0.8f;       // blocks per tick
    private static final int   LIFETIME = 20;      // ticks
    private static final float HITBOX_RADIUS = 0.7f;

    // Active boulders keyed by player UUID
    private static final Map<UUID, BoulderState> BOULDERS = new ConcurrentHashMap<>();

    private record BoulderState(Vec3d pos, Vec3d velocity, int ticksLeft, float damage, float knockback, BlockState blockState) {}

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();

        // Spawn boulder at start of ACTIVE phase
        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 0) {
            Vec3d spawnPos = player.getPos().add(0, player.getStandingEyeHeight() * 0.8, 0);
            Vec3d vel = player.getRotationVec(1.0f).multiply(SPEED);

            ServerWorld world = player.getServerWorld();
            BlockPos groundPos = ElementalInteractions.findSolidGroundBelow(world, player.getBlockPos(), 6);
            BlockState groundState = world.getBlockState(groundPos);
            if (groundState.isAir()) groundState = Blocks.STONE.getDefaultState();
            float damage = ElementalInteractions.calculateEarthHardnessDamage(world, groundPos, def.damage());

            BOULDERS.put(player.getUuid(), new BoulderState(spawnPos, vel, LIFETIME, damage, def.knockback(), groundState));

            float bonus = damage - def.damage();
            if (bonus > 0.5f) {
                player.sendMessage(Text.literal("§6[Earth] Boulder dipadatkan dari " + groundState.getBlock().getName().getString() + " §e(+" + String.format(Locale.ROOT, "%.1f", bonus) + " DMG)"), true);
            }
        }
    }

    public static void tickAllBoulders(net.minecraft.server.MinecraftServer server) {
        if (BOULDERS.isEmpty()) return;
        for (UUID id : BOULDERS.keySet()) {
            ServerPlayerEntity player = server.getPlayerManager().getPlayer(id);
            if (player != null) {
                advanceBoulder(player);
            } else {
                BOULDERS.remove(id);
            }
        }
    }

    private static void advanceBoulder(ServerPlayerEntity player) {
        UUID id = player.getUuid();
        BoulderState state = BOULDERS.get(id);
        if (state == null) return;

        ServerWorld world = player.getServerWorld();
        Vec3d nextPos = state.pos().add(state.velocity());

        // VFX at current position: tumbling stone chunks & dust trail matching block type
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                state.pos().x, state.pos().y, state.pos().z,
                4, HITBOX_RADIUS * 0.4, HITBOX_RADIUS * 0.4, HITBOX_RADIUS * 0.4, 0.04);
        world.spawnParticles(AvatarParticles.DUST,
                state.pos().x, state.pos().y, state.pos().z,
                6, HITBOX_RADIUS * 0.5, HITBOX_RADIUS * 0.5, HITBOX_RADIUS * 0.5, 0.02);
        world.spawnParticles(ParticleTypes.POOF,
                state.pos().x, state.pos().y, state.pos().z,
                2, HITBOX_RADIUS * 0.3, HITBOX_RADIUS * 0.3, HITBOX_RADIUS * 0.3, 0.01);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, state.blockState()),
                state.pos().x, state.pos().y, state.pos().z,
                3, HITBOX_RADIUS * 0.3, HITBOX_RADIUS * 0.3, HITBOX_RADIUS * 0.3, 0.04);

        // Collision check: entities
        Box hitbox = Box.of(nextPos, HITBOX_RADIUS * 2, HITBOX_RADIUS * 2, HITBOX_RADIUS * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitbox,
                e -> e != player && e.isAlive()
        );
        if (!targets.isEmpty()) {
            detonate(player, world, nextPos, targets, state);
            BOULDERS.remove(id);
            return;
        }

        // Collision check: blocks
        if (!world.isAir(net.minecraft.util.math.BlockPos.ofFloored(nextPos))) {
            detonate(player, world, state.pos(), List.of(), state);
            BOULDERS.remove(id);
            return;
        }

        // Advance or expire
        int ticksLeft = state.ticksLeft() - 1;
        if (ticksLeft <= 0) {
            BOULDERS.remove(id);
        } else {
            BOULDERS.put(id, new BoulderState(nextPos, state.velocity(), ticksLeft, state.damage(), state.knockback(), state.blockState()));
        }
    }

    private static void detonate(ServerPlayerEntity player, ServerWorld world, Vec3d pos,
                                  List<LivingEntity> targets, BoulderState state) {
        // Impact VFX: Cataclysmic tectonic crash & stone explosion using block particles
        world.spawnParticles(ParticleTypes.EXPLOSION,
                pos.x, pos.y, pos.z, 2, 0.2, 0.2, 0.2, 0.0);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                pos.x, pos.y, pos.z, 16, 0.5, 0.5, 0.5, 0.1);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                pos.x, pos.y, pos.z, 25, 0.7, 0.5, 0.7, 0.15);
        world.spawnParticles(AvatarParticles.DUST,
                pos.x, pos.y, pos.z, 30, 0.9, 0.5, 0.9, 0.1);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, state.blockState()),
                pos.x, pos.y, pos.z, 35, 0.7, 0.7, 0.7, 0.12);

        // Multi-layered deep tectonic roar SFX
        BlockPos blockPos = BlockPos.ofFloored(pos);
        world.playSound(null, blockPos,
                SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.5f);
        world.playSound(null, blockPos,
                SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 1.5f, 0.6f);
        world.playSound(null, blockPos,
                SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 2.0f, 0.7f);

        float hardness = state.blockState().getHardness(world, blockPos);
        if (hardness >= 10.0f) {
            world.playSound(null, blockPos, SoundEvents.BLOCK_ANVIL_LAND, SoundCategory.PLAYERS, 1.8f, 0.6f);
        }

        // Clear surface vegetation at impact point
        ElementalInteractions.clearVegetation(world, pos, 2.0);

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, state.damage());
            ElementalInteractions.applySeismicStagger(target, 40);
            Vec3d diff = target.getPos().subtract(pos);
            Vec3d knockDir = diff.lengthSquared() < 0.001 ? new Vec3d(0, 0, 1) : diff.normalize();
            target.addVelocity(knockDir.x * state.knockback(), 0.3, knockDir.z * state.knockback());
            target.velocityModified = true;
        }
    }

    public static void clear(UUID casterUuid) {
        BOULDERS.remove(casterUuid);
    }

    private EarthBoulderSkill() {}
}
