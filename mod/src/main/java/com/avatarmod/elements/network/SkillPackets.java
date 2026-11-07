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
                    buf.writeString(value.skillId());
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
                    buf.writeString(value.activeCooldownSkillId());
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

    // Client → Server: player selected a new active element
    public record C2SSetElement(String element) implements CustomPayload {
        public static final CustomPayload.Id<C2SSetElement> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_set_element"));
        public static final PacketCodec<PacketByteBuf, C2SSetElement> CODEC = PacketCodec.of(
                (value, buf) -> buf.writeString(value.element()),
                buf -> new C2SSetElement(buf.readString(16))
        );
        @Override public CustomPayload.Id<C2SSetElement> getId() { return ID; }
    }

    private SkillPackets() {}
}
