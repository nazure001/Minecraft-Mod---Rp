# AGENTS.md — Aturan Kerja Kolaborasi Multi-Agent

## Pihak yang terlibat

| Pihak | Peran |
|---|---|
| **ChatGPT** | Arsitektur, spesifikasi skill/armor/senjata, audit, review perubahan, analisis bug |
| **Claude Code** | Implementasi kode, migrasi datapack, integrasi aset, build, pengujian otomatis |
| **Antigravity IDE + agent** | Implementasi produksi (izin `mod/` aktif), debugging, tugas terpisah, pengujian integrasi |
| **User** | Menguji rasa kontrol, gerakan, visual, suara, menentukan hasil sesuai referensi |

## Aturan umum

1. **Satu editor per file pada satu waktu (Exclusive File Ownership).** Setiap agent hanya memodifikasi file yang dialokasikan secara eksplisit dalam dispatch/task.
2. **Setiap tugas punya branch / worktree sendiri.** Format: `feature/<nama>`, `fix/<nama>`, `content/<nama>`.
3. **Jangan push langsung ke `main`.** Semua perubahan lewat PR dan harus disetujui setelah review.
4. **Jangan menjalankan script deploy, mengubah instance Minecraft, menghapus file asal, atau menimpa konfigurasi lama** tanpa konfirmasi eksplisit dari user.
5. **Jangan menimpa world pengguna atau menjalankan server otomatis secara invasif.** Siapkan prosedur uji langkah-demi-langkah bagi pengguna.
6. **Jangan commit file besar** (>10 MB) tanpa Git LFS. File referensi (JAR, addon) ada di `reference/` dan di-ignore.
7. **Kontrak gameplay** ada di `docs/CONTENT_SPEC.md`. Untuk skill yang sudah aktif, nilai runtime berasal dari `mod/src/main/resources/data/avatar_elements/skill_definitions.json` (dengan override opsional di `config/avatar_elements/skill_definitions.json`); schema yang benar-benar dibaca ditentukan oleh `SkillConfigLoader`. Katalog desain yang belum aktif di `CONTENT_SPEC.md` bukan konfigurasi runtime. Jangan hardcode nilai skill tanpa merekonsiliasikannya dengan kontrak dan data runtime.

## Batas perubahan per agent

> **Catatan Scope Produksi (2026-11-08):**
> Larangan lama yang membatasi pengubahan file di `mod/` bagi Antigravity / subagent telah **DICABUT** untuk scope implementasi produksi ini per instruksi pengguna (*"dengan pencabutan larangan lama mengubah mod/ untuk scope ini"*). Koordinasi kerja antar-agent dilakukan via alokasi kepemilikan file eksklusif (*exclusive file ownership*).

### Claude Code boleh
- Edit file di `mod/`, `legacy/` (patch), `docs/` yang dialokasikan untuk tugasnya
- Buat file baru di struktur yang sudah ada
- Jalankan `./gradlew build`, `./gradlew test`
- Inisialisasi dan commit ke branch aktif

### Claude Code jangan
- Menghapus folder `legacy/` atau `reference/`
- Push ke `main` atau merge PR tanpa proses review
- Menjalankan server Minecraft otomatis atau memodifikasi world data pengguna
- Mengubah file yang dialokasikan untuk agent lain

### Antigravity IDE + agent boleh
- Baca semua file di workspace/repo
- Edit file di `mod/`, `docs/`, dan aset resource sesuai alokasi kepemilikan file tugas aktif (larangan lama pada `mod/` telah dicabut)
- Buat file baru di struktur yang sudah ada
- Jalankan build dan test lokal (`./gradlew build`, `./gradlew test`)
- Debug dan jalankan dev environment lokal

### Antigravity IDE + agent jangan
- Mengedit file yang sedang dialokasikan/dikerjakan agent lain (cek `TASKS.md` dan alokasi dispatch)
- Push ke `main` atau merge PR tanpa review
- Menjalankan server otomatis atau menimpa world pengguna

## Alur tugas

```
spesifikasi (ChatGPT)
  → tugas di TASKS.md
  → branch baru
  → implementasi (Claude Code / Antigravity)
  → build + unit test
  → review kode
  → uji di Minecraft (user)
  → perbaikan jika ada
  → merge ke main
```

## Status tugas

Gunakan tiga status yang berbeda di `TASKS.md`:
- `[ ]` Belum dimulai
- `[~]` Sedang dikerjakan — cantumkan nama agent dan branch
- `[x]` Selesai — cantumkan tanggal dan hasil pengujian

## Perintah build

```bash
# Build mod
cd mod && ./gradlew build

# Run test
cd mod && ./gradlew test

# Run dev client (Fabric)
cd mod && ./gradlew runClient

# Run dev server
cd mod && ./gradlew runServer
```

## Pemeriksaan wajib sebelum PR

- [ ] `./gradlew build` lulus tanpa error
- [ ] `./gradlew test` lulus
- [ ] Verifikasi test Python di `tests/` secara terpisah; task Gradle bukan pengganti suite tersebut
- [ ] Validasi schema JSON yang diubah terhadap loader/konsumen aktual
- [ ] Tidak ada file world/save yang ter-commit
- [ ] `TASKS.md` diperbarui
- [ ] Perubahan besar dicatat di `docs/DECISIONS.md`
