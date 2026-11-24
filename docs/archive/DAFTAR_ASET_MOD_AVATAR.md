# Daftar Aset Mod Avatar

Tanggal: 8 November 2026
Target: Minecraft Java 1.21.1, Fabric
Status: daftar kebutuhan produksi. Belum menyatakan aset selesai atau sudah diuji dalam game.
Acuan tampilan: [UI_THEME_SPEC.md](UI_THEME_SPEC.md) dan [mockup Water Tribe UI yang disetujui](../art-source/ui/concepts/Water%20Tribe%20UI%20Overlook.png).

## 1. Keputusan arah pengerjaan

Buat kumpulan bahan efek yang bisa digunakan oleh beberapa jurus. Contohnya, tekstur aliran air dan bentuk air melengkung dapat dipakai untuk Water Whip, Water Arms, dan Octopus Form. Setiap jurus tetap punya bentuk, gerakan, dan timing sendiri.

Efek visual atau VFX adalah seluruh tampilan efek di game. Partikel adalah salah satu cara menyusun VFX: gambar kecil atau serpihan yang muncul, bergerak, lalu hilang. Aura menjelaskan efek yang mengelilingi tubuh atau objek; aura dapat tersusun dari partikel, bentuk tiga dimensi, atau gabungan keduanya.

Gambar saja belum membuat jurus berfungsi. Kode mod mengatur posisi, bentuk, pergerakan, waktu muncul, dan penghapusannya. Damage, biaya chi, material dan perubahan dunia tetap ditentukan server.

## 2. Kelompok aset utama

| Kelompok | Yang harus dibuat | Bentuk berkas atau hasil |
|---|---|---|
| Ikon | Jurus, elemen, status, profesi, latihan, tingkatan | PNG latar transparan |
| Partikel | Percikan api, asap, angin, tetesan, cipratan, debu, serpihan batu/es | PNG tunggal atau beberapa gambar berurutan |
| Permukaan efek | Aliran air, busa, lidah api, garis angin, retakan es, kerak lava | PNG yang dapat diulang tanpa sambungan terlihat |
| Bentuk jurus | Bola, cincin, kerucut, kubah, pusaran, gelombang, tentakel | Bentuk tiga dimensi dari kode atau model yang didukung renderer |
| Jejak gerakan | Jejak tongkat, sapuan tangan, cambuk, lintasan proyektil | Tekstur memanjang + bentuk mengikuti gerakan |
| Benturan dan ledakan | Kilatan, gelombang kejut, cipratan, debu, pecahan, sisa asap | Gabungan gambar, partikel, bentuk dan gerakan |
| Aura | Efek awal, efek berulang, reaksi terkena pukulan, efek menghilang | Gabungan bahan efek + aturan pemicu |
| Gerakan pemain | Bersiap, mengambil ancang-ancang, menyerang, pulih, batal | Studi gerak dan hasil ekspor sesuai sistem animasi yang dipakai |
| Model benda | Senjata, wadah air/lava, pakaian/armor, konstruksi | Model sumber, tekstur, hasil ekspor yang sesuai |
| Antarmuka | Perkamen, kayu, tombol, tab, bingkai, bar, lambang | Potongan gambar yang dapat disusun ulang |
| Suara | Awal jurus, pengisian tenaga, serangan, benturan, pembatalan, menu | WAV sumber dan OGG untuk game |
| Interaksi dunia | Penanda sumber, pratinjau konstruksi, retakan, indikator material | Gambar/model seperlunya + penanda yang digambar kode |

## 3. Kebutuhan efek per elemen

