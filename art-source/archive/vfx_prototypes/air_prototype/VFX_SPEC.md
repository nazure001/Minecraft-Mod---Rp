# SPESIFIKASI TEKNIS VFX: AIR PROTOTYPE TEXTURES
**Folder:** `art-source/vfx/air_prototype/`  
**Spesialis:** Subagent B (VFX Texture Specialist)  
**Tanggal:** 2026-11-07  

---

## 1. Ringkasan Aset

| File | Dimensi & Format | Deskripsi Visual | Radius / Karakteristik |
| :--- | :--- | :--- | :--- |
| `air_arc.png` | 128x128 RGBA (32-bit) | Crescent slash arc untuk tebasan & sapuan angin | Lengkungan busur 124°, tebal di pusat (17px), meruncing lembut di ujung, $\alpha_{\text{border}} = 0$ |
| `air_ring.png` | 128x128 RGBA (32-bit) | Expanding shockwave ring (cincin tekanan udara) | Radius puncak 44px, pusat transparan total ($r < 28\text{px}, \alpha=0$), margin luar 8px, $\alpha_{\text{border}} = 0$ |
| `preview_vfx_composite.png` | 640x420 RGB | Lembar pratinjau multi-latar | Pratinjau pada Dark Tone (#13161C), Sky Tone (#92B1D3), Alpha Checkerboard, & Simulasi Additive Glow |
| `generate_vfx_textures.py` | Python (PIL + NumPy) | Generator prosedural sumber | Dapat diedit ulang dengan supersampling 4x (512x512 Lanczos downsampling) untuk anti-aliasing presisi |

---

## 2. Palet Warna & Visual Falloff

Arah visual mengikuti elemen **Pale Air**:
- **Core Highlight:** `#F4FAFF` (RGB 244, 250, 255) — densitas tekanan tertinggi di inti.
- **Mid Air Body:** `#D8ECF8` (RGB 216, 236, 248) — rona putih kebiruan pucat khas hembusan angin.
- **Falloff Fringe:** `#B2DCF4` (RGB 178, 218, 244) — tepi dispersi udara lembut sebelum mencapai $\alpha = 0$.

> [!NOTE]
> **Anti-Bounding Box Guarantee:**
> Seluruh pixel pada koordinat tepi terluar ($x=0, 127$ dan $y=0, 127$) memiliki nilai alpha tepat **0**. Tidak ada garis potong kotak (bounding box edge artifacts) saat tekstur dirotasi atau di-scale dalam engine.

---

## 3. Orientasi & Pemetaan UV

### A. `air_arc.png`
- **Orientasi Kanvas:** Menghadap ke atas (puncak busur di kuadran atas, kedua ujung meruncing simetris ke bawah).
- **Sumbu Puncak:** $(X=64, Y=38)$.
- **Ujung Busur (Tips):** Kiri $(X\approx 22, Y\approx 92)$, Kanan $(X\approx 106, Y\approx 92)$.
- **Mapping Saran:**
  - **Billboard Slash:** Quad 1x1 menghadap kamera, dirotasi sesuai vektor sudut sapuan senjata/ayunan tongkat.
  - **Ribbon Trail:** Diterapkan pada mesh busur sabit (curved strip) di mana U terentang dari ujung ke ujung dan V terentang dari sisi dalam ke luar.

### B. `air_ring.png`
- **Orientasi Kanvas:** Lingkaran isotropik terpusat di $(X=64, Y=64)$.
- **Pusat Transparan:** Area $r < 28\text{px}$ dijamin transparan penuh ($\alpha = 0$). Tidak menutupi karakter atau target di titik tengah ledakan udara.
- **Puncak Tekanan:** $r = 44\text{px}$ dengan densitas alpha puncak ~82%.
- **Secondary Echo:** Riak mikro pada $r = 30\text{px}$ memberikan kesan distorsi akustik/gelombang kejut nyata (bukan sekadar donat polos).

---

## 4. Rekomendasi Blend Mode

1. **ALPHA BLEND (`GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`):**
   - **Rekomendasi Utama untuk Siang Hari / Latar Terang:**
     Mencegah efek visual "tercuci" (washed out) saat pemain menghadap langit cerah, pasir gurun, atau salju.
   - Warna `#D8ECF8` tetap terbaca dengan siluet lembut.

2. **ADDITIVE BLEND (`GL_SRC_ALPHA, GL_ONE`):**
   - **Rekomendasi untuk Gua Gelap / Malam Hari / Burst Mantradaya:**
     Memberikan pendaran hembusan angin bertekanan tinggi tanpa menggelapkan latar belakang di malam hari.
   - Karena warna dasarnya putih pucat kebiruan, additive tidak menyebabkan saturasi silau neon berlebih.

3. **Vanilla Minecraft Translucent:**
   - Cocok langsung dengan pipeline render partikel standar Minecraft (`RenderType.translucent()` atau Particle Render Sheet `PARTICLE_SHEET_TRANSLUCENT`).

---

## 5. Usulan Penggunaan (Partikel / Billboard / Mesh)

- **Air Gust / Slash Particle (`air_arc.png`):**
  - Digunakan saat eksekusi skill sapuan angin (misal: hembusan tebasan tongkat udara).
  - Skala awal: $0.4$, membesar ke $1.2$ dalam durasi singkat ($4 - 8$ ticks) sambil memudar (fade out alpha).
- **Shockwave Ring / Updraft Burst (`air_ring.png`):**
  - **Planar Billboard:** Ditempatkan datar sejajar permukaan tanah (pitch $90^\circ$, XZ plane) saat karakter mendarat atau melakukan double jump / air leap.
  - **Cylindrical Mesh:** Ditumpuk vertikal dengan radius membesar bertahap untuk efek pusaran angin / updraft kolom.

---

## 6. Batasan & Status Pengujian

> [!CAUTION]
> **Pemberitahuan Pembatas Proyek:**
> - Aset ini adalah **art source prototype** murni.
> - **TIDAK** ada renderer kustom yang dibuat pada fase ini.
> - **JANGAN** mengklaim efek ini sudah berjalan atau diuji di dalam game runtime Minecraft.
> - File mod Java, skrip build Gradle, dan aset staff yang telah dibekukan **TIDAK TERSENTUH**.

### Aspek yang Belum Diuji:
1. Perilaku tampilan di bawah shader pack pihak ketiga (misal: Iris/Oculus, Complementary/BSL Shaders) terkait kedalaman depth buffer dan penanganan blend mode additive.
2. Interpolasi mipmap Minecraft standar pada resolusi 128x128 jika partikel berada di jarak jauh (LOD falloff).
3. Evaluasi kenyamanan visual saat di-render puluhan partikel sekaligus (overdraw check di area sempit).
