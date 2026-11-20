package com.avatarmod.elements.network;

import net.minecraft.network.PacketByteBuf;
import net.minecraft.network.codec.PacketCodec;
import net.minecraft.network.packet.CustomPayload;
import net.minecraft.util.Identifier;

public final class SkillPackets {

    // Client → Server: player requests to use a skill
    public record C2SSkillInput(String skillId) implements CustomPayload {
        public static final CustomPayload.Id<C2SSkillInput> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_skill_input"));
        public static final PacketCodec<PacketByteBuf, C2SSkillInput> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeString(value.skillId()),
                buf -> new C2SSkillInput(buf.readString(64))
        );

        @Override
        public CustomPayload.Id<C2SSkillInput> getId() { return ID; }
    }

    // Server → Client: result of a skill attempt
    public record S2CSkillResult(
            String skillId,
            boolean allowed,
            DenyReason denyReason,  // only meaningful when !allowed
            int cooldownTicks
    ) implements CustomPayload {

        public enum DenyReason {
            NONE, COOLDOWN, NOT_ENOUGH_CHI, WRONG_MASTERY, RATE_LIMITED;

            static DenyReason fromByte(byte b) {
                DenyReason[] v = values();
                return b >= 0 && b < v.length ? v[b] : NONE;
            }
        }

        public static final CustomPayload.Id<S2CSkillResult> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_skill_result"));
        public static final PacketCodec<PacketByteBuf, S2CSkillResult> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeString(value.skillId() != null ? value.skillId() : "");
                    buf.writeBoolean(value.allowed());
                    buf.writeByte(value.denyReason().ordinal());
                    buf.writeVarInt(value.cooldownTicks());
                },
                buf -> new S2CSkillResult(
                        buf.readString(64),
                        buf.readBoolean(),
                        DenyReason.fromByte(buf.readByte()),
                        buf.readVarInt()
                )
        );

        @Override
        public CustomPayload.Id<S2CSkillResult> getId() { return ID; }
    }

    // Server → Client: HUD state update (chi bar + active cooldowns)
    public record S2CHudUpdate(int currentChi, int maxChi, String activeCooldownSkillId,
                               int cooldownTicksRemaining) implements CustomPayload {
        public static final CustomPayload.Id<S2CHudUpdate> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_hud_update"));
        public static final PacketCodec<PacketByteBuf, S2CHudUpdate> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeVarInt(value.currentChi());
                    buf.writeVarInt(value.maxChi());
                    buf.writeString(value.activeCooldownSkillId() != null ? value.activeCooldownSkillId() : "");
                    buf.writeVarInt(value.cooldownTicksRemaining());
                },
                buf -> new S2CHudUpdate(
                        buf.readVarInt(),
                        buf.readVarInt(),
                        buf.readString(64),
                        buf.readVarInt()
                )
        );

        @Override
        public CustomPayload.Id<S2CHudUpdate> getId() { return ID; }
    }

    // Server → Client: active element synchronization (server-authoritative)
    public record S2CSyncElement(String element) implements CustomPayload {
        public static final CustomPayload.Id<S2CSyncElement> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_sync_element"));
        public static final PacketCodec<PacketByteBuf, S2CSyncElement> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeString(value.element() != null ? value.element() : "FIRE"),
                buf -> new S2CSyncElement(buf.readString(16))
        );

        @Override
        public CustomPayload.Id<S2CSyncElement> getId() { return ID; }
    }

    // Client → Server: cast skill in slot N of active element
    public record C2SSlotCast(int slotIndex) implements CustomPayload {
        public static final CustomPayload.Id<C2SSlotCast> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_slot_cast"));
        public static final PacketCodec<PacketByteBuf, C2SSlotCast> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeByte(value.slotIndex()),
                buf -> new C2SSlotCast(buf.readByte())
        );
        @Override public CustomPayload.Id<C2SSlotCast> getId() { return ID; }
    }

    // Client → Server: player starts holding a hold-release skill
    public record C2SHoldStart(int slotIndex) implements CustomPayload {
        public static final CustomPayload.Id<C2SHoldStart> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_hold_start"));
        public static final PacketCodec<PacketByteBuf, C2SHoldStart> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeByte(value.slotIndex()),
                buf -> new C2SHoldStart(buf.readByte())
        );
        public C2SHoldStart(int slotIndex, String skillId) {
            this(slotIndex);
        }
        public String skillId() { return ""; }
        @Override public CustomPayload.Id<C2SHoldStart> getId() { return ID; }
    }

    // Client → Server: player releases a hold-release skill
    public record C2SHoldRelease(int slotIndex, int heldTicks) implements CustomPayload {
        public static final CustomPayload.Id<C2SHoldRelease> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_hold_release"));
        public static final PacketCodec<PacketByteBuf, C2SHoldRelease> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeByte(value.slotIndex());
                    buf.writeVarInt(value.heldTicks());
                },
                buf -> new C2SHoldRelease(buf.readByte(), buf.readVarInt())
        );
        public C2SHoldRelease(int slotIndex, String skillId) {
            this(slotIndex, 0);
        }
        public String skillId() { return ""; }
        @Override public CustomPayload.Id<C2SHoldRelease> getId() { return ID; }
    }

    // Client → Server: request advancing to the next active element
    public record C2SCycleElement() implements CustomPayload {
        public static final CustomPayload.Id<C2SCycleElement> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_cycle_element"));
        public static final PacketCodec<PacketByteBuf, C2SCycleElement> CODEC =
                PacketCodec.unit(new C2SCycleElement());

        @Override public CustomPayload.Id<C2SCycleElement> getId() { return ID; }
    }

    // Client → Server: request selecting a specific configured element.
    public record C2SSelectElement(String element) implements CustomPayload {
        public static final CustomPayload.Id<C2SSelectElement> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_select_element"));
        public static final PacketCodec<PacketByteBuf, C2SSelectElement> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeString(value.element() != null ? value.element() : ""),
                buf -> new C2SSelectElement(buf.readString(16))
        );

        @Override public CustomPayload.Id<C2SSelectElement> getId() { return ID; }
    }

    // Server → Client (broadcast): phase transition for any caster, so nearby players
    // can render the charge orb on that player.
    // castSerial increments each time a NEW cast starts; allows client to ignore
    // late IDLE resets from a previous cast when a new cast has already begun.
    public record S2CPhaseSync(
            java.util.UUID casterUuid,
            String skillId,
            String phase,   // "IDLE" | "WINDUP" | "ACTIVE" | "RECOVERY"
            int ticksIn,
            int castSerial
    ) implements CustomPayload {
        public static final CustomPayload.Id<S2CPhaseSync> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_phase_sync"));
        public static final PacketCodec<PacketByteBuf, S2CPhaseSync> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeUuid(value.casterUuid());
                    buf.writeString(value.skillId() != null ? value.skillId() : "");
                    buf.writeString(value.phase() != null ? value.phase() : "IDLE");
                    buf.writeVarInt(value.ticksIn());
                    buf.writeVarInt(value.castSerial());
                },
                buf -> new S2CPhaseSync(
                        buf.readUuid(),
                        buf.readString(64),
                        buf.readString(16),
                        buf.readVarInt(),
                        buf.readVarInt()
                )
        );
        @Override public CustomPayload.Id<S2CPhaseSync> getId() { return ID; }
    }

    // Server → Client (broadcast): authoritative world position for a positional skill
    // (e.g. Earth Pillar ground center). Sent once on ACTIVE transition; client uses
    // this instead of guessing the position from look direction.
    public record S2CSkillPosition(
            java.util.UUID casterUuid,
            int castSerial,
            String skillId,
            double x, double y, double z
    ) implements CustomPayload {
        public static final CustomPayload.Id<S2CSkillPosition> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_skill_position"));
        public static final PacketCodec<PacketByteBuf, S2CSkillPosition> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeUuid(value.casterUuid());
                    buf.writeVarInt(value.castSerial());
                    buf.writeString(value.skillId() != null ? value.skillId() : "");
                    buf.writeDouble(value.x());
                    buf.writeDouble(value.y());
                    buf.writeDouble(value.z());
                },
                buf -> new S2CSkillPosition(
                        buf.readUuid(),
                        buf.readVarInt(),
                        buf.readString(64),
                        buf.readDouble(),
                        buf.readDouble(),
                        buf.readDouble()
                )
        );
        @Override public CustomPayload.Id<S2CSkillPosition> getId() { return ID; }
    }

    // Client → Server: player interacts with / manipulates an active earth pillar
    // actionType: 0 = KICK (Single Power Kick / Megalith Launch), 1 = STRIKE (Rapid Barrage Punch)
    public record C2SPillarInteract(int actionType) implements CustomPayload {
        public static final CustomPayload.Id<C2SPillarInteract> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_pillar_interact"));
        public static final PacketCodec<PacketByteBuf, C2SPillarInteract> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeByte(value.actionType()),
                buf -> new C2SPillarInteract(buf.readByte())
        );

        @Override public CustomPayload.Id<C2SPillarInteract> getId() { return ID; }
    }

    // Server → Client (broadcast): pillar action event for visual & audio FX
    // actionType: 0 = KICK (launches megalith), 1 = STRIKE (shatters stone shards), 2 = CRUMBLE (pillar collapses)
    public record S2CPillarAction(
            java.util.UUID casterUuid,
            int actionType,
            double x, double y, double z,
            double dirX, double dirY, double dirZ
    ) implements CustomPayload {
        public static final CustomPayload.Id<S2CPillarAction> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_pillar_action"));
        public static final PacketCodec<PacketByteBuf, S2CPillarAction> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeUuid(value.casterUuid());
                    buf.writeByte(value.actionType());
                    buf.writeDouble(value.x());
                    buf.writeDouble(value.y());
                    buf.writeDouble(value.z());
                    buf.writeDouble(value.dirX());
                    buf.writeDouble(value.dirY());
                    buf.writeDouble(value.dirZ());
                },
                buf -> new S2CPillarAction(
                        buf.readUuid(),
                        buf.readByte(),
                        buf.readDouble(),
                        buf.readDouble(),
                        buf.readDouble(),
                        buf.readDouble(),
                        buf.readDouble(),
                        buf.readDouble()
                )
        );

        @Override public CustomPayload.Id<S2CPillarAction> getId() { return ID; }
    }

    // Client → Server: Unarmed Martial Attack Combo or Aerial Dive-Kick
    public record C2SMartialAttack(int comboStep, boolean isAerial) implements CustomPayload {
        public static final CustomPayload.Id<C2SMartialAttack> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_martial_attack"));
        public static final PacketCodec<PacketByteBuf, C2SMartialAttack> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeByte(value.comboStep());
                    buf.writeBoolean(value.isAerial());
                },
                buf -> new C2SMartialAttack(buf.readByte(), buf.readBoolean())
        );

        @Override public CustomPayload.Id<C2SMartialAttack> getId() { return ID; }
    }

    private SkillPackets() {}
}