| Elemen | Bahan dasar | Efek jurus yang dibentuk | Ciri visual |
|---|---|---|---|
| Api | Lidah api, bara, asap, cahaya inti, tepi menyala | Jab, sapuan, pelindung, semburan, bola api, ledakan | Lincah, pecah di tepi, pusat terang |
| Udara | Garis angin, pusaran kecil, cincin tekanan, kabut tipis | Serangan tongkat, Air Palm/Blast, Vortex, Scooter, Spout | Ringan, transparan, arah gerakan jelas |
| Air | Aliran, tetesan, cipratan, busa, riak | Whip, jet, gelombang, lengan air, Octopus | Menyambung, lentur, mengalir dan menipis ke ujung |
| Tanah | Debu, serpihan, retakan, permukaan batu/tanah sumber | Boulder, Wall, pilar, armor, gelombang tanah | Berat, berbidang, debu muncul di titik gerak/bentur |
| Petir | Cabang kilat, inti putih, percikan listrik | Pengisian, sambaran, pengalihan petir | Cepat dan tajam; kilatan dapat dikurangi |
| Es | Permukaan es, retakan, embun dingin, pecahan | Tombak, perisai, penjara, jalur es | Lebih kaku daripada air, pecah menjadi serpihan |
| Lava | Aliran pijar, lapisan kerak, bara | Pengangkatan dan aliran lava | Terasa kental; mengikuti persediaan material nyata |
| Logam/tumbuhan | Kabel dan kilap; sulur dan daun | Cambuk/kabel logam; manipulasi tanaman | Material mudah dikenali, tidak sekadar ganti warna air |

Petir adalah cabang teknik, bukan elemen dasar kelima. Daftar ini tidak membuka teknik untuk pemain secara otomatis.

## 4. Paket efek untuk jurus yang menjadi prioritas

| Jurus | Aset yang dibutuhkan | Perilaku penting |
|---|---|---|
| Fire Jab | Ikon, gerak pukulan, semburan pendek di tangan, bara, benturan, suara | Api mengikuti pukulan; tidak wajib membentuk bola saat persiapan |
| Flame Sweep | Ikon, gerak sapuan, jejak api melengkung, bara, suara | Lengkungan menunjukkan arah dan luas serangan |
| Fire Guard | Ikon, gerak bertahan, efek pelindung, reaksi benturan, suara berulang | Awal → bertahan → padam; sesuai state kemampuan |
| Fire Jet | Ikon, gerak dash, semburan pendorong, jejak pendek, suara | Tetap dash; bukan proyektil bola api |
| Fire Blast | Ikon, gerak mengisi/melepas, bola api, partikel pengisian, proyektil, benturan/ledakan, pembatalan | Membesar sesuai aturan charge; batal tidak meledak atau melukai |
| Air Staff Attack | Ikon, gerak tusuk/putar/sapu, jejak angin pada tongkat, suara ayunan/benturan | Titik jejak melekat pada tongkat dan tidak tertinggal saat teleport |
| Air Vortex | Ikon, gerak jurus, pusaran, garis angin, debu, suara | Efek berulang selama aktif dan berhenti bersih |
| Water Whip | Ikon, gerak cambuk, bentuk air melengkung, aliran, tetesan, cipratan, suara | Air tampak menyambung; benturan sesuai hasil server |
| Earth Boulder | Ikon, gerak mengangkat/melempar, batu, debu awal, pecahan benturan, suara | Bentuk visual tidak mengubah aturan kerusakan blok tanpa implementasi gameplay |

Air Palm dan Air Blast dapat memakai bahan angin yang sama, tetapi status handler terbaru harus diperiksa sebelum dianggap jurus yang sudah berfungsi.

## 5. Aura: pisahkan berdasarkan tujuan

| Jenis | Contoh | Kapan muncul |
|---|---|---|
| Pengisian tenaga | Api berkumpul di tangan | Saat teknik benar-benar sedang charge |
| Kemampuan aktif | Pelindung api, aliran penyembuhan, kendaraan angin | Selama kemampuan aktif menurut server |
| Status | Terbakar, basah, dingin | Selama status masih berlaku |
| Kosmetik | Bara ringan atau garis angin untuk mastery | Jika sudah terbuka dan pemain mengaktifkannya; tanpa damage |
| Keadaan khusus | Avatar State | Jika sistem tersebut sudah diimplementasikan dan aktif |

