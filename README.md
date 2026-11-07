# Avatar: Elements — Minecraft Mod

Mod Avatar berbasis Fabric 1.21.1 untuk Minecraft Java Edition.

Empat elemen, sub-bending, senjata, animasi, dan sistem pertarungan dengan timeline terpadu: satu serangan memakai satu timeline untuk animasi, hitbox, VFX, suara, dan kesempatan kombo.

## Status proyek

Tahap 0–1: Audit + fondasi. Lihat [`docs/TASKS.md`](docs/TASKS.md) untuk status terkini.

## Struktur folder

```
avatar-project/
├── AGENTS.md           # Aturan kerja multi-agent
├── README.md
├── .gitignore
├── docs/
│   ├── PROJECT_PLAN.md   # Rencana menyeluruh
│   ├── ARCHITECTURE.md   # Arsitektur teknis
│   ├── CONTENT_SPEC.md   # Spesifikasi gameplay
│   ├── TASKS.md          # Daftar tugas aktif
│   ├── TESTING.md        # Panduan pengujian
│   └── DECISIONS.md      # Keputusan teknis
├── reference/          # JAR referensi dan addon Bedrock (tidak didistribusikan)
├── legacy/             # Datapack dan resourcepack lama
└── mod/                # Source mod Fabric 1.21.1
```

## Prasyarat

- Java 17+
- Git 2.x
- Gradle (via wrapper di `mod/`)

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
