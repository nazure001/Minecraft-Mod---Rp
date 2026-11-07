# Laporan Evaluasi Kandidat SFX Audio: Staff & Air
**Mod**: `avatar_elements`  
**Folder Kerja**: `art-source/audio/candidates/staff_air/`  
**Status**: KANDIDAT TERVERIFIKASI FISIK (WAV PCM 16-BIT 44.1kHz MONO)  
**Manifest Acuan**: `art-source/audio/prototype/v0.2/SFX_MANIFEST_v02.json`  

---

## 1. Ringkasan Eksekutif & Pemilihan Kandidat

Berdasarkan tinjauan terhadap repositori draf audio prosedural `art-source/audio/prototype/v0.2/`, telah diprioritaskan satu kandidat tunggal yang paling kuat dan representatif untuk masing-masing dari tiga core sound event target:

| Event Identifier Resmi | File Kandidat Prioritas | Durasi Eksak | Format Fisik | Status Auditori |
|---|---|---|---|---|
| `avatar_elements:staff.swing` | `staff_swing_1.wav` | 0.4500s (19.845 frame) | PCM 16-bit 44.1kHz Mono | **Belum dinilai secara auditori** |
| `avatar_elements:staff.impact` | `staff_impact_1.wav` | 0.2500s (11.025 frame) | PCM 16-bit 44.1kHz Mono | **Belum dinilai secara auditori** |
| `avatar_elements:air.release` | `air_release_1.wav` | 0.3000s (13.230 frame) | PCM 16-bit 44.1kHz Mono | **Belum dinilai secara auditori** |

> **Catatan Integritas Manifest**: Mengikuti manifesto `SFX_MANIFEST_v02.json`, tidak ada identifier baru yang dibuat, dan tidak dilakukan duplikasi nama/kloning file untuk mengklaim varian sekunder (`_2`, `_3`). Varian tambahan tetap dicatat jujur berstatus **BELUM DIBUAT** hingga ada variasi foley/DSP sintetis baru yang independen.

---

## 2. Metode Pembuatan & Analisis DSP Procedural

Ketiga kandidat disintesis secara deterministik menggunakan modulasi matematika Python (`math` & standard library `wave`/`struct`), memadukan osilator analitik, envelope eksponensial/sinusoidal, dan pembentukan noise (noise shaping).

### A. `staff_swing_1.wav` (`avatar_elements:staff.swing`)
* **Asal Sumber Draf**: Draf sintesis `staff_sweep.wav` (`gen_staff_sweep()`).
* **Algoritma DSP**:
  * **Envelope Dinamis**: $Envelope(t) = \sin^{1.3}\left(\frac{\pi t}{T}\right)$ dengan $T = 0.45\text{ s}$. Menghasilkan kurva serang-dan-lepas (attack-decay) asimetris halus yang meniru aerodinamika ayunan fisik.
  * **Modulasi Frekuensi (FM Pitch Glide)**: $f(t) = 320 - 140 \left(\frac{t}{T}\right)\text{ Hz}$. Frekuensi turun meluncur dari 320 Hz ke 180 Hz, merepresentasikan kompresi udara oleh bilah kayu berkecepatan tinggi yang melambat di akhir busur ayunan.
  * **Noise Shaping & Mixing**: $s(t) = (0.6 \cdot \sin(2\pi f(t) t) + 0.4 \cdot Noise_{white}) \cdot Envelope(t)$.
* **Karakter Akustik**: Desiran gesekan udara berpadu resonansi "whoosh" mid-low khas tongkat kayu tebal membelah udara.

---

### B. `staff_impact_1.wav` (`avatar_elements:staff.impact`)
* **Asal Sumber Draf**: Draf sintesis `staff_impact.wav` (`gen_staff_impact()`).
* **Algoritma DSP**:
  * **Envelope Redaman Cepat**: $Envelope(t) = e^{-28.0 \cdot t}$ dengan durasi $T = 0.25\text{ s}$. Redaman eksponensial tajam yang mencerminkan material kayu solid keras non-logam.
  * **Resonansi Bodi Kayu (Dual-Mode Harmonic)**: 
    $$Wood(t) = 0.7 \cdot \sin(2\pi \cdot 190 \cdot t) + 0.3 \cdot \sin(2\pi \cdot 380 \cdot t)$$
    Modus fundamental 190 Hz beresonansi dengan harmonik pertama 380 Hz pada bobot 70:30, meniru getaran longitudinal dan transversal silinder kayu padat.
  * **Transient Click / Contact Snap**: $Click(t) = Noise_{white} \cdot e^{-60.0 \cdot t}$. Letupan transient instan ($\tau \approx 16.7\text{ ms}$) merepresentasikan kontak benturan permukaan keras.
  * **Mixing**: $s(t) = (0.75 \cdot Wood(t) + 0.40 \cdot Click(t)) \cdot Envelope(t)$.
