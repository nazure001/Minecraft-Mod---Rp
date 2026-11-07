package com.avatarmod.elements.network;

import net.minecraft.network.PacketByteBuf;
import net.minecraft.network.codec.PacketCodec;
import net.minecraft.network.packet.CustomPayload;
import net.minecraft.util.Identifier;

public final class TestActionPackets {

    // C2S: client requests a test action
    public record C2STestAction() implements CustomPayload {
        public static final CustomPayload.Id<C2STestAction> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "c2s_test_action"));
        public static final PacketCodec<PacketByteBuf, C2STestAction> CODEC =
                PacketCodec.unit(new C2STestAction());

        @Override
        public CustomPayload.Id<C2STestAction> getId() {
            return ID;
        }
    }

    // S2C: server acknowledges the test action
    public record S2CAck(boolean allowed, int cooldownTicks) implements CustomPayload {
        public static final CustomPayload.Id<S2CAck> ID =
                new CustomPayload.Id<>(Identifier.of("avatar_elements", "s2c_ack"));
        public static final PacketCodec<PacketByteBuf, S2CAck> CODEC = PacketCodec.of(
                (value, buf) -> {
                    buf.writeBoolean(value.allowed());
                    buf.writeVarInt(value.cooldownTicks());
                },
                buf -> new S2CAck(buf.readBoolean(), buf.readVarInt())
        );

        @Override
        public CustomPayload.Id<S2CAck> getId() {
            return ID;
        }
    }

    private TestActionPackets() {}
}
