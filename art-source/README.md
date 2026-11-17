# Art Source

Sumber produksi dan bukti visual untuk Avatar: Elements (Minecraft Java 1.21.1, Fabric).
Isi folder ini bukan otomatis bagian dari mod runtime. Integrasi hanya dilakukan setelah
format, lisensi/provenance, dan referensi pemakaiannya diperiksa.

## Struktur

| Folder/file | Isi |
|---|---|
| `asset_pack/` | Aset master proyek Avatar Elements (animasi PAL, tekstur, sounds, models) |
| `asset_pack_t2_vfx/` | Aset master T2 volumetric VFX |
| `models/air_staff/` | Sumber Blockbench, ekspor model, tekstur, preview, dan handoff Air Staff |
| `animation_studies/` | Studi rig dan gerak Fire Jab serta staff thrust |
| `audio/` | Kandidat dan prototype SFX beserta manifest |
| `vfx/` | Prototype tekstur, model 3D, dan spesifikasi VFX |
| `ui/concepts/` | Mockup dan konsep antarmuka |
| `tools/` | Generator, verifikasi, dan pengujian editor/aset |
| `archive/` | Arsip review & paket ZIP sumber aset master |

## Aturan integrasi

- Pertahankan `mod/src/main/resources/` dan `mod/src/client/resources/` sebagai jalur runtime kanonis.
- Jangan menyalin model, texture, animasi, suara, atau mockup ke resource aktif tanpa memeriksa ID,
  format Minecraft 1.21.1, referensi kode, dan status review.
- Pertahankan versi sumber dan bukti review; jangan menimpa atau menghapus berkas asal.
- Generator dan review script yang dipindahkan dalam penataan ini menggunakan path relatif
  terhadap file script. Script lama di `animation_studies/` belum dipindah karena beberapa
  masih memakai path absolut; normalisasi path harus dilakukan sebelum folder itu direstrukturisasi.
