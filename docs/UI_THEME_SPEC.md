# UI_THEME_SPEC.md — HUD & GUI Avatar

Revisi: 2026-11-08, tambahan GUI v2. Status: arah visual disetujui pengguna;
implementasi, mockup, aset final dan runtime **belum dikerjakan dalam revisi dokumentasi ini**.

## 1. Keputusan utama

GUI utama memakai **gulungan perkamen bertema tribe dengan navigasi modern**.
Essential adalah referensi navigasi/pengaturan; RPG-HUD referensi modularitas HUD.
Keduanya bukan dependency wajib dan bukan sumber aset/kode untuk disalin otomatis.
Dokumen ini menjadi acuan UI aktif; tidak menggantikan kontrak gameplay atau status server.

## 2. Pemisahan tampilan

| Permukaan | Arah desain |
|---|---|
| Menu mod/settings | Gulungan terbuka, perkamen terang, tinta gelap, ujung kayu/pengikat; aksen tribe |
| HUD combat | Bingkai gulungan ringkas; tengah layar lapang; tidak menampilkan lembar besar saat bertarung |
| Profil | Lambang tribe, elemen dasar/aktif, mastery, profesi, teknik dan latihan |
| Skill tree | Diagram teknik di perkamen; teknik terkunci dengan segel dan alasan unlock |
| Konstruksi/utilitas | Material, volume dan biaya kontekstual, preview valid/tidak valid dengan alasan |
| Inventory vanilla | Bukan scope tahap UI awal; tidak mengubah layout/container/interaksi item |

## 3. Tema dan identitas

Tema AUTO mengikuti tribe/latar karakter. Elemen aktif menentukan aksen skill, bukan mengubah tribe pemain.
Pemain boleh memilih tema manual atau tampilan minimalis; tema tidak mengubah elemen/unlock.

| Tema | Aksen kandidat | Motif |
|---|---|---|
| Fire Nation | Merah tua dan emas | Api/cap |
| Water Tribe | Biru dan putih | Ombak |
| Earth Kingdom | Hijau dan warna tanah | Segel geometris/batu |
| Air Nomad | Jingga dan kuning hangat | Pusaran |
| Nonbender | Netral | Peralatan/senjata |

Palet ini rancangan artistik, bukan klaim motif resmi yang harus disalin dari film.
Avatar berlatar Water tetap berbingkai Water saat memakai Fire; indikator jurus menunjukkan Fire.
Identitas belum tersinkron memakai tema netral, bukan mengarang tribe dari item yang dipegang.

## 4. Navigasi dan kontrol

Kategori memakai tab/penanda halaman di sisi gulungan; pencarian dan panel isi konsisten antar tema.
Sediakan toggle, slider, dropdown, tooltip, tombol reset per kategori, serta indikator perubahan belum disimpan.
Terapkan/Batal jelas; preview HUD tidak menyimpan perubahan sampai diterapkan. Perubahan yang belum didukung
runtime ditandai disabled/direncanakan, bukan tombol aktif palsu.

| Kategori | Isi |
|---|---|
| HUD & Tema | AUTO/manual/minimal, skala, posisi, visibilitas widget, preview |
| Kontrol | Rebind dan penjelasan tekan/tahan/toggle; konflik input terlihat |
| Visual & Animasi | Partikel, trail, intensitas flash, camera shake, first person, reduced motion |
| Audio | Bending, senjata, impact dan ambience; hanya kanal yang sudah didukung |
| Gameplay Server | Aturan server terbaca; perubahan hanya melalui izin server yang sah |

Tombol buka menu harus rebindable; default ditetapkan setelah audit konflik. Jangan mengganti kontrol combat.
Saat screen terbuka, input tidak boleh bocor menjadi cast, serangan, scroll hotbar atau perubahan elemen.
Tutup screen tidak meninggalkan hold/charge macet; kebijakan cancel mengikuti kontrak kemampuan server.

