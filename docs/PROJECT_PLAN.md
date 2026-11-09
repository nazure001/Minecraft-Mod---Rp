> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# PROJECT_PLAN.md — Rencana Pengembangan Avatar: Elements

Platform: Minecraft Java 1.21.1, Fabric  
Target: Singleplayer dan dedicated server  
Prinsip utama: **Satu serangan = satu timeline** (animasi, hitbox, VFX, suara, kombo)

## Tahapan pengerjaan

| Tahap | Hasil konkret | Syarat selesai |
|---|---|---|
| **0 — Audit** | Inventaris aset, bug, bonus armor, skill dan generator lama | Jalur aktivasi dan konflik diketahui ✅ |
| **1 — Fondasi** | Mod Fabric, keybind, networking, penyimpanan, konfigurasi bersama | Bisa berjalan di client dan dedicated server |
| **2 — Prototipe vertikal** | Api tangan kosong + tongkat udara; masing-masing kombo + skill | Gerakan, damage, VFX, dan suara sinkron |
| **3 — Empat elemen** | Skill dasar, pertahanan, dan movement tiap elemen | Tiap elemen punya fungsi berbeda |
| **4 — Equipment** | Migrasi armor dan perluasan senjata | Bonus dan pergantian item tidak mengeksploitasi sistem |
| **5 — Progression** | Mastery, skill tree, sub-bending, Avatar State | Progres tersimpan dan aturan unlock konsisten |
| **6 — Presentasi** | Penyempurnaan animasi, efek, audio, backsound | Nyaman pada beberapa kualitas grafis |
| **7 — Server beta** | Pengujian multiplayer, performa, balancing | Tidak ada bug kritis yang diketahui |
| **8 — Rilis** | Paket client/server, panduan, konfigurasi, changelog | Instalasi baru dan migrasi berhasil diuji |

## Target rilis pertama yang realistis

Empat elemen dasar, dua moveset senjata matang, armor yang sudah diaudit, HUD, progression sederhana, multiplayer stabil. Sub-bending kompleks dan kombo senjata tambahan menyusul setelah fondasi lolos pengujian.

## Ukuran keberhasilan

Tombol merespons dengan jelas, gerakan cocok dengan benturan, efek terbaca, pemain lain melihat kejadian yang konsisten.

## Elemen dan skill

### Api — tekanan, serangan cepat, ledakan
- Dasar: Fire Jab, Flame Sweep, Fire Guard, Fire Jet
- Lanjut: Charged Blast, Combustion, Lightning

### Air (WATER) — adaptasi, kendali, pertahanan
- Dasar: Water Whip, Water Jet, Ice Spear, Ice Shield
- Lanjut: Water Arms, Octopus Form, Healing

### Tanah — stabilitas, serangan berat, kontrol medan
- Dasar: Earth Boulder, Earth Wall, Ground Spike, Earth Guard
- Lanjut: Earth Launch, Seismic Sense, Metalbending, Lavabending

### Udara (AIR) — kelincahan, pengalihan, dorongan
- Dasar: Air Palm, Air Blast, Air Sweep, Air Cushion
- Lanjut: Air Scooter, Air Spout, Vortex, Flight

### Avatar — menggabungkan elemen
- Pergantian elemen dan kombo lintas elemen
- Avatar State + finisher gabungan

## Weapon

| Senjata | Kombo | Skill khas |
|---|---|---|
| Tangan kosong | Pukulan/tendangan sesuai elemen | Bending langsung |
| Tongkat udara | Tusuk → putar → sapu | Air Vortex |
| Pedang tunggal | Tebas → balik → tusuk | Focused Slash |
| Pedang ganda | Tebasan bergantian → silang | Dash Cross |
| Tombak | Tusukan → sapuan → dorongan | Piercing Thrust |
| Palu bumi | Ayunan berat → hantaman | Earth Shatter |
| Kipas | Sapuan cepat dan pengalihan | Deflecting Gust |
| Sarung tangan logam | Pukulan dan tarikan | Metal Tether |

---

## Roadmap perluasan — 2026-11-08

Status semua tahap baru: PLANNED. Tidak menjadikan semua katalog target rilis pertama.

| Urutan | Hasil | Gate |
|---|---|---|
| A–D aktif | Orb lifecycle, rig terbukti, Fire Jab lengkap, hold-release + Fire Blast | Build dan runtime dicatat terpisah; tidak mengubah scope agent aktif |
| W1 | Kontrak kemampuan: activation/duration/source/effects/progression | Satu schema dan jalur validasi; migrasi loader terdokumentasi |
| W2 | Ledger dan transaksi material | Konservasi, abort, restart, chunk unload dan contention lolos |
| W3 | Earth Wall raise → hold → launch → impact → reclaim | Pengambilan nyata dan seluruh wall bergerak; tidak menggandakan material |
| W4 | Satu utilitas per elemen dengan dampak PvP eksplisit | Pemanasan, pengisian, shaping, hembusan; izin dan hit gating lolos |
| W5 | Profesi dan latihan | Unlock selektif, persistence, anti-farming; bukan combat XP untuk semua |
| W6 | Konstruksi master/terraforming | Preview, konfirmasi, volume, batch, konflik/izin, multiplayer |
| W7 | Imbue, interaksi elemen dan teknik lanjut | Menggunakan fondasi yang sama, scope dipecah per fitur |

Keputusan terbuka: mode perubahan terrain default, unit fluida, chi sustain, profession cap,
material tags, hasil impact/drop, aturan konstruksi terbengkalai, target beban server.
Agent boleh mempersiapkan desain W1; implementasi world mutation baru setelah A–D dan gate W2.

---

## Jalur UI — presentasi gulungan (2026-11-08)

Acuan: `UI_THEME_SPEC.md`. Jalur UI tidak memperluas implementasi A–D yang berjalan.
Sesudah checkpoint aktif: wireframe HUD/menu → satu tema fungsional → tema tribe → profil/skill tree kontekstual.
Tidak perlu menunggu seluruh W1–W7 selesai untuk tema dasar; widget material/profesi bergantung pada kontrak data fitur terkait.
Gate: readability, GUI scale, navigation, apply/cancel/reset, server authority dan tidak mengganggu input combat.
Inventory vanilla, fitur sosial dan penyalinan tampilan Essential bukan scope awal.
