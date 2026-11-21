package com.avatarmod.elements.client.screen;

import com.avatarmod.elements.client.hud.ElementWheelRenderer;
import com.avatarmod.elements.client.network.SkillClientHandler;
import com.avatarmod.elements.skill.ElementSlotMap;
import com.avatarmod.elements.skill.SkillRegistry;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.text.Text;
import org.lwjgl.glfw.GLFW;

import java.util.ArrayList;
import java.util.List;

/**
 * Interactive Skill Tree & Mastery Screen.
 * Visualizes basic elemental skills, advanced sub-bending paths (Lightning, Metal, Blood, Flight, etc.),
 * and allows instant unlock / testing when in Creative mode or Sandbox bypass.
 */
public final class SkillTreeScreen extends Screen {

    private String activeElement;
    private final List<SkillNode> nodes = new ArrayList<>();

    public record SkillNode(
            String id,
            String name,
            String subType,
            int tier,
            int x,
            int y,
            int color,
            String desc,
            boolean isSubBending
    ) {}

    public SkillTreeScreen() {
        super(Text.literal("§6§lAvatar Elemental Skill Tree & Mastery"));
        this.activeElement = ElementWheelRenderer.getCurrentElement();
        if (this.activeElement == null || "NONE".equals(this.activeElement)) {
            this.activeElement = "FIRE";
        }
    }

    @Override
    protected void init() {
        buildSkillTreeNodes();
    }

