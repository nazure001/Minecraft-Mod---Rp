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

### Air — adaptasi, kendali, pertahanan
- Dasar: Air Palm, Air Blast, Air Sweep, Air Cushion
- Lanjut: Air Scooter, Air Spout, Vortex, Flight

### Tanah — stabilitas, serangan berat, kontrol medan
- Dasar: Earth Boulder, Earth Wall, Ground Spike, Earth Guard
- Lanjut: Earth Launch, Seismic Sense, Metalbending, Lavabending

### Air — kelincahan, pengalihan, dorongan
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
