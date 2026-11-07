# AGENTS.md — Aturan Kerja Kolaborasi Multi-Agent

## Pihak yang terlibat

| Pihak | Peran |
|---|---|
| **ChatGPT** | Arsitektur, spesifikasi skill/armor/senjata, audit, review perubahan, analisis bug |
| **Claude Code** | Implementasi kode, migrasi datapack, integrasi aset, build, pengujian otomatis |
| **Antigravity IDE + agent** | Menjalankan proyek, debugging, tugas terpisah, pengujian integrasi |
| **User** | Menguji rasa kontrol, gerakan, visual, suara, menentukan hasil sesuai referensi |

## Aturan umum

1. **Satu editor per file pada satu waktu.** Jika dua agent perlu mengubah area yang sama, koordinasikan lewat issue/task sebelum mulai.
2. **Setiap tugas punya branch sendiri.** Format: `feature/<nama>`, `fix/<nama>`, `content/<nama>`.
3. **Jangan push langsung ke `main`.** Semua perubahan lewat PR dan harus disetujui.
4. **Jangan menjalankan script deploy, mengubah instance Minecraft, menghapus file asal, atau menimpa konfigurasi lama** tanpa konfirmasi eksplisit dari user.
5. **Jangan commit file besar** (>10 MB) tanpa Git LFS. File referensi (JAR, addon) ada di `reference/` dan di-ignore.
6. **Sumber kebenaran gameplay** ada di `docs/CONTENT_SPEC.md`. Jangan hardcode nilai skill, armor, atau weapon langsung di kode tanpa merujuk ke sana.

## Batas perubahan per agent

### Claude Code boleh
- Edit semua file di `mod/`, `legacy/` (patch), `docs/`
- Buat file baru di struktur yang sudah ada
- Jalankan `./gradlew build`, `./gradlew test`
- Inisialisasi dan commit ke branch aktif

### Claude Code jangan
- Menghapus folder `legacy/` atau `reference/`
- Push ke `main` atau merge PR
- Menjalankan server Minecraft atau modify world data
- Mengubah `AGENTS.md` ini tanpa konfirmasi user

### Antigravity IDE + agent boleh
- Baca semua file
- Edit file di branch-nya sendiri
- Jalankan build dan test lokal
- Debug dan jalankan dev server

### Antigravity IDE + agent jangan
- Edit file yang sedang dikerjakan Claude Code (cek `TASKS.md` kolom "Dikerjakan")
- Merge atau rebase branch tanpa konfirmasi

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
- [ ] Tidak ada file world/save yang ter-commit
- [ ] `TASKS.md` diperbarui
- [ ] Perubahan besar dicatat di `docs/DECISIONS.md`