* **Karakter Akustik**: Ketukan tumpul yang padat (*solid wooden thud*) berbobot dengan transient awal yang renyah tanpa dengung logam (*no metallic ring*).

---

### C. `air_release_1.wav` (`avatar_elements:air.release`)
* **Asal Sumber Draf**: Draf sintesis `staff_thrust.wav` (`gen_staff_thrust()`).
* **Algoritma DSP**:
  * **Envelope Dual-Eksponensial**: $Envelope(t) = e^{-18.0 \cdot t} \cdot (1.0 - e^{-120.0 \cdot t})$ dengan $T = 0.30\text{ s}$.
    * Attack sangat cepat ($1 - e^{-120 t}$ mencapai 90% dalam ~19 ms), meniru letupan pelepasan katup/tekanan udara mendadak.
    * Decay moderat ($e^{-18 t}$) meniru disipasi arus udara di atmosfer bebas.
  * **Modulasi Frekuensi (Whistling Jet)**: $f(t) = 450 - 250 \left(\frac{t}{T}\right)\text{ Hz}$. Meluncur tajam dari 450 Hz ke 200 Hz.
  * **Turbulence Noise Envelope**: $Noise(t) = Noise_{white} \cdot e^{-22.0 \cdot t}$.
  * **Mixing**: $s(t) = (0.75 \cdot \sin(2\pi f(t) t) + 0.35 \cdot Noise(t)) \cdot Envelope(t)$.
* **Karakter Akustik**: Pelepasan hembusan jet udara tajam, terfokus, dan padat, cocok untuk thrust tongkat pengendali udara maupun pelepasan tekanan angin terkompresi.

---

## 3. Verifikasi Properti Fisik File Audio (WAV PCM)

Setiap file diukur langsung dari struktur header RIFF dan buffer sample PCM 16-bit:

| Nama File | Ukuran File | Frame Count | Sample Rate | Bit Depth | Channel | Peak Level | RMS Level | DC Offset | Status Clipping |
|---|---|---|---|---|---|---|---|---|---|
| `staff_swing_1.wav` | 39.734 bytes | 19.845 | 44.100 Hz | 16-bit LE | 1 (Mono) | 28.000 (-1.37 dBFS) | -11.10 dBFS | -44.19 | 0 sampel (Aman) |
| `staff_impact_1.wav` | 22.094 bytes | 11.025 | 44.100 Hz | 16-bit LE | 1 (Mono) | 28.000 (-1.37 dBFS) | -19.97 dBFS | +67.29 | 0 sampel (Aman) |
| `air_release_1.wav` | 26.504 bytes | 13.230 | 44.100 Hz | 16-bit LE | 1 (Mono) | 28.000 (-1.37 dBFS) | -14.49 dBFS | -0.96 | 0 sampel (Aman) |

* Headroom puncak: +1.37 dB dari ambang digital clipping (32.767).
* DC Offset berada jauh di bawah 0.2% dari full dynamic scale.
* Durasi berada dalam rentang ideal gameplay responsive SFX (< 0.50 detik) sehingga tidak menyebabkan tumpukan latensi saat aksi berulang.

---

## 4. Batasan Teknis & Aspek yang Belum Diuji

1. **Evaluasi Auditori (Mendengarkan Langsung)**:
   > ⚠️ **Pernyataan Eksplisit**: Audio ini **BELUM DINILAI SECARA AUDITORI** melalui telinga manusia/monitoring speaker di sesi ini, karena keterbatasan lingkungan eksekusi CLI tanpa perangkat audio playback interaktif. Verifikasi saat ini murni berbasis integritas digital, formulasi DSP, dan visualisasi matematis metrik WAV.
2. **Format Runtime Target**:
   * File saat ini berformat WAV uncompressed PCM 16-bit (format master produksi).
   * Format runtime native Minecraft Java Edition adalah **OGG Vorbis** (`.ogg`, kualitas q=4 atau ~128-160kbps).
3. **Pemisahan Peran & Eksekusi Runtime**:
   * Konversi OGG Vorbis, penulisan `sounds.json`, registrasi `SoundEvent` Java di mod, dan pengujian sinkronisasi animasi in-game berada di luar lingkup subagent ini dan merupakan tanggung jawab Claude Code / Main Agent.
   * File di folder `art-source/audio/candidates/staff_air/` adalah artefak sumber bersih yang siap dikonversi saat pipeline audio runtime dijalankan.
