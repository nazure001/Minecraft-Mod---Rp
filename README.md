# Avatar: Elements — Minecraft Mod

Mod Avatar berbasis Fabric 1.21.1 untuk Minecraft Java Edition.

Empat elemen, sub-bending, senjata, animasi, dan sistem pertarungan dengan timeline terpadu: satu serangan memakai satu timeline untuk animasi, hitbox, VFX, suara, dan kesempatan kombo.

## Status proyek

Status implementasi, build, dan uji runtime harus dibaca terpisah dari milestone/roadmap. Lihat [`docs/TASKS.md`](docs/TASKS.md) untuk rincian pekerjaan; milestone yang direncanakan bukan klaim seluruh fitur sudah selesai atau diterima.

## Struktur folder

```
Minecraft Mod & Rp/
├── AGENTS.md           # Aturan kerja dan verifikasi
├── README.md
├── .gitignore
├── docs/
│   ├── PROJECT_PLAN.md  # Roadmap dan gate
│   ├── ARCHITECTURE.md  # Arsitektur aktual dan rancangan
│   ├── CONTENT_SPEC.md  # Schema/runtime snapshot dan katalog desain
│   ├── TASKS.md         # Status dan backlog
│   ├── TESTING.md       # Alur verifikasi
│   └── DECISIONS.md     # Keputusan teknis
├── reference/          # JAR referensi dan addon Bedrock (tidak didistribusikan)
├── legacy/             # Datapack dan resourcepack lama
└── mod/                # Source mod Fabric 1.21.1
```

`tests/` berisi suite Python terpisah dari source set test Gradle. Angka skill yang aktif dimuat dari `mod/src/main/resources/data/avatar_elements/skill_definitions.json`; `docs/CONTENT_SPEC.md` membedakan nilai aktif dari katalog desain.

## Prasyarat & Toolchain

- **Gradle Daemon Runtime (Loom 1.19.3)**: Membutuhkan **JVM 25** (misalnya Eclipse Temurin JDK 25 di `C:/Users/USER/.jdks/jdk-25.0.5+8` atau disetel via `org.gradle.java.home` di `gradle.properties`).
  > **Penting**: Menjalankan Gradle daemon hanya dengan Java 17 akan **gagal** (`Dependency requires at least JVM runtime version 25` per keputusan `docs/DECISIONS.md` D012).
- **Mod Compiler Toolchain**: Menargetkan **Java 21** (`sourceCompatibility = JavaVersion.VERSION_21`, `targetCompatibility = JavaVersion.VERSION_21`, `release = 21` via Gradle Java toolchain).
- **Git**: 2.x
- **Gradle**: Menggunakan wrapper yang disediakan di folder `mod/` (`gradlew` / `gradlew.bat`).

## Memulai

```bash
cd mod
./gradlew build
./gradlew runClient
```

## Kontribusi

Lihat [`AGENTS.md`](AGENTS.md) untuk aturan kolaborasi multi-agent dan alur kerja branch.

## Referensi

- [Epic Fight Mod](https://github.com/Yesssssman/epicfightmod) — sistem animasi pertarungan
- [Fabric Wiki](https://fabricmc.net/wiki/) — dokumentasi Fabric 1.21.1
