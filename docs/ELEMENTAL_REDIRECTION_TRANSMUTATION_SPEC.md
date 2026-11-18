# 🌀 Sistematika Intersepsi, Redireksi, & Transmutasi Elemen (Catch, Redirect & Earth Armor)
> **Dokumen Arsitektur & Spesifikasi Gameplay Lanjutan (Advanced PvP & Combat Mechanics)**  
> **Target:** Minecraft Fabric 1.21.1 (Avatar: Four Nations Elemental Suite)  
> **Status:** Arsitektur Disetujui — Kontrak Antar-Peran (User, Claude Code, Antigravity)  

---

## 1. Landasan Filosofis & Literatur Kanon (ATLA & LOK)

Dalam dunia *Avatar: The Last Airbender* dan *The Legend of Korra*, pertarungan antar-pengendali elemen sejenis bukanlah sekadar baku hantam damage searah, melainkan **dinamika aliran energi dan pengalihan momentum (*Flow & Redirection*)**:

1. **Pengendalian Tanah (Hung Gar & Southern Praying Mantis):**
   * **Menangkap (*Catch & Ground*):** Menahan hantaman batu lawan dengan kuda-kuda kokoh (*Ma Bu*), menyerap energi tumbukan ke dalam tanah.
   * **Memecah & Membalikkan (*Sharding & Catapulting*):** Memecah proyektil lawan menjadi piringan tajam atau serpihan, memutarnya, dan menendangnya kembali ke penyerang.
   * **Baju Zirah Batu (*Earth Armor*):** Mengumpulkan serpihan batu atau kristal di sekitar tubuh untuk ditempelkan sebagai lempeng pelindung tebal (seperti aksi Toph di Ba Sing Se dan Aang saat melawan Raja Api Ozai).
2. **Pengendalian Air (Tai Chi):**
   * Mengikuti aliran air lawan (*Push & Pull*), membelokkannya menjadi lingkaran pertahanan, atau membekukannya menjadi perisai es.
3. **Pengendalian Api (Northern Shaolin):**
   * *Fire Slicing / Dissipation:* Membelah lidah api lawan dengan ayunan tangan melingkar.
   * *Lightning Redirection (Iroh):* Mengalirkan petir masuk melalui satu lengan, melewati perut (*dantian*), dan mengeluarkannya lewat lengan lain tanpa menyentuh jantung.
4. **Pengendalian Angin (Baguazhang):**
   * Gerakan memutar menghindar melingkar (*circle walking*), menyerap badai lawan untuk mempercepat laju pusaran angin sendiri.

---

## 2. Diagram Alur Status Game (State Machine)

```
[Proyektil / Serangan Elemen Masuk]
               │
               ▼
   [Pemain Menahan Guard (Tombol V)] ──(Elemen Sama?)──► TIDAK ──► [Normal Guard Block / Damage]
               │ YA (Parry Window: 6 tick)
               ▼
    ┌──────────────────────────┐
    │ FASE 1: INTERCEPTION     │
    │ • Proyektil tidak meledak│
    │ • Damage = 0             │
    │ • Caster UUID dialihkan  │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────────────────────────┐
    │ FASE 2: CAPTURE BUFFER (Durasi: 30 tick/1.5s)│
    │ • Muncul 3D Serpihan/Energi Melayang         │
    │ • Pemain memegang kontrol sumber elemen      │
    └──────────┬───────────────────────────────┬───┘
               │                               │
        [Tekan Z / X]                   [Tekan Tahan V]
               │                               │
               ▼                               ▼
    ┌──────────────────────────┐    ┌──────────────────────────┐
    │ FASE 3A: REDIRECTION     │    │ FASE 3B: TRANSMUTATION   │
    │ • Serpihan dilempar balik│    │ • Menjadi Earth Armor    │
    │ • Kecepatan +25%         │    │ • Memberi Armor +6,      │
    │ • Damage bonus x1.2      │    │   Resistance I (10 detik)│
    └──────────────────────────┘    └──────────────────────────┘
```

---

## 3. Matriks Interaksi Antar-Elemen

| Elemen Penyerang | Elemen Bertahan | Mekanisme Intersepsi | Pilihan A (Redireksi) | Pilihan B (Transmutasi) |
|---|---|---|---|---|
| **Earth (Batu/Pillar)** | **Earth** | Entakan kuda-kuda menahan boulder | Melempar serpihan batu tajam kembali | Menempelkan batu ke badan (**Earth Armor**) |
| **Water (Whip/Jet)** | **Water** | Memutar arus air ke arah berlawanan | Membalikkan semburan air bertekanan | Membekukan air menjadi **Ice Shield / Armor** |
| **Fire (Blast/Jet)** | **Fire** | Ayunan belah api melingkar (*dissipation*) | Membalikkan gelombang api pekat | Menyerap energi menjadi **Heat Chi Surge** (Chi +25) |
| **Lightning** | **Fire** | Siklus petir Iroh (melalui perut) | Melontarkan petir kembali dengan 100% akurasi | Tidak ada (terlalu mematikan untuk diserap) |
| **Air (Blast/Vortex)** | **Air** | Langkah memutar melingkar (*Baguazhang*) | Membalikkan gelombang kejut angin | Mengubah hembusan menjadi **Air Scooter / Tailwind** |

---

## 4. Pembagian Peran Kerja (Triad Allocation)

### A. Game Director & Reviewer (User / Anda)
1. Menyetujui parameter timing (jendela parry $0.3\text{ detik}$, waktu buffer penahanan $1.5\text{ detik}$).
2. Menguji rasa pertarungan (*combat feel*) dan keseimbangan risiko vs hadiah (*risk-reward balance*) di Minecraft QA.

### B. Runtime & System Logic (Claude Code — `mod/src/`)
1. **`InterceptionHook`:** Mengaitkan event deteksi tabrakan proyektil/hitbox saat status pemain adalah `GUARDING`.
2. **`SameElementValidator`:** Memverifikasi `attacker.element == defender.element`.
3. **`CapturedStateController`:** Mengelola timer buffer $30\text{ tick}$ di server dan mendengarkan input reaksi pemain (Z/X untuk lempar balik, V untuk armor).
4. **`StatusEffectApplier`:** Memberikan efek status `avatar_elements:earth_armor` yang menaikkan atribut armor dan daya tahan ledakan selama 10 detik.
5. **`NetworkSync`:** Memancarkan paket S2C agar seluruh pemain di sekitar merender visual serpihan yang ditangkap.

### C. Produksi Aset 3D & VFX (Antigravity IDE — `art-source/asset_pack/`)
1. **`SM_Captured_Shards`:** Model 3D serpihan batu melayang berputar di sekitar pemain saat penangkapan berhasil.
2. **`SM_Earth_Armor_Plates`:** Model 3D lempeng pelindung batu pada dada, bahu, dan lengan pemain.
3. **`VFX_Redirection_Wave`:** Efek cincin kinetik saat lontaran balik dieksekusi.
4. **Animasi Tubuh (PAL):** Klip animasi gestur tangan memutar dan menyerap benturan.

---

## 5. Rencana Penerapan (Roadmap)

* **Fase 1 (Saat Ini):** Penyelesaian seluruh aset 3D Blockbench & visual VFX oleh Antigravity; integrasi VFX Earth Pillar oleh Claude Code.
* **Fase 2 (Berikutnya):** Implementasi logika deteksi Guard dan transfer proyektil di `mod/src/` oleh Claude Code mengacu pada dokumen ini.
* **Fase 3:** Integrasi model `Earth Armor` dan `Captured Shards` ke dalam event runtime.