Aura tidak harus selalu menyala. Tingkatan lebih tinggi tidak harus berarti layar dipenuhi partikel. Buat tampilan awal, tampilan berulang, dan tampilan berakhir. Efek berulang tidak boleh memaksa kemampuan berhenti karena durasi gambar habis.

## 6. Octopus Form dan manipulasi dunia

Octopus memakai tubuh tentakel air melengkung, meruncing ke ujung, dengan permukaan yang terlihat mengalir. Partikel tetesan/cipratan hanya pelengkap. Menggambar satu PNG gurita tidak cukup untuk membuat jurus yang bergerak mengitari pemain.

Urutan pembuktian: satu tentakel → dua tentakel → jumlah sesuai desain gameplay. Periksa kelengkungan, sambungan ke tubuh, arah serang, tampilan dari dekat/jauh, dan efek transparan yang saling menumpuk.

Earth Wall memerlukan tampilan pengangkatan dari sumber, kondisi wall, tendangan, wall terbang, benturan, lalu hasil akhirnya. Sumber, volume, blok yang hilang atau menetap, dan reklamasi mengikuti transaksi material server. Retakan visual tidak boleh diam-diam menghapus blok. Keputusan pemulihan dunia tidak ditetapkan oleh dokumen aset.

Utilitas juga membutuhkan umpan balik: percikan untuk menyalakan api, panas saat memasak, aliran saat mengisi wadah, debu saat menggemburkan, dan penanda saat mengambil material. Pemicu dan dampaknya mengikuti kemampuan yang sah.

## 7. Potongan GUI gulungan yang harus dibuat

| Bagian | Daftar gambar |
|---|---|
| Gulungan utama | Kertas tengah yang bisa diperluas, tepi, sudut, kayu penggulung, tali/pengikat |
| Hiasan tema | Kain/pita, lambang, motif pinggir; Water dibuat dulu sebagai contoh |
| Tombol | Normal, disorot, ditekan, fokus keyboard, tidak tersedia |
| Pengaturan | Kotak centang, sakelar, batang penggeser, pegangan, tab, panah, pencarian |
| HUD ringkas | Bingkai chi, isi bar, bingkai slot, segel elemen, indikator charge/cooldown |
| Profil | Bingkai potret, segel tingkatan, lambang profesi dan latihan |
| Pohon jurus | Bingkai simpul, segel terkunci, penanda dipilih/tersedia, gaya garis penghubung |
| Konstruksi | Penanda valid/tidak valid, ikon bahan, bingkai informasi biaya |

Tema: Api merah-emas; Air (Water) biru-putih; Tanah hijau-cokelat; Udara jingga-kuning; Nonbender netral. Gunakan sistem komponen yang sama dan variasi hiasan/warna. Jangan membuat lima sistem menu terpisah.

Nama, angka, tooltip, pemain tiga dimensi, dan status tidak ditempel permanen ke gambar. Gambar referensi berisi beberapa contoh layar; semuanya tidak ditampilkan serentak saat bertarung.

## 8. Ukuran awal yang disarankan

| Aset | Ukuran usulan |
|---|---|
| Ikon jurus | 32 × 32 piksel |
| Partikel kecil | 16 × 16 atau 32 × 32 piksel |
| Jejak gerakan | 64 × 16 atau 128 × 32 piksel |
| Permukaan air/api/busa | 64 × 64 atau 128 × 128 piksel |
| Lambang tribe/tingkatan | 32 × 32 atau 64 × 64 piksel |
| Komponen GUI | Sesuai ukuran komponen dan skala GUI; jangan satu gambar layar penuh |

Ini titik awal produksi, bukan batas engine. Untuk gambar efek yang membutuhkan transparansi, gunakan PNG RGBA tanpa latar putih atau pola kotak-kotak yang tertanam. Urutan gambar animasi, titik pusat dan ukuran bingkai harus konsisten. Bentuk efek bisa halus meskipun dunia Minecraft berbentuk blok.

