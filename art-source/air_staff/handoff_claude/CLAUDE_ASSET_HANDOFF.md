# Claude Code Asset Handover: Air Staff Prototype (v0.2)
**Minecraft Java Edition 1.21.1 | Namespace: `avatar_elements`**
**Status:** Frozen Prototype Asset (Candidate 2 Selected)
**Verified with:** Blockbench 5.2.2 & BlockbenchMCP

---

## 1. Item Registry Identity
- **Namespace:** `avatar_elements`
- **Item Identifier:** `air_staff`
- **Full ResourceLocation:** `avatar_elements:air_staff`

---

## 2. Runtime Asset Mapping Table

| Source File (in `art-source/`) | Target Runtime Location (in `mod/src/main/resources/assets/avatar_elements/`) | Description |
| :--- | :--- | :--- |
| `art-source/air_staff/handoff_claude/air_staff.json` | `models/item/air_staff.json` | Java Block/Item Model JSON (Blockbench 5.2.2 export) |
| `art-source/air_staff/handoff_claude/air_staff.png` | `textures/item/air_staff.png` | 32x32 RGBA Texture (Candidate 2 - Ash grain & linen wrap) |
| `art-source/air_staff/handoff_claude/air_staff.bbmodel` | *(Art source archive / non-runtime)* | Editable Blockbench source project |

### Audio Prototype Events (Sesuai SFX_MANIFEST_v02.json)
Daftar event audio yang disepakati merujuk sepenuhnya pada:  
[`art-source/audio/prototype/v0.2/SFX_MANIFEST_v02.json`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/audio/prototype/v0.2/SFX_MANIFEST_v02.json)

**Ketentuan Integrasi Audio:**
- **Daftar Event:** Gunakan 14 event inti yang sudah disepakati di manifest (skema namespace `avatar_elements:fire.*`, `avatar_elements:staff.*`, `avatar_elements:air.*`). Jangan membuat atau mengganti identifier dengan skema baru seperti `item.air_staff.*`.
- **Status Varian:** Terdapat 9 varian mockup sintetis yang tersedia secara fisik di folder `art-source/audio/prototype/v0.2/` dan 18 varian berstatus `BELUM DIBUAT` (didokumentasikan dalam manifest).
- **Format Runtime Target:** Mod Java Edition 1.21.1 menggunakan OGG Vorbis 44.1kHz yang didaftarkan melalui `assets/avatar_elements/sounds.json` mengacu pada event manifest tersebut.

---

## 3. Model & Texture Specifications

### Geometri & Elemen
- **Total Cubes:** 5 (`lower_cap`, `lower_shaft`, `grip_wrap`, `upper_shaft`, `upper_cap`).
- **Dimensi Total:** Tinggi 30 unit (Y: -7 s.d. +23), shaft 1.5x1.5 unit, grip & caps 2.0x2.0 unit.
- **Pivot Root:** `[8, 8, 8]`.

### Texture & UV
- **Tekstur Resolusi:** 32x32 pixel.
- **Reference Keys:** 
  - `"0": "avatar_elements:item/air_staff"`
  - `"particle": "avatar_elements:item/air_staff"`
- **Karakteristik Visual (Kandidat 2):**
  - **Shaft:** Serat kayu vertikal memanjang sepanjang sumbu Y (meniadakan pola kotak catur/belang repetitif).
  - **Grip:** Lilitan linen 4-tingkat dengan kontras bayangan lipatan (`#8A7C68`) dan highlight tepian (`#EEEAE0`).

### Display Transforms
Telah dikonfigurasi lengkap untuk:
- `thirdperson_righthand` / `thirdperson_lefthand`
- `firstperson_righthand` / `firstperson_lefthand`
- `ground`
- `gui`
- `fixed`

---

## 4. Backlog / Catatan Polish Berikutnya
- **Diagonal Grip Refinement:** Tekstur lilitan grip saat ini disetujui sebagai placeholder fungsional prototipe. Polish lebih lanjut (variasi lilitan diagonal resolusi tinggi) dialokasikan untuk iterasi visual berikutnya tanpa memblokir implementasi kode item.

---

## 5. Status Verifikasi
- [x] Lolos audit plugin `check_model` (0 issues).
- [x] Ekspor semantik 100% konsisten antara Blockbench Compiler dan JSON runtime.
- [x] Tangkapan viewport bersih tersedia di `air_staff_clean_viewport.png`.
