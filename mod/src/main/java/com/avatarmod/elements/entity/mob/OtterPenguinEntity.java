package com.avatarmod.elements.entity.mob;

import net.minecraft.block.Blocks;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.passive.AnimalEntity;
import net.minecraft.entity.passive.PassiveEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Items;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

/**
 * Otter Penguin — Agile arctic creature capable of sledging across snow and ice sheets.
 */
public class OtterPenguinEntity extends AnimalEntity {

    public OtterPenguinEntity(EntityType<? extends AnimalEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 4;
    }

    public static DefaultAttributeContainer.Builder createOtterPenguinAttributes() {
        return AnimalEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 20.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.26)
                .add(EntityAttributes.GENERIC_ARMOR, 1.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new EscapeDangerGoal(this, 1.4));
        this.goalSelector.add(3, new TemptGoal(this, 1.2, stack -> stack.isOf(Items.COD) || stack.isOf(Items.SALMON), false));
        this.goalSelector.add(4, new WanderAroundFarGoal(this, 0.9));
        this.goalSelector.add(5, new LookAtEntityGoal(this, PlayerEntity.class, 10.0f));
        this.goalSelector.add(6, new LookAroundGoal(this));
    }

    @Override
    public void tick() {
        super.tick();

        // Slide boost on ice or snow
        BlockPos below = this.getBlockPos().down();
        var block = this.getWorld().getBlockState(below).getBlock();
        if (block == Blocks.ICE || block == Blocks.PACKED_ICE || block == Blocks.BLUE_ICE || block == Blocks.SNOW_BLOCK) {
            this.setVelocity(this.getVelocity().multiply(1.15, 1.0, 1.15));
            this.velocityModified = true;
        }
    }

    @Override
    public boolean isBreedingItem(net.minecraft.item.ItemStack stack) {
        return stack.isOf(Items.COD) || stack.isOf(Items.SALMON);
    }

    @Nullable
    @Override
    public PassiveEntity createChild(ServerWorld world, PassiveEntity entity) {
        return null;
    }
}
