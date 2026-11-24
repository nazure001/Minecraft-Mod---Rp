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
 * Earth Tunnel & Earth Surfing — Master Earthbending Traversal & Geological Manipulation.
 *
 * Implements two authentic martial arts traversal modes:
 * 1. Subterranean Excavation (Underground / Facing Solid Rock & Soil):
 *    Weighty, controlled subterranean parting of stone and soil at balanced excavation speed (0.42).
 *    - Pulverizes common rocks into dust while preserving valuable ore drops.
 *    - Dense subterranean grinding soundscapes and rock fracture debris.
 * 2. Surface Earth Surfing (Above Ground / Open Terrain):
 *    Surfs atop a surging, undulating tectonic wave of soil and bedrock.
 *    - Dynamic elevation control: pitch gaze up/down or jump/sneak to elevate or lower the wave height!
 *    - Continuous furrowed wake of cracked earth, dust clouds, and rolling ground ripples.
 *    - Tramples and seismically staggers enemies in the surf path.
 */
public final class EarthTunnelSkill {

    public static final String ID = "avatar:earth_tunnel";
    private static final double BASE_BURROW_SPEED = 0.42; // Balanced realistic subterranean tunneling speed
    private static final double BASE_SURF_SPEED = 0.88;

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

        // 4. Check for solid earth directly ahead in gaze direction
        BlockPos excavationCenter = BlockPos.ofFloored(player.getEyePos().add(look.multiply(1.8)));
        int excavated = excavateTunnelCorridor(world, excavationCenter, player);

        if (excavated > 0) {
            // === STATE A: SUBTERRANEAN BURROWING ===
            double burrowSpeed = BASE_BURROW_SPEED * speedMultiplier;
            player.setVelocity(look.x * burrowSpeed, look.y * burrowSpeed, look.z * burrowSpeed);
            player.velocityModified = true;

            // Rhythmic subterranean grinding, root tearing, and rock fracturing sounds
            if (t % 4 == 0) {
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_STONE_BREAK, SoundCategory.BLOCKS, 0.95f, 0.85f);
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_ROOTED_DIRT_BREAK, SoundCategory.BLOCKS, 1.0f, 1.05f);
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.BLOCKS, 0.85f, 0.80f);
            }

            // Heavy mineral dust and stone chips swirling around the burrowing earthbender
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    player.getX(), player.getY() + 0.8, player.getZ(),
                    6, 0.4, 0.4, 0.4, 0.08);
            world.spawnParticles(AvatarParticles.DUST,
                    player.getX(), player.getY() + 0.5, player.getZ(),
                    8, 0.5, 0.5, 0.5, 0.04);
        } else {
            // === STATE B: SURFACE EARTH SURFING WITH DYNAMIC ELEVATION ===
            double surfSpeed = BASE_SURF_SPEED * speedMultiplier;
            double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
            Vec3d forward = horizLen > 1e-4
                    ? new Vec3d(look.x / horizLen, 0, look.z / horizLen)
                    : new Vec3d(0, 0, 1);

            // Dynamic height control based on player look pitch:
            // Pitch < -6 (looking up): elevate wave upward!
            // Pitch > 10 (looking down): lower wave or descend hills smoothly!
            double pitch = player.getPitch();
            double vy = player.getVelocity().y;

            if (pitch < -6.0) {
                // Elevate: convert upward gaze into soaring ground wave lift
                double climbFactor = Math.min(0.42, -look.y * 0.50);
                vy = Math.max(vy, climbFactor);
            } else if (pitch > 10.0) {
                // Descend / hug contour
                vy = Math.min(vy, -0.22);
            } else if (player.isOnGround()) {
                // Gentle baseline lift to effortlessly ride over 1-block steps and hill crests
                vy = 0.16;
            }

            player.setVelocity(forward.x * surfSpeed, vy, forward.z * surfSpeed);
            player.velocityModified = true;

            // Sample ground block beneath player to create authentic undulating ground wave
            BlockPos groundBelow = findSurfaceGroundBelow(world, player.getBlockPos(), 4);
            BlockState groundState = world.getBlockState(groundBelow);
            if (groundState.isAir() || !groundState.getFluidState().isEmpty()) {
                groundState = Blocks.DIRT.getDefaultState();
            }

            // Undulating wave particles directly under feet
            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, groundState),
                    player.getX(), player.getY() + 0.1, player.getZ(),
                    8, 0.35, 0.15, 0.35, 0.08);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    player.getX(), player.getY() + 0.15, player.getZ(),
                    5, 0.3, 0.1, 0.3, 0.05);

            // Trailing furrow wake of cracked earth and dust behind player
            for (double dist = 0.8; dist <= 2.4; dist += 0.8) {
                Vec3d trailPos = player.getPos().subtract(forward.multiply(dist));
                world.spawnParticles(AvatarParticles.DUST,
                        trailPos.x, trailPos.y + 0.1, trailPos.z,
                        4, 0.35, 0.1, 0.35, 0.02);
                world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, groundState),
                        trailPos.x, trailPos.y + 0.05, trailPos.z,
                        3, 0.25, 0.05, 0.25, 0.03);
            }

            // Rhythmic stone rumbling and earth slide audio
            if (t % 5 == 0) {
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_GRAVEL_STEP, SoundCategory.PLAYERS, 0.90f, 0.80f);
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.ENTITY_IRON_GOLEM_STEP, SoundCategory.PLAYERS, 0.75f, 1.10f);
            }
        }

        // 5. Knockback and seismically stagger mobs collided with along path
        Box bumpBox = Box.of(player.getPos().add(0, 0.5, 0), 2.2, 2.2, 2.2);
        List<LivingEntity> enemies = world.getEntitiesByClass(
                LivingEntity.class, bumpBox,
                e -> e != player && e.isAlive()
        );
        DamageSource attackSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : enemies) {
            Vec3d push = e.getPos().subtract(player.getPos()).normalize().multiply(def.knockback() * 1.2);
            e.addVelocity(push.x, 0.30, push.z);
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

    private static BlockPos findSurfaceGroundBelow(ServerWorld world, BlockPos start, int maxDepth) {
        for (int dy = 0; dy <= maxDepth; dy++) {
            BlockPos check = start.down(dy);
            if (!world.getBlockState(check).getCollisionShape(world, check).isEmpty()) {
                return check;
            }
        }
        return start.down();
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
