> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# TESTING.md — Panduan Pengujian

> Sinkronisasi workflow 2026-11-08: dokumen ini mencakup Fabric mod dan menyimpan beberapa skenario datapack lama. Bagian Avatar State, Earth Wall, scoreboard, dan `/function` di bawah bukan bukti atau prosedur yang valid untuk runtime Fabric saat ini; perlakukan sebagai checklist legacy/rencana sampai fitur dan command terkait benar-benar tersedia.

## Alur verifikasi yang berlaku

1. `.\gradlew.bat build` dari `mod/` untuk kompilasi Fabric.
2. Jalankan suite Python yang relevan dari `tests/` secara terpisah; file-file tersebut bukan test source Gradle dan belum memiliki manifest dependency/runner proyek yang terverifikasi. Sebagian script menetapkan `D:\repo\Minecraft Mod & Rp` sebagai root, jadi periksa path sebelum dijalankan di workspace lain.
3. Uji manual hanya pada world QA terisolasi, ikuti `MANUAL_TESTING_GUIDE.md` setelah memastikan langkahnya cocok dengan source aktif.
4. Catat build, automated test, dan hasil Minecraft sebagai status terpisah di `TASKS.md`. Jangan menandai in-game verification hanya berdasarkan build atau keberadaan test.

State pemain saat ini menggunakan Fabric `AttachmentType` dan tidak persisten lintas sesi; jangan memakai scoreboard datapack sebagai pemeriksaan state mod.

## Status pengujian

Setiap fitur harus mencatat status berikut secara terpisah sebelum merge:
1. **Build** — `.\gradlew.bat build` tanpa error.
2. **Automated checks** — jalankan test/validator yang benar-benar mencakup perubahan. Jangan menganggap `gradlew test` mencakup suite Python di `tests/`.
3. **Minecraft runtime** — user mengonfirmasi uji manual/multiplayer yang sesuai; build dan static checks tidak membuktikan perilaku runtime.

## Pengujian singleplayer

### Skill dasar
- [ ] Skill aktif saat cooldown = 0
- [ ] Skill ditolak (pesan muncul) saat cooldown > 0
- [ ] Skill ditolak saat chi tidak cukup
- [ ] Chi berkurang sesuai nilai di CONTENT_SPEC.md
- [ ] Cooldown dimulai setelah cast, bukan sebelum
- [ ] Animasi mulai sebelum hitbox aktif (windup_ticks)
- [ ] Hitbox aktif pada frame yang benar
- [ ] VFX muncul bersamaan hitbox
- [ ] Suara muncul bersamaan hitbox

### Kombo
- [ ] Serangan kedua hanya bisa masuk dalam combo_window_ticks
- [ ] Mengganti senjata saat kombo membatalkan kombo
- [ ] Terkena stagger membatalkan kombo
- [ ] Cooldown tidak direset oleh pergantian senjata

### Movement
- [ ] Fire Jet tidak menembus dinding (block check)
- [ ] Fire Jet tidak melempar pemain ke void (edge check)
- [ ] Fallback jarak pendek berjalan saat jalur penuh terblokir

### Avatar State
- [ ] Tidak aktif saat mastery semua elemen belum terbuka
- [ ] Tidak aktif saat chi < 50
- [ ] Tidak aktif saat cooldown > 0
- [ ] Chi berkurang 50 saat aktivasi
- [ ] Efek (Resistance, Speed, Strength, Regeneration) hanya amplifier 1
- [ ] Cooldown 200 ticks muncul setelah Avatar State habis
- [ ] Tidak aktif kembali selama cooldown

### Earth Wall
- [ ] Blok muncul di posisi yang benar
- [ ] Blok hilang setelah 140 ticks (7 detik)
- [ ] Marker entity dihapus setelah blok hilang
- [ ] Tidak ada marker leak di chunk yang di-unload

## Pengujian multiplayer (dedicated server)

### Setup minimal
- Dua client terhubung ke dedicated server
- Latency simulasi: 100ms (gunakan network throttle tool)

### Skenario wajib
- [ ] Dua pemain menyerang bersamaan — tidak ada overlap damage yang salah
- [ ] Cooldown server authority — client cepat tidak bisa bypass cooldown
- [ ] Chi server authority — client tidak bisa cast tanpa chi yang cukup
- [ ] Reconnect saat skill aktif — state tersimpan dengan benar
- [ ] Earth Wall terlihat oleh pemain lain
- [ ] VFX skill terlihat oleh pemain lain (S2C_AnimationTrigger)