## 5. Informasi HUD

| Kelompok | Widget |
|---|---|
| Inti | Health (bila mode pengganti dipilih), chi, elemen aktif, slot skill |
| Kontekstual | Stamina saat dipakai, charge, cooldown, water/lava reserve, material dan konstruksi aktif |
| Menu | Profil tribe, mastery, job, skill tree, latihan dan detail aturan |

Tidak ada angka dummy sebagai data live. Widget fitur yang belum tersedia disembunyikan atau diberi label pada mockup.
Health/stamina/chi harus dibedakan ikon dan teks, bukan warna saja. Jangan tampilkan dua health/hunger bar
bila mode pengganti dipakai. Mode overlay tambahan menjadi pilihan integrasi awal yang lebih terbatas.
RPG-HUD/Essential terpasang tidak membuktikan kompatibilitas; uji overlap dan render ordering sebelum menyatakan dukungan.

## 6. Implementasi dan data

Satu sistem widget/layout dengan theme tokens: palet, background, frame, ikon, focus, disabled, hover, spacing.
Tidak membuat lima screen dengan logika terpisah. Perkamen dibuat modular (misalnya 9-slice) agar skalabel;
teks, widget dan tooltip dirender terpisah dari gambar latar dan mendukung lokalisasi.

Client menyimpan preferensi tema/posisi/skala/audio/efek. Server menjadi authority chi, cooldown,
elemen, tribe yang dikonfigurasi, mastery, profesi, material, unlock dan aturan dunia.
Screen membaca snapshot state yang sama dengan HUD; jangan membuat tabel skill/biaya kedua.
Editor aturan server hanya untuk permission sah dan validasi ulang server; UI client tidak mengubah balance lokal.

Menu tidak mewajibkan koneksi akun/internet atau fitur sosial Essential. Aset GUI/fonts/icons dibuat sendiri
atau memakai aset berizin jelas; simpan provenance. Mod Menu integration opsional setelah audit versi, bukan dependency baru otomatis.

## 7. Aksesibilitas dan animasi

Teks tinta gelap di perkamen terang; motif tidak menutupi area baca. Kontras fokus/disabled/hover tetap terbaca.
Navigasi keyboard, tooltip yang dapat diakses, clipping/scroll benar dan teks panjang tidak terpotong.
Pengaturan ukuran teks/GUI scale, pengurangan flash, camera shake dan reduced motion tersedia sesuai dukungan.
Animasi membuka gulungan singkat dan opsional; tidak mengunci kontrol atau menunda akses tombol.
HUD memperhitungkan chat, subtitle, bossbar, debug, hotbar, status effect dan mount UI.

## 8. Urutan pengerjaan

1. Setelah checkpoint A–D: audit HUD aktual dan kontrak data; wireframe menu gulungan + HUD minimal.
2. Buat komponen netral dan satu tema, preview layout, config versioning, reset/apply/cancel.
3. Tambah token tema tribe lain dan AUTO/manual; satu layar pengaturan yang berfungsi.
4. Hubungkan profil/skill tree/material hanya ketika data runtime-nya tersedia.
5. Uji resolusi kecil/besar, GUI scale, keyboard, bahasa panjang, SP/MP, kompatibilitas HUD.

Status desain bukan gate build/runtime. Tidak perlu menunggu seluruh profesi selesai untuk membuat tema dasar.

## 9. Referensi yang diperiksa

- RPG-HUD 3.13 Fabric 1.21.1: struktur komponen HUD, tipe tampilan, settings/warna dari isi JAR.
  Metadata mencantumkan GPL-3.0. Belum diuji runtime dalam audit referensi ini.
- Essential unggahan 1.21.1: container dan JAR internal GUI, palette, komponen, font/settings.
  Tidak menganggap nomor container sebagai versi fitur GUI; belum diaudit visual runtime.
- Konsep gulungan bertema tribe: arahan pengguna; aset original proyek.