    private void buildSkillTreeNodes() {
        nodes.clear();
        int centerX = width / 2;
        int startY = 70;

        // Base elemental branches based on activeElement
        switch (activeElement) {
            case "FIRE" -> {
                // Main branch: Firebending (Tier 1-3)
                nodes.add(new SkillNode("avatar:fire_jab", "Fire Jab", "Fire Basic", 1, centerX - 120, startY, 0xFFFF4500, "Serangan cepat kepalan api jarak dekat.", false));
                nodes.add(new SkillNode("avatar:fire_blast", "Fire Blast", "Fire Basic", 2, centerX - 120, startY + 45, 0xFFFF3300, "Tembakan bola api berdaya ledak sedang.", false));
                nodes.add(new SkillNode("avatar:flame_sweep", "Flame Sweep", "Fire Master", 3, centerX - 120, startY + 90, 0xFFFF2200, "Ayunan cambuk kobaran api melingkar luas.", false));
                nodes.add(new SkillNode("avatar:fire_jet", "Fire Jet", "Mobility", 3, centerX - 120, startY + 135, 0xFFFF6600, "Propulsi api untuk meluncur dan melesat.", false));

                // Sub-bending branch: Lightning Generation & Combustion
                nodes.add(new SkillNode("avatar:lightning_strike", "Lightning Strike", "Sub-Bending: Kilat", 4, centerX + 60, startY + 20, 0xFF00E5FF, "Tembakan petir murni berdaya hancur tinggi.", true));
                nodes.add(new SkillNode("avatar:combustion_blast", "Combustion Beam", "Sub-Bending: Peledak", 5, centerX + 60, startY + 75, 0xFFFF0055, "Ledakan terarah jarak jauh dengan gelombang kejut dahsyat.", true));
                nodes.add(new SkillNode("avatar:dragon_fire", "Dragon Fire (Sun Warriors)", "Ancient Form", 5, centerX + 60, startY + 130, 0xFFFFD700, "Api abadi berwarna-warni dengan efisiensi Chi sempurna.", true));
            }
            case "AIR" -> {
                // Main branch: Airbending (Tier 1-3)
                nodes.add(new SkillNode("avatar:air_palm", "Air Palm", "Air Basic", 1, centerX - 120, startY, 0xFFE0FFFF, "Dorongan angin telapak tangan berdaya tolak tinggi.", false));
                nodes.add(new SkillNode("avatar:air_blast", "Air Blast", "Air Basic", 2, centerX - 120, startY + 45, 0xFFB0E0E6, "Pukulan angin jarak jauh penyapu lawan.", false));
                nodes.add(new SkillNode("avatar:air_staff_attack", "Air Staff Kata", "Martial Air", 3, centerX - 120, startY + 90, 0xFF87CEEB, "Rangkaian kombo tongkat angin 3-pukulan akrobatik.", false));
                nodes.add(new SkillNode("avatar:air_scooter", "Air Scooter", "Mobility", 2, centerX - 120, startY + 135, 0xFFE6E6FA, "Menunggangi bola angin berputar tanpa batas waktu.", false));

                // Sub-bending branch: True Flight (Guru Laghima) & Spiritual Projection
                nodes.add(new SkillNode("avatar:air_vortex", "Air Vortex", "Advanced Control", 4, centerX + 60, startY + 20, 0xFFADD8E6, "Pusaran angin tornado penyedot proyektil lawan.", false));
                nodes.add(new SkillNode("avatar:unsupported_flight", "Weightlessness (Flight)", "Sub-Bending: Terbang", 5, centerX + 60, startY + 75, 0xFFF0F8FF, "Kemampuan terbang bebas di angkasa tanpa batas energi.", true));
                nodes.add(new SkillNode("avatar:spiritual_projection", "Spiritual Projection", "Spiritual Mastery", 5, centerX + 60, startY + 130, 0xFFD8BFD8, "Menembus rintangan dan memproyeksikan wujud roh.", true));
            }
            case "WATER" -> {
                // Main branch: Waterbending (Tier 1-3)
                nodes.add(new SkillNode("avatar:water_whip", "Water Whip", "Water Basic", 1, centerX - 120, startY, 0xFF1E90FF, "Cambuk air fleksibel pemotong musuh.", false));
                nodes.add(new SkillNode("avatar:water_jet", "Water Jet", "Water Basic", 2, centerX - 120, startY + 45, 0xFF00BFFF, "Pancaran air deras bertekanan tinggi.", false));
                nodes.add(new SkillNode("avatar:octopus_form", "Octopus Form", "Water Defense", 3, centerX - 120, startY + 90, 0xFF4682B4, "8 tentakel air pelindung yang menepis proyektil.", false));
                nodes.add(new SkillNode("avatar:water_surf", "Water Surf", "Mobility", 2, centerX - 120, startY + 135, 0xFF5F9EA0, "Berselancar di atas ombak air dengan kecepatan tinggi.", false));

                // Sub-bending branch: Healing & Bloodbending
                nodes.add(new SkillNode("avatar:healing_water", "Water Healing", "Sub-Bending: Penyembuh", 3, centerX + 60, startY + 20, 0xFF40E0D0, "Memulihkan darah sekutu dan membersihkan efek racun.", true));
                nodes.add(new SkillNode("avatar:ice_spikes", "Ice Spikes", "Phase Change", 4, centerX + 60, startY + 75, 0xFFAFEEEE, "Membekukan air menjadi tombak es mematikan.", false));
                nodes.add(new SkillNode("avatar:bloodbending", "Bloodbending (Full Moon)", "Forbidden Sub-Bending", 5, centerX + 60, startY + 130, 0xFF8B0000, "Mengendalikan cairan tubuh musuh secara mutlak.", true));
            }
            case "EARTH" -> {
                // Main branch: Earthbending (Tier 1-3)
                nodes.add(new SkillNode("avatar:earth_boulder", "Earth Boulder", "Earth Basic", 1, centerX - 120, startY, 0xFF8B5A2B, "Melempar bongkahan batu dengan auto-target.", false));
                nodes.add(new SkillNode("avatar:boulder_launch", "Megalith Launch", "Earth Heavy", 2, centerX - 120, startY + 45, 0xFF654321, "Menghisap tanah lalu melontarkan batu raksasa.", false));
                nodes.add(new SkillNode("avatar:earth_pillar", "Earth Pillar", "Tactical Earth", 3, centerX - 120, startY + 90, 0xFF70543E, "Mencuatkan pilar batu (Dapat ditendang/dipukul).", false));
                nodes.add(new SkillNode("avatar:earth_wall", "Earth Wall", "Defense", 2, centerX - 120, startY + 135, 0xFF5C4033, "Dinding pelindung tanah kokoh penahan serangan.", false));

                // Sub-bending branch: Metalbending, Lavabending & Seismic Sense
                nodes.add(new SkillNode("avatar:seismic_sense", "Seismic Sense (Toph)", "Sensory Earth", 3, centerX + 60, startY + 20, 0xFFDAA520, "Mendeteksi semua pergerakan musuh melalui tanah.", true));
                nodes.add(new SkillNode("avatar:metalbending", "Metalbending", "Sub-Bending: Logam", 4, centerX + 60, startY + 75, 0xFF708090, "Mengendalikan kabel logam dan baju zirah besi.", true));
                nodes.add(new SkillNode("avatar:lavabending", "Lavabending (Ghazan)", "Sub-Bending: Lava", 5, centerX + 60, startY + 130, 0xFFFF4500, "Mencairkan batu menjadi magma panas yang membara.", true));
            }
            default -> { // NON_BENDER
                nodes.add(new SkillNode("avatar:chi_strike", "Chi Strike", "Martial Arts", 1, centerX - 120, startY, 0xFFC0C0C0, "Pukulan cepat penyumbat aliran energi musuh.", false));
                nodes.add(new SkillNode("avatar:acrobatic_dodge", "Acrobatic Dodge", "Mobility", 2, centerX - 120, startY + 45, 0xFFA9A9A9, "Gerakan akrobatik menghindar dari proyektil elemen.", false));
                nodes.add(new SkillNode("avatar:grapple_wire", "Grapple Wire", "Gadget", 3, centerX - 120, startY + 90, 0xFF696969, "Kabel penarik untuk bermanuver di tebing dan bangunan.", false));
                nodes.add(new SkillNode("avatar:smoke_bomb", "Smoke Bomb", "Tactical", 2, centerX - 120, startY + 135, 0xFF505050, "Bom asap untuk membutakan penglihatan musuh.", false));

                nodes.add(new SkillNode("avatar:nerve_strike", "Nerve Severance (Ty Lee)", "Sub-Path: Chi Blocker", 4, centerX + 60, startY + 45, 0xFFFF69B4, "Melumpuhkan kemampuan elemen lawan total selama 8 detik.", true));
                nodes.add(new SkillNode("avatar:electrified_gauntlet", "Shock Gauntlet (Equalist)", "Sub-Path: Tech Weapon", 5, centerX + 60, startY + 105, 0xFF00CED1, "Sarung tangan listrik penyengat dengan efek stun tinggi.", true));
            }
        }
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        // Semi-transparent background
        context.fill(0, 0, width, height, 0xD0100C08);

        int centerX = width / 2;

        // Title and Element Banner
        context.drawCenteredTextWithShadow(textRenderer, title, centerX, 18, 0xFFFFD700);
        context.drawCenteredTextWithShadow(textRenderer,
                Text.literal("§7Jalur Elemen: §e" + activeElement + " §7(Tekan §6[G] §7untuk ganti elemen)"),
                centerX, 34, 0xFFE8D8C3);

        // Creative / Testing Mode notice
        boolean creative = client != null && client.player != null && client.player.isCreative();
        String modeNotice = creative
                ? "§a[Mode Kreatif / Sandbox] Semua skill dan sub-bending terbuka langsung untuk uji coba!"
                : "§e[Hardcore Progression] Kalahkan Mini-Boss untuk membuka Sub-Bending (Opsi A & B Aktif)";
        context.drawCenteredTextWithShadow(textRenderer, Text.literal(modeNotice), centerX, 50, 0xFFFFFFFF);

        // Render Branch Labels
        context.drawTextWithShadow(textRenderer, Text.literal("§6► Jurus Dasar & Seni Bela Diri"), centerX - 180, 56, 0xFFFFAA00);
        context.drawTextWithShadow(textRenderer, Text.literal("§d► Cabang Sub-Bending Khusus"), centerX + 20, 56, 0xFFFF55FF);

        SkillNode hoveredNode = null;

        // Render Nodes
        for (SkillNode node : nodes) {
            boolean hovered = mouseX >= node.x && mouseX < node.x + 130 && mouseY >= node.y && mouseY < node.y + 36;
            if (hovered) hoveredNode = node;

            int borderCol = hovered ? 0xFFFFFFFF : (node.isSubBending ? 0xFFFFD700 : 0xFF888888);
            int bgCol = hovered ? (node.color | 0x88000000) : 0xBB201A15;

            // Box
            context.fill(node.x - 2, node.y - 2, node.x + 132, node.y + 38, borderCol);
            context.fill(node.x, node.y, node.x + 130, node.y + 36, bgCol);

            // Icon / Indicator
            context.fill(node.x + 4, node.y + 4, node.x + 10, node.y + 32, node.color);

            // Texts
            context.drawTextWithShadow(textRenderer, Text.literal("§f" + node.name), node.x + 16, node.y + 6, 0xFFFFFFFF);
            context.drawTextWithShadow(textRenderer, Text.literal("§7" + node.subType + " §8[Tier " + node.tier + "]"),
                    node.x + 16, node.y + 20, 0xFFAAAAAA);
        }

        // Draw Tooltip if hovering a node
        if (hoveredNode != null) {
            List<Text> tooltip = new ArrayList<>();
            tooltip.add(Text.literal("§e§l" + hoveredNode.name));
            tooltip.add(Text.literal("§bKategori: §f" + hoveredNode.subType));
            tooltip.add(Text.literal("§6Tingkat Mastery Diperlukan: §fTier " + hoveredNode.tier));
            tooltip.add(Text.literal("§7" + hoveredNode.desc));
            if (creative) {
                tooltip.add(Text.literal("§a✔ Bebas diuji coba kapan saja di Sandbox Mode."));
            } else {
                tooltip.add(Text.literal(hoveredNode.isSubBending
                        ? "§c✖ Kalahkan Mini-Boss elemen ini untuk membuka segel gulungan."
                        : "§e✔ Naikkan Mastery elemen untuk menggunakan jurus ini."));
            }
            context.drawTooltip(textRenderer, tooltip, mouseX, mouseY);
        }

        // Footer instructions
        context.drawCenteredTextWithShadow(textRenderer,
                Text.literal("§8Tekan [K] atau [ESC] untuk kembali ke permainan"), centerX, height - 18, 0xFF888888);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_K || keyCode == GLFW.GLFW_KEY_ESCAPE) {
            close();
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    @Override
    public boolean shouldPause() {
        return false;
    }
}