### Performa
- [ ] 20 TPS terjaga saat 2 pemain menggunakan skill bersamaan
- [ ] Tidak ada marker entity leak setelah 5 menit pertarungan
- [ ] Paket jaringan per detik tidak melebihi 50/pemain saat idle

## Skenario edge case

| Skenario | Cara menguji | Hasil yang diharapkan |
|---|---|---|
| Mati saat skill aktif | Cast skill, langsung /kill | Skill dibatalkan, cooldown tidak dimulai |
| Respawn | Mati dan respawn | Chi direset ke max, cooldown = 0 |
| Restart server | Cast skill, hentikan server, restart | Chi dan mastery tersimpan, cooldown = 0 |
| Pindah dimensi | Aktif Avatar State, masuk nether | Avatar State dibatalkan |
| Input cepat berulang | Klik skill > 20x per detik | Hanya cast pertama yang valid, sisanya diabaikan |
| Chi habis saat channeling | Gunakan skill channeling, biarkan chi habis | Skill dibatalkan, pesan muncul |

## Tools legacy datapack (bukan pemeriksaan state Fabric)

```bash
# Lihat scoreboard chi pemain
/scoreboard players get <player> avatar_chi

# Cek cooldown
/scoreboard players get <player> avatar_cd

# Cek Avatar State
/scoreboard players get <player> avatar_state

# Reset semua stats (untuk ulang test)
/function avatar_skills:tree/init_player
```

## Prosedur Uji In-Game Terisolasi (Milestone 4 & Milestone 5)

> Siapkan world pengujian terisolasi (flat world / test world kosong). Jangan gunakan save utama.
> Jalankan client dengan `.\gradlew runClient` dari folder `mod/`.

### Prosedur Uji 1: Fire Jab (Milestone 4 — Fase C)
1. Pilih elemen `FIRE` (tekan `R` hingga muncul indikator Fire di action bar).
2. Spawn target entity uji (contoh: `/summon zombie ~ ~ ~2 {NoAI:1b}`).
3. Amati pose idle: pemain berada dalam ready stance.
4. Tekan tombol `Z` (Slot 1: `fire_jab`):
   - **Antisipasi (2 tick / 0.10 detik):** Lengan kanan ditarik ke belakang, charge orb oranye menyala di kepalan tangan kanan.
   - **Strike (3 tick / 0.15 detik, eksekusi di tick 1 active / tick 3 absolut):**
     - Kepalan tangan kanan memukul ke depan.
     - Knuckle VFX: partikel api (`flame`) memancar tepat dari ujung kepalan tangan kanan (terlacak 1:1 via `KnuckleVfxHelper`).
     - Jet flame meluncur ke arah pandang.
     - Suara woosh api (`fire_release` / `blaze_shoot`) berbunyi serempak.
     - Zombie menerima damage 4.0 HP dan terkena knockback 0.3 blok.
   - **Recovery (4 tick / 0.20 detik):** Lengan dan tubuh kembali mulus 100% identik ke pose awal (zero-delta pose recovery).
   - Cooldown 6 tick (0.3s) tertera di HUD dan chi berkurang 8 poin.
5. Uji perspektif:
   - Tekan `F5` (third-person): charge orb menempel di kepalan tangan kanan dan berotasi saat tubuh bergerak.
   - Tekan `F5` kembali (first-person): charge orb tampil di ruang viewmodel kanan bawah tanpa menutupi crosshair.

### Prosedur Uji 2: Fire Blast Hold-Release (Milestone 5 — Fase D)
1. Pilih elemen `FIRE`.
2. Tekan dan tahan tombol `X` (Slot 2: `fire_blast`):
   - Pemain memasuki fase **HOLD** (chi berkurang 20 poin).
   - Charge orb muncul di kepalan tangan kanan.
   - Semakin lama tombol ditahan (hingga 40 tick / 2 detik):
     - Charge orb membesar secara visual dari radius 0.20 hingga 0.45 (third-person) / 0.06 hingga 0.14 (first-person).
