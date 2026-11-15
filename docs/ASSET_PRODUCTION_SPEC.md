# ASSET_PRODUCTION_SPEC — Avatar Elements

Tanggal: 2026-11-08. Target: Minecraft Java 1.21.1, Fabric. Status: usulan produksi aset setelah pengguna menyetujui arah seni UI. Dokumen ini adalah katalog kebutuhan, bukan laporan bahwa aset telah selesai atau sudah berjalan di dalam game.

## 1. Cakupan dan Sumber Keputusan

Berdasarkan `UI_THEME_SPEC.md` terlampir, [mockup Water Tribe UI yang telah disetujui](../art-source/ui/concepts/Water%20Tribe%20UI%20Overlook.png), `CONTENT_SPEC.md`, serta bagian koreksi di akhir `CHARGE_ORB_SPEC.md`. Katalog gameplay saat ini memiliki 62 entri skill/modifier; angka ini tidak berarti ke-62 skill tersebut sudah diimplementasikan. Status kode/build/runtime terbaru harus diambil dari repositori dan laporan integrasi tim. Jangan mengubah cast type, damage, cooldown, chi, atau unlock melalui dokumen aset ini.

Mockup merupakan papan panduan untuk berbagai layar. Jangan menampilkan halaman settings, profile, skill tree, dan construction secara bersamaan di atas HUD combat. Teks, angka, nilai slider, dan player preview adalah widget/data runtime, bukan dipotong dari gambar lalu ditanam permanen (baked) ke dalam PNG.

## 2. Riset Alat dan Tingkat Kesesuaian

