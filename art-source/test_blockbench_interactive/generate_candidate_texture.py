import os
import math
from PIL import Image

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\test_blockbench_interactive"
tex_cand_path = os.path.join(out_dir, "air_staff_candidate.png")

tex = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
pix = tex.load()

# 1. SHAFT WOOD (X: 0..16, Y: 0..16) — Serat Memanjang Vertikal Sepanjang Sumbu Y
# Hindari belang kotak berulang: gunakan variasi kolom vertikal x yang halus sepanjang y
c_wood_dark   = (148,  96, 52, 255) # Bayangan serat tepi
c_wood_base   = (176, 122, 74, 255) # Warna dasar kayu ash
c_wood_mid    = (192, 138, 88, 255) # Serat midtone alami
c_wood_light  = (212, 160, 108, 255) # Kilau serat memanjang
c_wood_pore   = (132,  84, 44, 255) # Pori serat kayu sesekali

for y in range(0, 16):
    for x in range(0, 16):
        # Pola serat memanjang: dominan variasi fungsi x (kolom), dengan variasi lembut sepanjang y
        # Tidak ada (x * 3 + y * 7) % 5 yang menghasilkan catur!
        col = x % 2 # Setiap face (lebar 2px) memiliki kolom kiri dan kanan
        
        # Variasi vertikal panjang (gelombang lembut frekuensi rendah)
        y_mod = (y + (x // 2) * 3) % 8
        
        if col == 0:
            # Kolom kiri: sedikit lebih teduh / bertekstur
            if y_mod in (0, 7):
                pix[x, y] = c_wood_dark
            elif y_mod in (1, 2):
                pix[x, y] = c_wood_base
            elif y_mod == 3:
                pix[x, y] = c_wood_pore # pori serat sesekali
            else:
                pix[x, y] = c_wood_mid
        else:
            # Kolom kanan: kilau serat kayu
            if y_mod in (1, 2, 3):
                pix[x, y] = c_wood_light # serat terang memanjang
            elif y_mod in (4, 5):
                pix[x, y] = c_wood_mid
            else:
                pix[x, y] = c_wood_base

# 2. GRIP LINEN WRAP (X: 16..24, Y: 0..6) — Lilitan Diagonal yang Terbaca Jelas
# 4 sisi: north (16..18), east (18..20), south (20..22), west (22..24)
# Lebar total 8 piksel membungkus silinder, tinggi 6 piksel.
c_seam = (138, 124, 104, 255) # Bayangan alur sambungan pita lilitan (deep seam)
c_mid  = (204, 196, 180, 255) # Badan kain linen krem (unbleached linen mid)
c_high = (238, 234, 224, 255) # Punggung pita lilitan (highlight ridge)
c_soft = (220, 214, 200, 255) # Sisi landai pita (soft highlight)

for y in range(0, 6):
    for x in range(16, 24):
        u = x - 16 # 0 s/d 7
        v = y      # 0 s/d 5
        # Lilitan diagonal: sudut kemiringan teratur mengalir melingkari 4 sisi
        diag = (u + v) % 4
        if diag == 0:
            pix[x, y] = c_seam # Alur batas lilitan
        elif diag == 1:
            pix[x, y] = c_mid  # Badan lilitan bawah
        elif diag == 2:
            pix[x, y] = c_high # Puncak timbul lilitan kain
        else:
            pix[x, y] = c_soft # Transisi lilitan atas

# Tutup atas dan bawah balutan kain (X: 16..20, Y: 6..8)
for y in range(6, 8):
    for x in range(16, 20):
        if (x + y) % 2 == 0:
            pix[x, y] = c_soft
        else:
            pix[x, y] = c_mid

# Area sisa kuadran grip (X: 20..32, Y: 6..16) diisi linen cadangan
for y in range(8, 16):
    for x in range(16, 32):
        diag = (x + y) % 4
        if diag == 0:
            pix[x, y] = c_seam
        elif diag == 2:
            pix[x, y] = c_high
        else:
            pix[x, y] = c_mid

# 3. END CAPS (X: 0..16, Y: 16..20) — Kayu Ujung Padat Gelap (Lower & Upper Cap)
c_cap_base = (102, 72, 48, 255)
c_cap_rim  = (128, 92, 64, 255)
c_cap_dark = (76,  52, 34, 255)

for y in range(16, 20):
    for x in range(0, 16):
        if y == 16 or y == 19:
            pix[x, y] = c_cap_rim
        elif x % 2 == 0:
            pix[x, y] = c_cap_base
        else:
            pix[x, y] = c_cap_dark

# 4. FIBER ACCENTS (X: 16..32, Y: 16..32) — Serat Kayu Pendukung
for y in range(16, 32):
    for x in range(16, 32):
        v_streak = ((x - 16) + (y - 16) * 3) % 7
        if v_streak in (0, 1):
            pix[x, y] = c_wood_dark
        elif v_streak in (2, 3):
            pix[x, y] = c_wood_base
        elif v_streak in (4, 5):
            pix[x, y] = c_wood_mid
        else:
            pix[x, y] = c_wood_light

tex.save(tex_cand_path, "PNG")
print("Saved candidate texture to:", tex_cand_path)