3. Lepaskan tombol `X`:
   - Transisi ke fase **ACTIVE**.
   - Bola api (`FireBall`) berkecepatan 1.8 blok/tick meluncur lurus ke arah crosshair pemain.
   - Partikel trail api dan asap membuntuti bola api di udara.
   - Saat mengenai target atau blok:
     - Ledakan AOE (`explosion`, `flame`, `lava`) meledak di titik benturan.
     - Suara ledakan terdengar.
     - Semua entity dalam radius ledakan (1.0 blok untuk tap cepat s/d 3.0 blok untuk full charge) menerima damage (2.45 s/d 7.0 HP) dan knockback.
   - Cooldown 20 tick (1.0s) mulai berjalan di HUD.
4. Uji interupsi hold:
   - Tahan tombol `X`, lalu ubah dunia / dimensi atau `/kill`: charge orb langsung hilang seketika dan state hold bersih tanpa kebocoran memory.

---

## Acceptance tests W — belum dijalankan (2026-11-08)

Jalankan world mutation hanya pada world uji terisolasi yang diizinkan. Jangan gunakan save pengguna.

| Area | Kasus | Hasil wajib |
|---|---|---|
| Material | Ambil → wall → launch → pecah/endap → reclaim | Total material sesuai ledger; VFX tidak memberi drop tambahan |
| Race | Dua pemain mengambil blok/wadah sama | Satu transaksi menang; biaya dan material transaksi gagal konsisten |
| Cancel | Cancel di setiap langkah transaksi | Tidak ada sumber terhapus tanpa representasi atau material ganda |
| Persistence | Save/restart, chunk unload, pemilik disconnect/pindah dimensi | Konstruksi/material dipulihkan atau diselesaikan tepat sekali |
| Restore | Pemain lain membangun di lokasi sumber | Bangunan baru tidak ditimpa; konflik tercatat dan material direkonsiliasi |
| Wall | Raise dari blok valid lalu kick | Seluruh wall meluncur; asal meninggalkan bekas |
| Collision | Wall cepat melintasi target/dinding | Tidak tunneling; damage per target dibatasi aturan |
| Permissions | Source/target claim, PvP off, friendly fire | Utility tidak membypass aturan combat/world |
| Heat | Memasak di tangan vs panas terarah | Resep/input tepat; memasak tidak otomatis merusak entity sekitar |
| Fluid | Isi wadah kecil/besar, flow/source dan lava | Volume konsisten; tidak membuat infinite fluid/duplikasi bucket |
| Mining | Ore + tier/loot/enchantment/XP | Mengikuti kontrak hasil, tidak farm XP berulang |
| Profesi | Master elemen tanpa unlock profesi | Teknik pekerjaan tetap ditolak dengan alasan jelas |
| Air ride | Durasi panjang dan knock/stagger | Tidak mati karena timer; interrupt sesuai aturan; jatuh sesuai kontrak |
| Build | Preview lalu izin/material berubah sebelum confirm | Server validasi ulang; transaksi aman saat gagal |
| Presentasi | First person dan pemain pengamat | Attachment, serial, phase dan cleanup konsisten |
| Performa | Batas material/konstruksi/batch dilewati | Ditolak/dibagi aman; tidak membekukan tick server |

Catat tiap hasil: commit, config hash, environment, langkah, expected/actual, log/screenshot, PASS/FAIL/NOT RUN.

---

## Acceptance UI — BELUM DIJALANKAN (2026-11-08)

| Kasus | Hasil wajib |
|---|---|
| AUTO dan ganti elemen | Bingkai tetap tribe, aksen slot mengikuti elemen |
| Tema manual/minimal | Mengubah tampilan saja; resource/unlock tidak berubah |
| Resolusi/GUI scale/bahasa | Teks, pencarian, scroll dan tooltip terbaca; tidak keluar layar |
| Apply/Cancel/Reset/restart | Preferensi tersimpan tepat; cancel tidak menyimpan preview |
| Keyboard/reduced motion | Fokus terlihat; menu langsung bisa dipakai tanpa menunggu animasi gulungan |
| Screen saat combat | Klik/scroll/key tidak membocorkan cast atau hotbar; close tidak membuat hold macet |
| Server authority | Pemain biasa tidak mengubah chi, unlock, terrain rules dari UI |
| Missing state | Tema netral dan placeholder berlabel; tidak mengarang data player |
| HUD bersama vanilla/mod lain | Tidak ada bar duplikat atau overlap tak bisa diatur; bossbar/chat/subtitle/mount teruji |
| Fitur belum tersedia | Widget hidden/disabled jelas; bukan tombol live palsu |

Acuan desain: UI_THEME_SPEC.md. Simpan bukti per commit dan bedakan mockup dari screenshot runtime.
