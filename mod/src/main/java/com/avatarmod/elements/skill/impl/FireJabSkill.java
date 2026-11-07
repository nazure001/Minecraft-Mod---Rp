package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

public final class FireJabSkill {

    /**
     * Called every server tick while the player has fire_jab in timeline.
     * Triggers hitbox exactly on the first tick of the ACTIVE phase.
     */
    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return; // fire only on first active tick

        executeHitbox(player, def);
    }

    private static void executeHitbox(ServerPlayerEntity player, SkillDefinition def) {
        ServerWorld world = player.getServerWorld();
        Vec3d pos = player.getPos().add(0, player.getStandingEyeHeight() / 2.0, 0);
        Vec3d look = player.getRotationVec(1.0f);
        // Center hitbox slightly in front of player
        Vec3d center = pos.add(look.multiply(def.range() * 0.6));

        double r = def.range();
        Box box = Box.of(center, r * 2, r * 2, r * 2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= r * r
        );

        DamageSource source = world.getDamageSources().playerAttack(player);

        for (LivingEntity target : targets) {
            target.damage(source, def.damage());

            // Knockback away from player
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            target.addVelocity(
                    knockDir.x * def.knockback(),
                    0.1 + def.knockback() * 0.3,
                    knockDir.z * def.knockback()
            );
            target.velocityModified = true;
        }

        // VFX: flame particles at center
        world.spawnParticles(ParticleTypes.FLAME,
                center.x, center.y, center.z,
                12, r * 0.4, r * 0.4, r * 0.4, 0.05);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                center.x, center.y, center.z,
                4, r * 0.2, r * 0.2, r * 0.2, 0.01);

        // SFX: fire woosh
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BLAZE_SHOOT,
                SoundCategory.PLAYERS,
                0.6f, 1.3f + (world.getRandom().nextFloat() * 0.2f));
    }

    private FireJabSkill() {}
}
