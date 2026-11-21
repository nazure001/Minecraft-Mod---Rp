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
import net.minecraft.network.packet.s2c.play.EntityVelocityUpdateS2CPacket;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Earth Tunnel & Earth Surfing — Master Earthbending Subterranean Excavation & Traversal.
 *
 * Implements two fluid traversal states:
 * 1. Earth Tunneling (Underground / Facing Rock & Soil):
 *    Parting and excavating solid earth, deepslate, stone, dirt, and sand in a 3x3 tunnel
 *    ahead of the player without requiring a pickaxe.
 *    - Ores (Coal, Iron, Copper, Gold, Diamond, Emerald, etc.) drop naturally.
 *    - Standard stone/dirt is pulverized into mineral dust, preventing ground clutter.
 *    - Player is propelled smoothly through subterranean passageways.
 * 2. Earth Surfing (Above Ground / Open Surface):
 *    Surfs atop a surging wave ridge of stone and soil, effortlessly scaling hills
 *    and rough terrain with high forward momentum.
 */
public final class EarthTunnelSkill {

    public static final String ID = "avatar:earth_tunnel";
    private static final double BASE_BURROW_SPEED = 0.75;
    private static final double BASE_SURF_SPEED = 0.90;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.HOLD && timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();
        ServerWorld world = player.getServerWorld();

        // 1. Chi sustain consumption during hold phase (1 Chi every 3 ticks)
        if (timeline.phase() == SkillTimeline.Phase.HOLD && t > 0 && t % 3 == 0) {
            if (!data.trySpendChi(1)) {
                timeline.releaseHold();
                return;
            }
        }

        // 2. Fall damage immunity while tunneling or earth surfing
        player.fallDistance = 0.0f;

        // 3. Direction and weapon synergy
        Vec3d look = player.getRotationVec(1.0f);
        double speedMultiplier = ElementalInteractions.getWeaponSpeedMultiplier(player.getMainHandStack(), "EARTH");

        // 4. Excavate blocks ahead in gaze direction
        BlockPos excavationCenter = BlockPos.ofFloored(player.getEyePos().add(look.multiply(1.8)));
        int excavated = excavateTunnelCorridor(world, excavationCenter, player);

        if (excavated > 0) {
            // === STATE A: SUBTERRANEAN BURROWING ===
            double burrowSpeed = BASE_BURROW_SPEED * speedMultiplier;
            player.setVelocity(look.x * burrowSpeed, look.y * burrowSpeed, look.z * burrowSpeed);
            player.velocityModified = true;

            // Rhythmic subterranean grinding & stone parting sounds
            if (t % 4 == 0) {
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_STONE_BREAK, SoundCategory.BLOCKS, 0.85f, 0.95f);
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_ROOTED_DIRT_BREAK, SoundCategory.BLOCKS, 0.90f, 1.10f);
            }
        } else {
            // === STATE B: SURFACE EARTH SURFING ===
            double surfSpeed = BASE_SURF_SPEED * speedMultiplier;
            double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
            Vec3d forward = horizLen > 1e-4
                    ? new Vec3d(look.x / horizLen, 0, look.z / horizLen)
                    : new Vec3d(0, 0, 1);

            double vy = player.getVelocity().y;
            if (player.isOnGround()) {
                vy = 0.12; // gentle step-up lift over surface obstacles
            }

            player.setVelocity(forward.x * surfSpeed, vy, forward.z * surfSpeed);
            player.velocityModified = true;

            // Stone fragments & dust trail along terrain
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    player.getX(), player.getY() + 0.15, player.getZ(),
                    4, 0.25, 0.1, 0.25, 0.04);
            world.spawnParticles(AvatarParticles.DUST,
                    player.getX(), player.getY() + 0.1, player.getZ(),
                    5, 0.3, 0.1, 0.3, 0.02);

            if (t % 6 == 0) {
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_GRAVEL_STEP, SoundCategory.PLAYERS, 0.80f, 0.85f);
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.ENTITY_IRON_GOLEM_STEP, SoundCategory.PLAYERS, 0.60f, 1.20f);
            }
        }

        // 5. Knockback and stagger mobs collided with along path
        Box bumpBox = Box.of(player.getPos().add(0, 0.5, 0), 2.0, 2.0, 2.0);
        List<LivingEntity> enemies = world.getEntitiesByClass(
                LivingEntity.class, bumpBox,
                e -> e != player && e.isAlive()
        );
        DamageSource attackSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : enemies) {
            Vec3d push = e.getPos().subtract(player.getPos()).normalize().multiply(def.knockback());
            e.addVelocity(push.x, 0.25, push.z);
            e.velocityModified = true;
            if (def.damage() > 0) {
                e.damage(attackSource, def.damage());
            }
            ElementalInteractions.applySeismicStagger(e, 40);
        }

        // 6. Periodic velocity synchronization
        if (t % 2 == 0) {
            player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));
        }
    }

    private static int excavateTunnelCorridor(ServerWorld world, BlockPos center, ServerPlayerEntity player) {
        int count = 0;
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                for (int dz = -1; dz <= 1; dz++) {
                    BlockPos p = center.add(dx, dy, dz);
                    BlockState state = world.getBlockState(p);
                    if (ElementalInteractions.isBendableEarth(state)) {
                        if (ElementalInteractions.isOreBlock(state)) {
                            // Extract valuable ore blocks with full item drops
                            world.breakBlock(p, true, player);
                        } else {
                            // Pulverize stone/soil cleanly to avoid cluttering underground tunnels
                            world.setBlockState(p, Blocks.AIR.getDefaultState());
                        }

                        // Particle debris burst
                        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, state),
                                p.getX() + 0.5, p.getY() + 0.5, p.getZ() + 0.5,
                                3, 0.2, 0.2, 0.2, 0.1);
                        count++;
                    }
                }
            }
        }
        return count;
    }

    private EarthTunnelSkill() {}
}