| Sumber | Poin Berguna | Cara Penggunaan dalam Proyek | Batasan yang Terverifikasi |
|---|---|---|---|
| [ResourcePack AI Studio](https://resourcepack.ai/docs) | Membuat sampel tekstur, ikon, model; [VFX memiliki buildup/loop/fade](https://resourcepack.ai/docs/vfx); ekspor pack | Menguji konsep dan mengekspor bahan baku dengan hak pakai; periksa berkas asli sebelum integrasi | [VFX platform membutuhkan RP Engine](https://resourcepack.ai/docs/vfx), 1.21.4+; ZIP biasa tidak menjalankan VFX. Tidak kompatibel langsung dengan target 1.21.1 |
| [ResourcePack AI Exporting](https://resourcepack.ai/docs/exporting) | Membedakan Java pack, Bedrock, dan ekspor plugin | Hanya ambil aset yang sesuai untuk Java 1.21.1; periksa skema pack/model setelah ekspor | [Ekspor plugin bukan pack mandiri](https://resourcepack.ai/docs/exporting); animasi runtime tidak otomatis terbawa dalam Java ZIP biasa |
| [MythicCraft](https://mythiccraft.io/) / [ModelEngine](https://wiki.mythiccraft.io/modelengine/Modeling/Importing-a-Model) | Mengemas model, animasi, [skill](https://resourcepack.ai/docs/rp-engine/skills); menggabungkan mob, HUD, profesi | Mempelajari cara pengorganisasian paket dan lifecycle; gunakan aset hanya jika lisensi mengizinkan konversi/distribusi | [Alur kerja plugin/blueprint/resourcepack](https://wiki.mythiccraft.io/modelengine/Modeling/Importing-a-Model) bukan loader Fabric; `.bbmodel` tidak otomatis menjadi animasi pemain |
| [Dokumentasi Fabric 1.21.1](https://docs.fabricmc.net/1.21.1/develop/rendering/particles/creating-particles) | [Tipe partikel, client factory, JSON tekstur](https://docs.fabricmc.net/1.21.1/develop/rendering/particles/creating-particles); [custom screen](https://docs.fabricmc.net/1.21.1/develop/rendering/gui/custom-screens), [suara](https://docs.fabricmc.net/1.21.1/develop/sounds/custom) | Fondasi integrasi utama untuk mod | Nama mapping pada contoh dapat berbeda dengan Yarn proyek; harus dicocokkan dengan Gradle lokal |
| [Fabric API WorldRenderEvents 1.21.1](https://maven.fabricmc.net/docs/fabric-api-0.115.6+1.21.1/net/fabricmc/fabric/api/client/rendering/v1/WorldRenderEvents.html) | Titik ekstensi renderer dunia | Fondasi untuk mesh/ribbon berbasis attachment, tergantung render pass | Tidak menyediakan tube mesh, IK, transparency sorting, atau networking secara otomatis |

Rekomendasi: pertahankan Fabric sebagai runtime utama. Jangan menambahkan MythicMobs, ModelEngine, atau RP Engine sebagai dependency untuk menjalankan mod saat ini. Pisahkan bahan mentah artistik dari engine yang menggunakan bahan tersebut. Jangan mewajibkan instalasi shaderpack untuk efek inti; glow fullbright tidak sama dengan bloom atau pencahayaan dinamis.

Status jalur animasi: Fire Jab memiliki studi rig `.bbmodel` dan clip PAL JSON terpisah. Model Blockbench tidak dimuat otomatis sebagai animasi pemain; ekspor harus disesuaikan ke tulang player PAL yang benar dan diverifikasi in-game. VFX Blockbench juga memerlukan jalur ekspor serta renderer Fabric yang nyata; `.bbmodel` saja bukan VFX runtime.

## 3. Katalog Aset yang Harus Dikelola

Ukuran di bawah ini adalah usulan titik awal, bukan batasan kaku dari Minecraft. Ukuran tampilan dihitung berdasarkan GUI scale/render scale, bukan sama dengan resolusi gambar.

| Kelompok | Aset yang Dibutuhkan | Format/Resolusi Usulan | Kebutuhan Integrasi | Prioritas |
|---|---|---|---|---|
| Ikon skill | Satu siluet jelas untuk setiap entri skill; slot kosong, locked, unavailable dipakai bersama | PNG RGBA 32×32; sumber 128×128 bila perlu | HUD/skill tree, cooldown dan state digambar melalui kode | P0/P1 lalu P2 |
| Ikon status | Burn, wet, chilled, stagger, guard, charge, source missing; hanya aktif saat state ada | PNG 16/32×32 | State server, tooltip yang dapat diterjemahkan | P1 |
| Micro-particle | Ember, flame tongue, smoke puff, gust curl, droplet, splash, foam, dust, stone chip, frost, spark | PNG RGBA 16/32×32; frame terpisah saat memakai sprite provider | [Registrasi partikel, daftar tekstur JSON, factory](https://docs.fabricmc.net/1.21.1/develop/rendering/particles/creating-particles), lifetime, batas spawn | P0/P1 |
| Flipbook | Flame burst, impact flash, small splash, smoke expansion, crackle | Usulan 4–8 frame/urutan, pivot seragam | Pemilihan frame berdasarkan usia (age); jangan mengasumsikan semua sheet memakai `.mcmeta` | P0/P1 |
| Ribbon/trail | Soft streak, hard crescent, flowing water stripe, flame edge, cable highlight | PNG 64×16 atau 128×32, UV searah jalur gerak | Mesh ribbon, sampling tip/base, fade riwayat gerak, dan reset saat teleport | P0/P1 |
| Mesh VFX | Ring, arc, cone, sphere shell, dome, tube, funnel, wave sheet | Mesh prosedural di kode atau format eksportir yang benar-benar didukung | [Renderer](https://maven.fabricmc.net/docs/fabric-api-0.115.6+1.21.1/net/fabricmc/fabric/api/client/rendering/v1/WorldRenderEvents.html), UV, culling, blend/depth; bukan PNG yang otomatis membentuk 3D | P0/P1/P2 |
| Material VFX | Fire turbulence, water flow/foam, air streak, dust, lava crust, ice cracks | PNG 64/128×128 tileable; mask grayscale jika diwarnai saat runtime | UV scroll, state material, alpha; custom shader hanya setelah PoC | P0/P1/P2 |
| Charge | Core/shell/noise, orbit particles, aksen release/cancel | Gunakan kembali kit sphere/ring dan tekstur | Attachment tangan, sinkronisasi phase + cast serial, sudut pandang 1st/3rd person | P0 Fire Blast |
| Impact/explosion | Hit flash, radial shockwave, ember/splash/debris, sisa asap | Gunakan primitif bersama + profil per elemen | Impact yang dikonfirmasi server; VFX tidak menghancurkan blok sendiri | P0/P1 |
| Aura | Loop jarang, aktivasi, deaktivasi, hit pulse | Material/partikel pakai ulang; preset berbasis data | State dan visibilitas/LOD; tier kosmetik opsional | P1/P2 |
| Model senjata/gear | Staff Candidate 2, senjata yang sudah memiliki kontrak, wadah air/lava, armor per tier | Sumber `.bbmodel`, PNG; eksportir/runtime yang sesuai | Transformasi item, posisi genggaman tangan, skin/lengan, registri model | Audit dulu |
| Animasi | Player cast, ready, overlay lokomosi, kombo senjata, cancel | Studi `.bbmodel` + ekspor sesuai template PAL yang terbukti | Rig nyata, blend, sinkronisasi fase, interupsi; jangan ekspor buta | P0/P1 |
| SFX | Charge start/loop, release, hit, sustain stop, cancel, UI | Sumber WAV; runtime OGG, mono untuk SFX spasial | [`sounds.json`, event, subtitle](https://docs.fabricmc.net/1.21.1/develop/sounds/custom), penghentian loop dan atenuasi | P0/P1 |
| HUD | Bingkai gulungan kecil, slot skill, bar track/fill, segel elemen | PNG modular 9-slice bila sesuai | Render widget + nilai server, geser/skala bila didukung | P1 |
| GUI | Perkamen, penggulung kayu, pembatas, state button/toggle/slider/dropdown/tab | PNG tileable/9-slice; ikon terpisah, teks runtime | [Layar custom](https://docs.fabricmc.net/1.21.1/develop/rendering/gui/custom-screens), fokus/navigasi/input capture | P1 setelah A–D |
| Progression | Lambang tribe, 7 segel tier, lencana profesi/latihan, simpul skill | PNG 32/64×64, garis tetap terbaca pada ukuran kecil | Unlock berbasis data, label terlokalisasi | P2 |
| Manipulasi dunia | Sorotan sumber, pratinjau valid/invalid, indikator material, tahap kerusakan konstruksi | Outline/mesh kode, mask retakan, tekstur blok sumber | Ledger + izin dunia + state konstruksi | P2 |
| Umpan balik QoL | Percikan api, panas memasak, aliran pengisian, debu bajak tanah, penanda ekstraksi bijih | Gunakan kembali kit partikel/kurva | Aksi server nyata; jangan mengubah kosmetik menjadi damage | P2 |
| Pemasaran/referensi | Concept sheet, storyboard, seni promo, tangkapan layar | PNG ukuran besar, tidak dipakai menggantikan aset runtime | Hanya untuk persetujuan dan panduan arah seni | Sesuai kebutuhan |

## 4. Bahasa Visual per Elemen

| Elemen | Bentuk/Gerakan | Kit Inti | Aura yang Sesuai |
|---|---|---|---|
| Fire (Api) | Lidah api menyobek, memuai-menyusut, inti terang, bara terpental terarah | Flame strip, burst, ember, smoke, heat ring | Heat haze opsional, bara jarang; tidak membakar seluruh tubuh secara default |
| Air (Udara) | Jernih dan ringan, garis lengkung berpilin, tekanan terbaca lewat cincin/jejak | Gust curl, soft ribbon, pressure ring, funnel | Beberapa jejak angin berputar; pertahankan siluet pemain |
| Water (Air) | Menyambung, meruncing, mengalir terarah; busa pada titik benturan | Flow tube/ribbon, droplet, splash, foam, ripple | Pita air kecil + tetesan; bukan bola padat yang menutupi tubuh |
| Earth (Tanah) | Bermassa berat, bersudut tegas, akselerasi berat, debu saat menghantam tanah | Tekstur blok sumber, bongkahan batu, dust, crack | Debu atau serpihan batu sangat jarang sesuai teknik |
| Lightning (Sub-bending Api) | Cabang patahan cepat, inti putih dan tepi biru dingin | Bolt mesh/ribbon, spark, kilatan singkat | Hanya saat kemampuan/state benar-benar aktif; opsi reduced-flash |
| Ice / Lava / Metal / Plant | Cabang variasi dengan material tersendiri | Pecahan/retakan es, kerak lava, kabel baja, sulur/daun | Sesuai teknik; tidak menambah tribe baru |

Jangan memaksakan setiap skill menjadi bola (orb) atau ledakan. Blue Fire sebaiknya berupa modifier material yang terkendali. Tier tinggi meningkatkan kehalusan detail dan keterbacaan identitas; jangan sekadar melipatgandakan jumlah partikel di setiap tier. Keempat elemen utama mempertahankan keterbacaan tempur (combat readability) yang setara.

## 5. Paket Lengkap untuk Satu Skill

Setiap skill menggunakan komponen yang diperlukan dari tabel berikut; tidak wajib memiliki seluruh efek sekaligus.

| Komponen | Isi Serah Terima |
|---|---|
| Identity | `skillId`, ikon, palet/motif, material sumber bila ada |
| Anticipation / WINDUP | Pose, penanda arah/titik kumpul, suara awal; tidak menghasilkan hit lebih awal |
| Sustain / charge | Loop mulus tanpa jeda saat menyambung, attachment, ukuran sesuai state yang disetujui |
| Active / release | Animasi pukulan/pelepasan, bentuk efek selaras dengan arah serangan |
| Hit / miss | Impact mengikuti hasil server; serangan meleset tidak memutar penanda konfirmasi kena |
| Recovery / finish | Jejak memudar (trail fade) dan pose kembali ke lokomosi |
| Cancel / interrupt | Dissolve/penghentian loop singkat, pembersihan tanpa memunculkan proyektil atau damage |
| First person | Attachment viewmodel/tangan terpisah, tidak menutupi crosshair |
| Multiplayer | Pelacakan owner dan observer menampilkan state yang tepat, membersihkan cast kedaluwarsa |
| LOD/accessibility | Jarak dekat/jauh, pengurangan partikel/gerak/kilatan; tanda serangan (telegraph) inti tetap terbaca |

Timing diambil dari `SkillTimeline` aktual. Studi Fire Jab 2/3/4 ticks adalah angka laporan saat ini yang harus diverifikasi ulang di repositori saat integrasi. VFX melakukan interpolasi berdasarkan partial tick; jangan menggantikan tick gameplay dengan FPS. Fire Jet tetap berupa dash. Fire Blast adalah paket prioritas untuk `HOLD_RELEASE`.

## 6. Matriks Seluruh Katalog Skill

Ke-62 entri di bawah ini merupakan cakupan karya seni masa depan. Banyak entri memakai kit yang sama; tidak perlu membuat 62 renderer terpisah. Kolom cast adalah label yang tercantum di `CONTENT_SPEC.md`, bukan hasil audit kode. Label `hold` lama perlu dinormalisasi melalui kontrak gameplay sebelum produksi final.

| Skill ID | Nama | Cast di Katalog | Paket Visual yang Diusulkan |
|---|---|---|---|
| `avatar:fire_jab` | Fire Jab | instant | Semburan api pada kepalan tangan + bara + impact |
| `avatar:flame_sweep` | Flame Sweep | instant | Ribbon melengkung + bara + jejak panas |
| `avatar:fire_jet` | Fire Jet (dash) | instant | Semburan pendorong singkat di tangan/kaki + ekor dash; bukan proyektil |
| `avatar:fire_guard` | Fire Guard | channel | Perisai cincin api + loop + reaksi benturan |
| `avatar:fire_blast` | Fire Blast | hold→release | Charge orb + proyektil + visual ledakan + cancel |
| `avatar:fire_stream` | Fire Stream | channel | Semburan api kontinu + titik sembur (nozzle) + impact loop |
| `avatar:fire_ring` | Fire Ring | instant | Cincin api menyebar di permukaan tanah + tepi lidah api |
| `avatar:fire_whip` | Fire Whip | instant | Ribbon/kurva api meruncing + ledakan kecil di ujung |
| `avatar:fire_arc` | Fire Arc | instant | Busur api meluncur + jejak lintasan |
| `avatar:fire_wall` | Fire Wall | instant | Tirai api + tepi dasar menyala + dissolve |
| `avatar:fire_shield` | Fire Shield | toggle | Kubah/panel api + riak saat terkena serangan |
| `avatar:fire_breath` | Fire Breath | channel | Kerucut api dari mulut + efek fatamorgana panas opsional |
| `avatar:jet_propulsion` | Jet Propulsion | channel | Loop semburan tangan/kaki + akselerasi/deselerasi |
| `avatar:flame_vortex` | Flame Vortex | channel | Heliks api + corong pusaran + debu dasar |
| `avatar:lightning_strike` | Lightning Strike | hold→release | Kilat bercabang + filamen pengisian + impact |
| `avatar:lightning_redirect` | Lightning Redirect | instant/counter | Kilat diterima/dialihkan + percikan listrik di tangan |
| `avatar:combustion_beam` | Combustion Beam | hold→release | Garis peringatan/sinar + titik ledakan + gelombang kejut |
| `avatar:blue_fire` | Blue Fire | passive modifier | Variasi material/palet api biru; tidak menduplikasi seluruh skill |
| `avatar:air_palm` | Air Palm | instant | Kerucut tekanan pendek + cincin + impact |
| `avatar:air_blast` | Air Blast | instant | Proyektil tekanan + cincin + jejak hembusan; orb hanya jika desain benar-benar memakai charge |
| `avatar:air_staff_attack` | Air Staff Attack | instant/combo | Ribbon mengikuti ujung/pangkal tongkat + tusukan/putaran/sapuan |
| `avatar:air_vortex` | Air Vortex | channel | Corong pusaran angin + pita hembusan + serpihan kosmetik |
| `avatar:air_swipe` | Air Swipe | instant | Bulan sabit angin + jejak |
| `avatar:air_wave` | Air Wave | instant | Muka gelombang angin + debu menyapu tanah |
| `avatar:air_funnel` | Air Funnel | hold | Corong meruncing + tarikan/dorongan sesuai state gameplay |
| `avatar:air_shield` | Air Shield | toggle | Kubah angin transparan + garis aliran + riak benturan |
| `avatar:air_cushion` | Air Cushion | instant | Bantalan udara rendah + cincin kompresi/pendaratan |
| `avatar:air_spout` | Air Spout | hold | Kolom pusaran di bawah tubuh + sustain/stop |
| `avatar:air_scooter` | Air Scooter | hold | Bola/cincin angin di bawah pemain + jejak gerak |
| `avatar:breath_of_wind` | Breath of Wind | instant | Kerucut angin dari mulut + garis hembusan |
| `avatar:true_flight` | True Flight | channel | Aliran udara di sekitar tubuh + lepas landas/mendarat |
| `avatar:sound_vibration` | Sound Vibration | instant | Gelombang cincin samar berirama + SFX |
| `avatar:air_suffocation` | Air Suffocation | channel | Cincin udara di sekitar target + indikator jelas dengan opasitas rendah |
| `avatar:water_whip` | Water Whip | instant | Kurva/tabung air meruncing + aliran + tetesan + cipratan |
| `avatar:water_jet` | Water Jet | channel | Semburan air kontinu + titik sembur + cipratan |
| `avatar:ice_spear` | Ice Spear | instant | Mesh tombak es + jejak embun beku + pecah berkeping |
| `avatar:ice_disk` | Ice Disk | instant | Mesh cakram es + putaran + pecah berkeping |
| `avatar:ice_shield` | Ice Shield | instant | Panel es + tahapan retakan + serpihan es |
| `avatar:water_wave` | Water Wave | hold | Mesh muka gelombang + puncak busa + cipratan tepi |
| `avatar:ice_prison` | Ice Prison | hold→release | Mesh/struktur kurungan es + buildup + retak/pecah |
| `avatar:water_arms` | Water Arms | hold | Dua kurva lengan air + attachment tangan/ujung |
| `avatar:octopus_form` | Octopus Form | channel | Banyak tabung tentakel meruncing + aliran + serangan ujung/cipratan, LOD |
| `avatar:steam_cloud` | Steam Cloud | instant | Sprite uap lembut + memudar + batas penghalangan pandang |
| `avatar:ice_path` | Ice Path | instant | Jalur/ubin es mengikuti permukaan tanah + tepi beku |
| `avatar:healing` | Healing | channel | Aliran air memutar di tangan/target + kilau lembut + loop |
| `avatar:bloodbending` | Bloodbending | channel | Penanda postur/kendali + aksen air sangat tipis; tanpa efek gore |
| `avatar:plantbending` | Plantbending | hold | Kurva sulur/daun + tumbuh/menarik kembali |
| `avatar:earth_wall` | Earth Wall | instant/construct actions | Blok/struktur dari material sumber + angkat/tendang/meluncur/impact/reklamasi |
| `avatar:earth_boulder` | Earth Boulder | instant | Mesh/bongkahan batu + debu angkatan + serpihan benturan |
| `avatar:earth_bullet` | Earth Bullet | instant | Batu kecil + jejak debu + benturan serpihan |
| `avatar:earth_pillar` | Earth Pillar | instant | Kolom material sumber + debu dasar + naik/menetap |
| `avatar:earth_rampart` | Earth Rampart | instant | Struktur pelindung multi-segmen + sambungan + debu |
| `avatar:ground_stomp` | Ground Stomp | instant | Cincin debu + hamparan retakan sementara + denyut tanah |
| `avatar:boulder_launch` | Boulder Launch | hold→release | Batu charge/melayang + meluncur + impact |
| `avatar:earth_armor` | Earth Armor | instant | Mesh pelindung batu melekat di tubuh + serpihan + pasang/lepas |
| `avatar:rock_cage` | Rock Cage | instant | Struktur kurungan batu + naik + hancur |
| `avatar:earth_surf` | Earth Surf | hold | Pijakan/gelombang tanah bergerak + jejak debu |
| `avatar:earth_tunnel` | Earth Tunnel | hold | Permukaan galian + serpihan + pratinjau aman sesuai transaksi dunia |
| `avatar:seismic_sense` | Seismic Sense | toggle | Denyut permukaan tanah + garis tepi target sesuai izin server |
| `avatar:metalbending_whip` | Metalbending Whip | instant | Kurva logam + kilau spekular + percikan benturan |
| `avatar:metal_cable` | Metal Cable | instant | Kurva kabel baja + kepala pengait + tegangan/tarik kembali |
| `avatar:lavabending` | Lavabending | hold→release | Mesh aliran lava + kerak + bara + panas; material nyata dari ledger |

## 7. Octopus Form: Kriteria Khusus

Air direpresentasikan melalui beberapa tabung melengkung yang meruncing di sepanjang spline, tekstur aliran memanjang di badan tentakel, serta busa/cipratan di area yang relevan. Jangan menyusun rangkaian kubus sebagai hasil akhir artistik. Server menyimpan geometri kolisi sederhana berbasis segmen/kapsul atau model yang disetujui; client melakukan interpolasi visual di sekitar data tersebut tanpa menentukan sendiri apakah serangan mengenai target. Batas toleransi antara tampilan visual dan volume hit harus dirancang secara eksplisit.

PoC dimulai dari satu tentakel → dua tentakel → jumlah final sesuai desain gameplay. Jumlah tentakel, segmen, verteks, dan jarak LOD wajib diukur kinerjanya sebelum dikunci. Uji tampilan menembus tentakel yang saling bertumpuk, di bawah air, latar gelap/terang, sudut pandang pengamat (observer), dan first person. Tidak perlu menjanjikan refraksi nyata sejak awal; kombinasi aliran + highlight + alpha yang tepat sudah cukup untuk menyampaikan kesan air.

## 8. Aura dan Cast Berkelanjutan

| Jenis | Kapan Muncul | Kapan Berhenti |
|---|---|---|
| Charge cue | State charge nyata dari teknik | Release/cancel/interruption |
| Sustained ability | Guard, berkendara, healing, atau channel sedang aktif | Mengikuti kondisi server; tidak berhenti sendiri hanya karena klip animasi selesai |
| Status cue | Burn/wet/chilled... benar-benar aktif | Saat status dihapus |
| Cosmetic mastery | Diaktifkan oleh pemain dan sudah di-unlock | Mematikan preferensi/keluar dunia; tidak menghasilkan damage |
| Avatar State | Saat sistem gameplay ini diimplementasikan dan aktif | State berakhir/interruption |

Air Scooter dan Air Spout menggunakan alur `start → loop → stop`; bagian loop tidak memasang batas waktu paksa (hard timeout) dari sisi visual untuk menghentikan jurus. Durasi gameplay, pengurangan chi, dan interupsi akibat serangan tetap ditentukan oleh spesifikasi/server. Setiap instance efek mengikat `owner + cast serial` guna mencegah loop lama hidup kembali setelah recast atau berpindah dunia.

## 9. UI Berdasarkan Mockup yang Disetujui

| Kit | Elemen yang Digambar (Artwork) | Elemen Runtime |
|---|---|---|
| Fondasi gulungan | Perkamen terang, tepi kertas, penggulung kayu, pita kain, pembatas | Tata letak melar/menyusut sesuai layar/GUI scale |
| Kontrol umum | Normal/hover/focus/pressed/disabled; checkbox/toggle, thumb, track, tab | Teks terjemahan, nilai slider, tooltip, navigasi |
| Variasi tema | Fire merah-emas, Water biru-putih, Earth hijau-cokelat, Air oranye-kuning, Neutral | AUTO mengikuti tribe, aksen mengikuti elemen aktif, opsi manual/minimal |
| HUD combat | Bingkai ringkas, mask bar, bingkai slot, segel aktif, cincin charge | Chi/cooldown/slot; bar darah hanya pada mode pengganti |
| Profil/tree | Segel tier/profesi, gaya simpul/penghubung | Model pemain, mastery, unlock, dan latihan nyata |
| Konstruksi | Motif valid/invalid dan ikon material | Geometri cetak biru, ketersediaan material, dan izin server |

Prioritaskan penyelesaian tema Water sebagai acuan pembanding terhadap mockup di atas sistem widget bersama. Jangan membuat lima logika layar terpisah. Jauhkan teks dari berkas gambar. Artwork boleh memiliki detail kaya, tetapi wajib diuji keterbacaannya pada GUI scale kecil. Area tengah HUD harus lapang; jangan menampilkan profil/skill tree secara penuh saat bertarung.

## 10. Batch Produksi dan Syarat Perpindahan Tahap

| Batch | Hasil yang Dibutuhkan | Syarat Penyelesaian |
|---|---|---|
| B0 — Audit | Inventaris aset saat ini, lisensi/asal-usul, dimensi, urutan frame, peta duplikat | Setiap kandidat memiliki status `reuse`/`fix`/`replace`; jangan membuat ulang aset yang sudah bagus |
| B1 — Fire Jab vertical slice | Ikon, kit burst/ember/smoke, attachment buku jari kanan, animasi/SFX/impact/cancel | Terlihat benar di dalam game pada mode first/third person dan observer; fase/hit selaras |
| B2 — Charge Fire Blast | Core/shell + ring/noise, start-loop-release-cancel, proyektil/impact | Lifecycle serta recast/interrupt/late tracking berjalan benar; pertahankan Fire Jet sebagai dash |
| B3 — Tiga kit elemen lainnya | Air ribbon/ring + staff/vortex; Water flow/splash + whip; Earth dust/chip + boulder | Satu skill per elemen berjalan di game; tekstur/renderer dapat dipakai ulang |
| B4 — Fondasi UI | Widget gulungan Water + HUD ringkas, dilanjutkan variasi tema | Berbagai GUI scale, fokus keyboard, input capture, menggunakan data nyata |
| B5 — Lanjutan | Octopus, wall berbasis sumber dunia, aura/mastery, profesi/konstruksi | Kontrak gameplay serta anggaran rig/render telah dikunci |

B1 dan B2 mengikuti checkpoint A–D tim saat ini tanpa membuat cabang gameplay tandingan. Artwork dapat disiapkan lebih awal, sedangkan ekspor animasi final menunggu template rig nyata. Katalog 62 ikon adalah target lengkap jangka panjang, bukan kewajiban menyelesaikan 62 ikon sekaligus saat ini. Set ikon awal (starter set): Fire Jab, Flame Sweep, Fire Guard, Fire Jet, Fire Blast, Air Staff Attack, Air Vortex, Water Whip, dan Earth Boulder; utamakan memeriksa ikon yang sudah ada terlebih dahulu.

Aset lama dilaporkan memiliki frame partikel, ikon skill/status, trail, model tongkat, dan mockup SFX. Laporan tersebut hanya menjadi titik awal audit; belum membuktikan bahwa aset-aset tersebut ada di `HEAD` saat ini atau sudah mencapai kualitas final.

## 11. Standar Serah Terima ke Dalam Game

| Kolom | Ketentuan |
|---|---|
| ID/path | Namespace aset `avatar_elements`; ID gameplay tetap mengikuti registri proyek, jangan mengubah `avatar:` secara sepihak |
| Source | Simpan `.bbmodel`/sumber berlapis/WAV dan prompt bila ada; pisahkan dari hasil ekspor runtime |
| Particle | `assets/avatar_elements/textures/particle/*.png`, `assets/avatar_elements/particles/*.json`; registrasi kode common/client |
| VFX texture | `assets/avatar_elements/textures/vfx/...` adalah konvensi proyek, bukan auto-discovery bawaan vanilla |
| UI | `assets/avatar_elements/textures/gui/...`; label teks disimpan di `lang/*.json` |
| Sound | `assets/avatar_elements/sounds/.../*.ogg` + `sounds.json`; mono untuk audio spasial, titik loop, dan kunci subtitle |
| Animation | Path/format mengikuti adaptor PAL yang digunakan; jangan mengasumsikan `.bbmodel` atau JSON Bedrock dapat berjalan langsung |
| Alpha/UV | PNG RGBA transparan sesuai kebutuhan; tanpa latar checkerboard, tanpa teks/logo/gizmo tertanam; perataan frame, pivot, dan arah UV konsisten |
| Blend/light | Deklarasikan opaque/cutout/translucent/additive bila didukung renderer; kebijakan depth/culling/light; uji sorted transparency |
| Scale/axes | Catat satuan, sumbu, pivot, bind pose, konvensi Euler/quaternion, dan konversi ke runtime; jangan menyalin mentah nilai Euler antar dua rig berbeda |
| Lifetime | `start`/`loop`/`end`/`cancel`, batas kecepatan/warna/skala, nama attachment, serta reset saat disconnect/mati/pindah dunia |
| Provenance | Pembuat/URL/lisensi/tanggal pengambilan, hak modifikasi dan distribusi di dalam `.jar`; bebas watermark tidak otomatis berarti boleh didistribusikan ulang |
| Status | `proposed → source_ready → exported → integrated → runtime_verified`; keberhasilan build tidak sama dengan `runtime_verified` |

Contoh catatan kerja (skema pengelolaan yang diusulkan, **BUKAN** loader JSON baru yang didukung langsung oleh mod):

```json
{
  "asset_id": "avatar_elements:fire/ember",
  "kind": "particle_sprite_sequence",
  "skills": ["avatar:fire_jab", "avatar:fire_blast"],
  "priority": "P0",
  "status": "proposed",
  "size_px": [32, 32],
  "frames": 6,
  "attachment": "right_knuckle",
  "phase": ["ACTIVE", "IMPACT"],
  "source_path": null,
  "runtime_paths": [],
  "license": "pending",
  "acceptance": ["alpha_clean", "phase_sync", "first_third_person", "observer", "lod"]
}
```

## 12. Kinerja dan Pengujian Penerimaan (Acceptance Testing)

Jangan menerapkan batas 2–5 partikel/detik milik aura pasif ke seluruh VFX pertarungan. Pisahkan anggaran (budget) antara aura pasif, burst singkat, dan mesh berkelanjutan; tetapkan angka berdasarkan hasil profiling pada perangkat target. Hindari penggunaan satu entity server untuk setiap percikan/tetesan kosmetik apabila mod dapat merendernya di sisi client.

| Pengujian | Hal yang Harus Diamati |
|---|---|
| Solo dan observer | First/third person, pemain yang baru masuk ke jangkauan pelacakan, caster lain, owner tidak ter-render dua kali |
| Lifecycle | Finish/cancel/knock/death/recast/disconnect/pindah dimensi/reload resource; tidak ada suara atau trail yang tertinggal |
| Geometri | Pivot/genggaman/tangan tepat, tidak memakai AABB kasar untuk menggantikan pemeriksaan kontak, tidak terjadi translasi ganda |
| Keterbacaan tempur | Arah, jangkauan, dan waktu penanda serangan terbaca jelas; hindari ukuran visual efek yang melebihi area damage sebenarnya |
| Pengaturan rendah | Pengurangan kepadatan partikel/trail/kilatan/getaran layar; pertahankan penanda serangan inti tanpa memberi keuntungan visual tidak adil di PvP |
| Render | Kondisi terang/gelap, di bawah air, tumpang-tindih objek transparan, mode Fabulous/Fast/Fancy bila didukung, serta berbagai GUI scale |
| Kinerja | Frame time serta jumlah partikel/verteks/draw call saat banyak caster aktif; jumlah entity server tidak bertambah mengikuti percikan kosmetik |
| Pengemasan | Skema aset Java 1.21.1; tekstur yang hilang tampak jelas di log; custom shader memiliki fallback |

## 13. Panduan Tugas Agent (Agent Brief)

- **Art / Antigravity**: Jalankan B0 terlebih dahulu, pertahankan checkpoint tongkat yang sudah dibekukan, bangun kit Fire Jab serta papan panduan per fase. Serahkan PNG terpisah berlatar transparan, berkas sumber yang dapat diedit, pratinjau dengan label terpisah, serta parameter attachment/timing. Jangan mengubah gameplay atau menambahkan skill baru hanya karena gambarnya sudah tersedia.
- **Runtime Agent**: Periksa repositori/Gradle aktual, tetapkan rig dan renderer bersama untuk burst/ribbon/ring/tube. Integrasikan Fire Jab dan Fire Blast sesuai pipeline yang ada dengan menjaga otoritas server dan nomor seri state. Selesaikan satu paket teknik secara utuh di dalam game sebelum memperluas ke skill lain.
- **Reviewer**: Bandingkan hasil render aktual terhadap konsep dari berbagai sudut pandang, pastikan kebersihan alpha/pivot/fase/cleanup/LOD, dan catat kelulusan build pass, solo pass, serta multiplayer pass secara terpisah.

## 14. Sumber Riset

Diakses pada 2026-11-08. Ketentuan artwork/batch/anggaran di atas adalah usulan untuk proyek ini, bukan fitur yang dijamin langsung oleh situs-situs referensi berikut:

- Pengantar ResourcePack AI: https://resourcepack.ai/docs
- Kebutuhan VFX, loop, dan batasan ZIP: https://resourcepack.ai/docs/vfx
- Format ekspor: https://resourcepack.ai/docs/exporting
- RP Engine skills: https://resourcepack.ai/docs/rp-engine/skills
- Rangkaian produk MythicCraft: https://mythiccraft.io/
- Pipeline impor ModelEngine: https://wiki.mythiccraft.io/modelengine/Modeling/Importing-a-Model
- Partikel Fabric 1.21.1: https://docs.fabricmc.net/1.21.1/develop/rendering/particles/creating-particles
- Layar custom Fabric 1.21.1: https://docs.fabricmc.net/1.21.1/develop/rendering/gui/custom-screens
- Suara custom Fabric 1.21.1: https://docs.fabricmc.net/1.21.1/develop/sounds/custom
- WorldRenderEvents API 0.115.6+1.21.1: https://maven.fabricmc.net/docs/fabric-api-0.115.6+1.21.1/net/fabricmc/fabric/api/client/rendering/v1/WorldRenderEvents.html
