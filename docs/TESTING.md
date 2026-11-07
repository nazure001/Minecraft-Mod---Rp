# TESTING.md — Panduan Pengujian

## Status pengujian

Setiap fitur harus melewati tiga status sebelum merge:
1. **Lolos build** — `./gradlew build` tanpa error
2. **Lolos unit test** — `./gradlew test` tanpa failure
3. **Diuji di Minecraft** — user konfirmasi lewat pengujian manual

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

## Tools bantu

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