## 9. Urutan produksi dan pembagian pekerjaan

| Tahap | Hasil |
|---|---|
| 0. Periksa yang sudah ada | Catat asset lama: pakai, perbaiki atau ganti. Verifikasi lisensi dan kualitas |
| 1. Fire Jab lengkap | Ikon + gerak + api + benturan + suara, terlihat benar dalam game |
| 2. Fire Blast | Pengisian + pelepasan + proyektil + benturan + pembatalan |
| 3. Elemen lain | Satu paket angin, air, tanah; buktikan Staff/Vortex, Whip dan Boulder |
| 4. GUI dasar | Komponen gulungan Water dan HUD ringkas, lalu variasi tribe |
| 5. Teknik lanjutan | Octopus, Earth Wall berbasis material, aura mastery, konstruksi/profesi |

Gambar ikon, partikel, tekstur, komponen GUI, konsep dan suara dapat disiapkan sambil agent mengerjakan kode. Ekspor animasi final menunggu template rig yang benar-benar didukung. Pembuatan asset tidak mengganti urutan checkpoint tim atau membuat pipeline gameplay kedua.

Setiap paket jurus diperiksa dari pandangan orang pertama, orang ketiga dan pemain lain. Uji selesai, batal, kena gangguan, cast ulang, mati dan pindah dunia. Efek dan suara tidak boleh tertinggal. Sediakan pengurangan partikel/kilatan tanpa menghilangkan tanda serangan penting.

## 10. Hasil penelitian resource

| Resource | Relevansi | Keputusan untuk mod |
|---|---|---|
| ResourcePack AI | Pembuat konsep/aset dan referensi efek dengan awal, pengulangan, akhir | Periksa hasil ekspor dan hak pakai. VFX siap jalannya membutuhkan RP Engine dan Minecraft 1.21.4+, bukan langsung untuk Fabric 1.21.1 |
| MythicCraft | Contoh pemisahan skill, model, kosmetik, HUD dan profesi | Referensi desain dan pengemasan. Plugin mereka tidak otomatis menjadi dependency Fabric |
| Fabric 1.21.1 | Panduan partikel, layar dan suara custom | Acuan teknis integrasi yang sesuai target |
| Blockbench | Pembuatan model dan studi animasi; format ekspor punya kemampuan berbeda | Sesuaikan format dengan renderer/animasi yang benar, bukan hanya ekstensi .bbmodel |
| Player Animation Library | Sistem pemutaran dan pengendalian gerakan pemain | Ikuti versi dan template yang dipakai repo; tidak mengganti dependency dari contoh dokumentasi terbaru |

Jangan membeli plugin atau mengganti versi Minecraft hanya karena demo efeknya menarik. PNG/model yang bisa diekspor belum membuktikan perilaku efek atau animasinya tersedia di mod. Hak mengunduh atau memakai aset tidak otomatis mencakup hak membagikannya dalam berkas mod.

## 11. Sumber

Diperiksa 8 November 2026. Pembagian kategori, ukuran dan urutan produksi di atas merupakan rekomendasi untuk proyek ini.

- https://resourcepack.ai/docs/vfx
- https://resourcepack.ai/docs/exporting
- https://mythiccraft.io/
- https://docs.fabricmc.net/1.21.1/develop/rendering/particles/creating-particles
- https://docs.fabricmc.net/1.21.1/develop/rendering/gui/custom-screens
- https://docs.fabricmc.net/1.21.1/develop/sounds/custom
- https://blockbench.net/wiki/blockbench/formats/
- https://docs.zigythebird.com/pal/intro/

Rincian pemetaan 62 entri skill/modifier tersedia pada ASSET_PRODUCTION_SPEC.md. Dokumen ini menjadi daftar produksi yang lebih mudah dibaca; kedua dokumen tidak mengklaim seluruh jurus tersebut telah diimplementasikan.
