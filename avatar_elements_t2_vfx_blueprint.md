# Blueprint Kandidat Art-Source & Catatan Integrasi Minimal Partikel Udara (Fase T2)

Dokumen ini merupakan revisi terbatas atas katalog kandidat aset `avatar_elements_t2_vfx_assets.zip` (tanpa meregenerasi ulang aset yang sudah ada, tanpa mengedit `mod/`, dan tanpa memperluas keputusan gameplay). Seluruh referensi API menggunakan **Yarn Mappings untuk Minecraft Java 1.21.1 + Fabric API** ([All Classes and Interfaces (yarn 1.21.1+build.1 API)](https://maven.fabricmc.net/docs/yarn-1.21.1+build.1/allclasses-index.html) dan [Creating Custom Particles - Fabric Documentation](https://docs.fabricmc.net/develop/rendering/particles/creating-particles)), yang terbukti dipakai oleh proyek dari import seperti `net.minecraft.util.Identifier` (`AvatarElementsMod.java:10`) dan `net.minecraft.registry.Registries` (`AvatarItems.java:8`).

## 1. Identitas Snapshot Source yang Diperiksa

Karena arsip source yang diunggah tidak menyertakan folder `.git`, identitas snapshot kerja (*working-tree snapshot*) dikunci menggunakan checksum SHA-256 dan daftar file aktual berikut:

* **Arsip Source:** `src.rar` (`17.607` byte, SHA-256: `3cb9bc1f21631a5822dcc2e254bb554ebd7d17a8a17ac992b92d1a4b71343806`)
* **Manifest Mod:** `fabric.mod.json` (`907` byte, SHA-256: `46038356159d2f34ab6f3ca1c379bdc94d90cada11d3ce35d4f169fbc9082176`)
* **Cakupan File dalam Snapshot (`24` file):**
  * **Client (`4` Java, `1` JSON):** `AvatarElementsClient.java` (`baris 1–31`), `AvatarKeyBindings.java` (`baris 1–34`), `ClientNetworkHandler.java` (`baris 1–33`), `SkillClientHandler.java` (`baris 1–55`), `avatar_elements.client.mixins.json` (`baris 1–9`).
  * **Common/Server (`12` Java, `2` JSON):** `AvatarElementsMod.java` (`baris 1–34`), `PlayerBendingData.java` (`baris 1–120`), `SkillTimeline.java` (`baris 1–76`), `AvatarItems.java` (`baris 1–31`), `AvatarNetworking.java` (`baris 1–66`), `AvatarServerEvents.java` (`baris 1–30`), `SkillNetworking.java` (`baris 1–89`), `SkillPackets.java` (`baris 1–86`), `TestActionPackets.java` (`baris 1–42`), `SkillDefinition.java` (`baris 1–23`), `SkillRegistry.java` (`baris 1–50`), `SkillValidator.java` (`baris 1–83`), `avatar_elements.mixins.json` (`baris 1–9`), `fabric.mod.json` (`baris 1–38`).
  * **Assets (`5` file):** `icon.png`, `items/air_staff.json` (`baris 1–6`), `lang/en_us.json` (`baris 1–7`), `models/item/air_staff.json` (`baris 1–115`), `textures/item/air_staff.png`.

## 2. Pemisahan Fakta Source, Usulan Visual, Usulan Gameplay, dan Belum Diverifikasi

| Kategori | Status & Detail Berdasarkan Bukti File/Baris |
| :--- | :--- |
| **Fakta Source (Terbukti di `src.rar`)** | • **Entrypoint & Inisialisasi:** `AvatarElementsMod.java:26-32` memanggil `SkillRegistry.populate()`, `AvatarItems.register()`, registrasi payload/receiver T1-2 & T1-3, serta `AvatarServerEvents.register()`. Belum ada registrasi `Registries.PARTICLE_TYPE` atau `Registries.STATUS_EFFECT`.<br>• **Skill Terdaftar:** `SkillRegistry.java:16-35` mendaftarkan 6 skill hard-coded: `avatar:fire_jab` (`baris 17-19`), `avatar:flame_sweep` (`baris 20-22`), `avatar:fire_jet` (`baris 23-25`), `avatar:fire_guard` (`baris 26-28`), `avatar:air_palm` (`baris 29-31`), dan `avatar:air_blast` (`baris 32-34`).<br>• **Timeline Fase:** `SkillTimeline.java:12, 31-66` menjalankan state machine `IDLE → WINDUP → ACTIVE → RECOVERY → IDLE` yang di-tick setiap akhir tick server melalui `AvatarServerEvents.java:22-26` → `PlayerBendingData.java:111-118` (`tickTimeline()` di `baris 93-98`).<br>• **Item Senjata:** `AvatarItems.java:15, 24-25` mendaftarkan `air_staff` sebagai `new Item(new Item.Settings().maxCount(1))` tanpa class kustom atau handler kombo.<br>• **Folder Resource:** Di dalam `src/main/resources/assets/avatar_elements/` hanya terdapat subfolder `items/`, `lang/`, `models/item/`, dan `textures/item/`. Belum ada subfolder `particles/`, `textures/particle/`, `textures/mob_effect/`, `textures/gui/`, maupun `textures/vfx/`. |
| **Usulan Visual (Kandidat `art-source` di `avatar_elements_t2_vfx_assets.zip`)** | • **Definisi & Frame Partikel:** 6 file JSON di `assets/avatar_elements/particles/` dan 22 frame PNG (`16x16`) di `assets/avatar_elements/textures/particle/` (`fire_ember`, `fire_arc_slash`, `air_gust_swirl`, `air_ring`, `water_droplet`, `earth_chunk`).<br>• **Ikon HUD Skill:** 6 ikon `16x16` PNG di `assets/avatar_elements/textures/gui/skills/` untuk ke-6 skill yang ada di `SkillRegistry.java:16-35`.<br>• **Tekstur Trail & Ikon Cadangan:** 4 tekstur pita `64x16` di `textures/vfx/` dan 6 ikon `18x18` di `textures/mob_effect/` disimpan murni sebagai kandidat visual di `art-source` (belum aktif di `mod/`). |
| **Usulan Gameplay (Backlog — Bukan Keputusan Aktif)** | • **Status Effect & Statistik Baru:** Ide efek status (`fire_guard`, `fire_jet_boost`, `air_mobility`, `chi_focus`, `earth_rooted`, `water_chilled`) serta ide skill/statistik Water & Earth (`water_whip`, `water_ice_shard`, `earth_throw`, `earth_wall_shock`) **bukan keputusan aktif** dan ditempatkan di backlog.<br>• **Moveset Alternatif:** Variasi gerakan di luar kombo prototipe dasar disimpan sebagai backlog. |
| **Belum Diverifikasi (Membutuhkan Bukti Runtime)** | • Bukti log kelulusan `./gradlew build` dan startup penuh `runClient` / `runServer` belum dilampirkan.<br>• Tampilan in-game `air_staff` di Minecraft 1.21.1 belum terverifikasi (`models/item/air_staff.json:2` menggunakan `"format_version": "26.3"` dari Blockbench dan `items/air_staff.json:1-6` menggunakan format Client Items 1.21.4+).<br>• Animasi frame partikel dari kandidat `avatar_elements_t2_vfx_assets.zip` belum berjalan di in-game sampai class `Particle` + `ParticleFactory` didaftarkan dan diuji di client. |

## 3. Koreografi Visual untuk 6 Skill Eksisting (`SkillRegistry.java:16-35`)

Tabel di bawah ini hanya memetakan **fakta stat** dari `SkillRegistry.java:16-35` dengan **usulan visual** kandidat partikel pada fase `SkillTimeline.java:12` (**tanpa mengubah damage, range, cooldown, atau menambahkan status effect**):

| Skill ID (`SkillRegistry.java`) | Stat Fakta (`chiCost / cd / windup / active / recovery / range`) | Usulan Visual `WINDUP` | Usulan Visual `ACTIVE` | Usulan Visual `RECOVERY` |
| :--- | :--- | :--- | :--- | :--- |
| `avatar:fire_jab` (`baris 17-19`) | `8 / 6t / 2t / 3t / 4t / 2.5m` | Spawn `fire_ember` kecil di posisi tangan pemain | Spawn `fire_arc_slash` + `fire_ember` bergerak lurus sejauh `2.5m` searah vektor pandang | Kepulan tipis `fire_ember` frame akhir memudar |
| `avatar:flame_sweep` (`baris 20-22`) | `15 / 12t / 3t / 8t / 6t / 5.0m` | Spawn `fire_ember` melingkar di sekitar pinggang | Sapuan busur horizontal `fire_arc_slash` di depan pemain hingga jarak `5.0m` | Sisa partikel `fire_ember` meluruh di tanah |
| `avatar:fire_jet` (`baris 23-25`) | `25 / 30t / 1t / 1t / 10t / 0.0m` | Kilatan `fire_ember` di titik kaki pemain | Semburan kerucut `fire_ember` ke arah berlawanan arah dorong | Jejak `fire_ember` mengecil selama `10t` |
| `avatar:fire_guard` (`baris 26-28`) | `10 (+2/t) / 8t / 2t / 60t / 5t / 0.0m` | Cincin `fire_ember` naik dari dasar kaki | Cincin partikel `fire_ember` mengelilingi pemain selama fase `ACTIVE` (`60t`) | Partikel cincin menyebar keluar dan hilang |
| `avatar:air_palm` (`baris 29-31`) | `6 / 5t / 2t / 2t / 4t / 3.0m` | Tarikan tipis `air_gust_swirl` di depan dada | Cincin `air_ring` melesat lurus ke depan sejauh `3.0m` | Disipasi `air_gust_swirl` di ujung jarak |
| `avatar:air_blast` (`baris 32-34`) | `12 / 10t / 3t / 4t / 6t / 8.0m` | Pusaran `air_gust_swirl` di sekeliling lengan | Gelombang beruntun `air_gust_swirl` + `air_ring` sepanjang jalur `8.0m` | Pusaran angin melambat dan transparan |

## 4. Kombo Prototipe `air_staff` (Dikembalikan ke: Tusukan → Putaran → Sapuan)

Urutan kombo prototipe untuk `air_staff` (`AvatarItems.java:15`) dikembalikan ke urutan resmi **Tusukan → Putaran → Sapuan** (tanpa penambahan status effect atau perubahan stat diluar kesepakatan). Variasi moveset alternatif dipindahkan ke bagian backlog di bawah.

| Urutan Kombo Prototipe | Gerakan Dasar | Usulan Visual Partikel & Trail Kandidat (`art-source`) |
| :--- | :--- | :--- |
| **Tahap 1: Tusukan (*Thrust*)** | Dorongan lurus ujung tongkat ke depan | 1 cincin `air_ring` di ujung tongkat + garis lurus pendek `air_gust_swirl` searah tusukan |
| **Tahap 2: Putaran (*Spin*)** | Putaran tongkat mengelilingi sumbu tubuh | Pita melingkar `air_staff_trail.png` / deretan `air_gust_swirl` mengikuti rotasi yaw pemain |
| **Tahap 3: Sapuan (*Sweep*)** | Ayunan melebar horizontal untuk menutup rangkaian kombo | Busur lebar `air_staff_trail.png` disertai pelepasan `air_gust_swirl` dan `air_ring` ke arah depan |

* **Backlog Moveset & Konten (Tidak Aktif):**
  * Moveset alternatif *Horizontal Sweep → Ascending Thrust → 360° Cyclone Vault Slam*.
  * Kandidat ikon status effect (`textures/mob_effect/*.png`) dan kandidat partikel Water/Earth (`water_droplet`, `earth_chunk`) disimpan di `art-source` hingga fase spesifikasi terkait disetujui.

## 5. Catatan Penting: Daftar `textures` JSON Bukan Bukti Animasi Berjalan

Menyediakan file JSON seperti `assets/avatar_elements/particles/air_gust_swirl.json` yang berisi daftar `"textures": ["avatar_elements:air_gust_swirl_0", ..., "avatar_elements:air_gust_swirl_3"]` **hanya memberi tahu `ParticleManager` di client untuk memuat keempat PNG tersebut ke dalam objek `SpriteProvider` pada texture atlas partikel** ([Creating Custom Particles - Fabric Documentation](https://docs.fabricmc.net/develop/rendering/particles/creating-particles)).

Daftar JSON tersebut **bukan bukti bahwa animasi frame berjalan otomatis**, karena di Minecraft Java 1.21.1 ([SpriteBillboardParticle (yarn API)](https://maven.fabricmc.net/docs/yarn-21w05b+build.8/net/minecraft/client/particle/SpriteBillboardParticle.html)):
1. Jika class partikel hanya memanggil `this.setSprite(spriteProvider)` di konstruktor (yang memilih 1 sprite acak), maka partikel akan menampilkan **1 frame statis yang sama** sepanjang hidupnya.
2. Agar frame PNG berganti dari `_0` → `_1` → `_2` → `_3` seiring bertambahnya umur partikel (`age` terhadap `maxAge`), class partikel di client **wajib** menyimpan referensi `SpriteProvider`, memanggil `this.setSpriteForAge(spriteProvider)` saat konstruksi, dan memanggil kembali `this.setSpriteForAge(this.spriteProvider)` di setiap `tick()` setelah mengecek `if (this.age++ >= this.maxAge)`.
3. Selain pergantian frame, perilaku fisika seperti ukuran (`scale`), batas umur (`maxAge`), gravitasi (`gravityStrength`), redaman kecepatan (`velocityMultiplier`), dan transparansi (`ParticleTextureSheet.PARTICLE_SHEET_TRANSLUCENT`, lihat [Particle (yarn 1.21.5+build.1 API)](https://maven.fabricmc.net/docs/yarn-1.21.5+build.1/net/minecraft/client/particle/Particle.html)) seluruhnya ditentukan di kode Java client, bukan di file JSON.

## 6. Usulan Integrasi Minimal 1 Partikel Udara (`avatar_elements:air_gust_swirl`) untuk Claude

Berikut adalah catatan dan snippet kode minimal bagi Claude untuk mengintegrasikan **satu partikel udara (`air_gust_swirl`)** pada Minecraft 1.21.1 (Fabric, Yarn mappings) **tanpa damage, tanpa status effect, dan tanpa mengubah dependency**.

### A. Penempatan File Aset dari `avatar_elements_t2_vfx_assets.zip`
Salin hanya 5 file berikut dari arsip kandidat ke `src/main/resources/`:
* `assets/avatar_elements/particles/air_gust_swirl.json`
* `assets/avatar_elements/textures/particle/air_gust_swirl_0.png`
* `assets/avatar_elements/textures/particle/air_gust_swirl_1.png`
* `assets/avatar_elements/textures/particle/air_gust_swirl_2.png`
* `assets/avatar_elements/textures/particle/air_gust_swirl_3.png`

### B. Registrasi Common (`src/main/java/com/avatarmod/elements/particle/AvatarParticles.java`)
Menggunakan `FabricParticleTypes.simple()` dari `net.fabricmc.fabric.api.particle.v1.FabricParticleTypes` dan mendaftarkannya ke `Registries.PARTICLE_TYPE` ([Creating Custom Particles - Fabric Documentation](https://docs.fabricmc.net/develop/rendering/particles/creating-particles)):

```java
package com.avatarmod.elements.particle;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;

public final class AvatarParticles {

    // false = tetap menghormati jarak render partikel standar client
    public static final SimpleParticleType AIR_GUST_SWIRL = FabricParticleTypes.simple(false);

    public static void register() {
        Registry.register(
                Registries.PARTICLE_TYPE,
                AvatarElementsMod.id("air_gust_swirl"),
                AIR_GUST_SWIRL
        );
    }

    private AvatarParticles() {}
}
```
*Catatan panggil di `AvatarElementsMod.java:27`:* tambahkan `AvatarParticles.register();` di dalam `onInitialize()`.

### C. Implementasi Partikel & Factory Client (`src/client/java/com/avatarmod/elements/client/particle/AirGustSwirlParticle.java`)
Menurunkan `SpriteBillboardParticle` ([SpriteBillboardParticle (yarn API)](https://maven.fabricmc.net/docs/yarn-21w05b+build.8/net/minecraft/client/particle/SpriteBillboardParticle.html)) dengan pemilihan frame berbasis umur (`setSpriteForAge`) dan sheet `PARTICLE_SHEET_TRANSLUCENT` ([Particle (yarn API)](https://maven.fabricmc.net/docs/yarn-1.21.5+build.1/net/minecraft/client/particle/Particle.html)) agar piksel semi-transparan pada PNG dirender dengan blending alpha yang benar:

```java
package com.avatarmod.elements.client.particle;

import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleFactory;
import net.minecraft.client.particle.ParticleTextureSheet;
import net.minecraft.client.particle.SpriteBillboardParticle;
import net.minecraft.client.particle.SpriteProvider;
import net.minecraft.client.world.ClientWorld;
import net.minecraft.particle.SimpleParticleType;

public class AirGustSwirlParticle extends SpriteBillboardParticle {

    private final SpriteProvider spriteProvider;

    protected AirGustSwirlParticle(
            ClientWorld world,
            double x, double y, double z,
            double velocityX, double velocityY, double velocityZ,
            SpriteProvider spriteProvider
    ) {
        super(world, x, y, z, velocityX, velocityY, velocityZ);
        this.spriteProvider = spriteProvider;
        this.maxAge = 10 + this.random.nextInt(6); // Umur 10-15 tick (~0.5 - 0.75 detik)
        this.scale = 0.22f;
        this.gravityStrength = -0.02f; // Mengambang naik tipis seperti hembusan angin
        this.velocityMultiplier = 0.92f;
        this.velocityX = velocityX;
        this.velocityY = velocityY;
        this.velocityZ = velocityZ;
        // Set frame awal (_0) sesuai age = 0
        this.setSpriteForAge(spriteProvider);
    }

    @Override
    public void tick() {
        this.prevPosX = this.x;
        this.prevPosY = this.y;
        this.prevPosZ = this.z;
        if (this.age++ >= this.maxAge) {
            this.markDead();
            return;
        }
        // Perbarui frame (_0 -> _1 -> _2 -> _3) proporsional terhadap age / maxAge
        this.setSpriteForAge(this.spriteProvider);
        this.move(this.velocityX, this.velocityY, this.velocityZ);
        this.velocityX *= this.velocityMultiplier;
        this.velocityY *= this.velocityMultiplier;
        this.velocityZ *= this.velocityMultiplier;
    }

    @Override
    public ParticleTextureSheet getType() {
        return ParticleTextureSheet.PARTICLE_SHEET_TRANSLUCENT;
    }

    public static class Factory implements ParticleFactory<SimpleParticleType> {
        private final SpriteProvider spriteProvider;

        public Factory(SpriteProvider spriteProvider) {
            this.spriteProvider = spriteProvider;
        }

        @Override
        public Particle createParticle(
                SimpleParticleType type,
                ClientWorld world,
                double x, double y, double z,
                double velocityX, double velocityY, double velocityZ
        ) {
            return new AirGustSwirlParticle(
                    world, x, y, z, velocityX, velocityY, velocityZ, this.spriteProvider
            );
        }
    }
}
```

### D. Registrasi Factory di `AvatarElementsClient.java`
Di dalam `AvatarElementsClient.onInitializeClient()` (`AvatarElementsClient.java:14`), daftarkan factory menggunakan overload `PendingParticleFactory` dari `ParticleFactoryRegistry` ([Creating Custom Particles - Fabric Documentation](https://docs.fabricmc.net/develop/rendering/particles/creating-particles)):

```java
ParticleFactoryRegistry.getInstance().register(
        AvatarParticles.AIR_GUST_SWIRL,
        AirGustSwirlParticle.Factory::new
);
```

### E. Prosedur Pengujian Mandiri (Tanpa Damage / Tanpa Status Effect)
1. **Uji via Command Vanilla (`/particle`) di Singleplayer & Dedicated Server:**
   * Pastikan pengaturan grafis client `Video Settings -> Particles` disetel ke `All`.
   * Jalankan perintah:
     ```mcfunction
     /particle avatar_elements:air_gust_swirl ~ ~1.2 ~ 0.25 0.15 0.25 0.02 12 normal
     ```
   * **Kriteria Lulus:** Tidak ada error `Unable to load particle description` atau `Missing texture` di log client; terlihat 12 partikel pusaran angin semi-transparan yang berganti bentuk dari frame `air_gust_swirl_0` hingga `air_gust_swirl_3` sebelum menghilang setelah ~10–15 tick.
2. **Uji Integrasi Visual pada `avatar:air_palm` atau `TestAction` (Server-Side Spawn Tanpa Gameplay Baru):**
   * Di handler server (mis. saat `avatar:air_palm` lolos validasi di `SkillNetworking.java:65` atau di dalam `AvatarNetworking.java:53`), panggil method bawaan `ServerWorld#spawnParticles`:
     ```java
     var look = player.getRotationVec(1.0f);
     player.getServerWorld().spawnParticles(
             AvatarParticles.AIR_GUST_SWIRL,
             player.getX() + look.x * 1.2,
             player.getEyeY() - 0.2 + look.y * 1.2,
             player.getZ() + look.z * 1.2,
             6,                  // count
             0.12, 0.12, 0.12,   // delta offset X, Y, Z
             0.04                // speed
     );
     ```
   * **Kriteria Lulus:** Saat pemain menekan tombol aksi/skill, partikel muncul di depan pemain baik bagi dirinya sendiri maupun pemain lain di dedicated server, tanpa memberikan damage atau efek status apa pun.