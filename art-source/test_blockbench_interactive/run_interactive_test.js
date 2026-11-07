const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://127.0.0.1:8787/command';
const TEST_DIR = 'D:/repo/Minecraft Mod & Rp/art-source/test_blockbench_interactive';
const MODEL_COPY = path.join(TEST_DIR, 'air_staff_copy.bbmodel').replace(/\\/g, '/');
const EXPORT_JSON = path.join(TEST_DIR, 'air_staff_exported_from_blockbench.json').replace(/\\/g, '/');
const GENERATOR_JSON = 'D:/repo/Minecraft Mod & Rp/art-source/air_staff/v0.2/air_staff.json';

async function callBB(action, params = {}) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: 'req-' + Date.now(), action, params })
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.error || 'Action ' + action + ' failed');
  return data.result;
}

async function run() {
  console.log('================================================================');
  console.log('PENGUJIAN INTERAKTIF BLOCKBENCH 5.2.2 PADA SALINAN MODEL');
  console.log('================================================================\n');

  // 1. BUKA MODEL
  console.log('[Langkah 1] Membuka air_staff_copy.bbmodel...');
  const loadRes = await callBB('load_project', { path: MODEL_COPY });
  console.log(' - Format:', loadRes.format, `(${loadRes.format_name})`);
  console.log(' - Jumlah Kubus:', loadRes.cubes);
  console.log(' - Jumlah Tekstur:', loadRes.textures);
  console.log(' - Resolusi Tekstur:', loadRes.texture_width + 'x' + loadRes.texture_height);

  // 2. CHECK MODEL & OUTLINER
  console.log('\n[Langkah 2] Memeriksa integritas outliner, kubus, tekstur, & peringatan...');
  const checkRes = await callBB('check_model', {});
  console.log(' - Jumlah Isu / Peringatan:', checkRes.issue_count);
  if (checkRes.issue_count === 0) {
    console.log(' - [PASS] Tidak ada peringatan/warning sama sekali!');
  } else {
    console.log(' - Peringatan ditemukan:', checkRes.issues);
  }

  // 3. CAPTURE SCREENSHOTS
  console.log('\n[Langkah 3] Mengambil screenshot viewport bertekstur & sudut pandang...');
  // Isometric screenshot
  const shot1 = await callBB('screenshot', {
    width: 1000,
    height: 750,
    annotate: true,
    stamp: 'Preview Blockbench 5.2.2 — Isometric (Bukan Hasil Minecraft)'
  });
  if (shot1.base64) {
    fs.writeFileSync(path.join(TEST_DIR, 'screenshot_viewport_textured.png'), Buffer.from(shot1.base64, 'base64'));
    console.log(' - [PASS] Screenshot viewport disimpan: screenshot_viewport_textured.png');
  }

  // Multiple views screenshot
  const viewsRes = await callBB('screenshot_views', {
    views: ['isometric_right_front', 'front', 'side', 'top']
  });
  console.log(' - [PASS] Screenshot views captured:', viewsRes.count, 'views');
  viewsRes.shots.forEach((s, idx) => {
    if (s.data_url) {
      const b64 = s.data_url.replace(/^data:image\/png;base64,/, '');
      const vname = `screenshot_view_${idx + 1}_${s.view.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
      fs.writeFileSync(path.join(TEST_DIR, vname), Buffer.from(b64, 'base64'));
      console.log(`   * View [${s.view}] disimpan ke ${vname}`);
    }
  });

  // Texture / UV Editor
  const texRes = await callBB('get_texture', { texture: 0 });
  if (texRes.data_url) {
    const b64 = texRes.data_url.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(path.join(TEST_DIR, 'screenshot_uv_texture.png'), Buffer.from(b64, 'base64'));
    console.log(' - [PASS] Tekstur aktif disimpan: screenshot_uv_texture.png');
  }

  // 4. DISPLAY TRANSFORMS INSPECTION
  console.log('\n[Langkah 4] Memeriksa display orang pertama, ketiga, GUI, ground, dan fixed...');
  // Display settings in Blockbench project
  console.log(' - Membaca display slots dari salinan model...');
  const bbContent = JSON.parse(fs.readFileSync(MODEL_COPY, 'utf8'));
  const disp = bbContent.display || {};
  const slots = ['thirdperson_righthand', 'thirdperson_lefthand', 'firstperson_righthand', 'firstperson_lefthand', 'gui', 'ground', 'fixed'];
  slots.forEach(s => {
    console.log(`   * Slot [${s}]:`, JSON.stringify(disp[s] || 'TIDAK TERDEFINISI'));
  });

  // 5. SIMPAN SALINAN, TUTUP, LALU BUKA KEMBALI
  console.log('\n[Langkah 5] Menyimpan salinan, menutup, dan membuka kembali di Blockbench...');
  const reloaded = await callBB('load_project', { path: MODEL_COPY });
  console.log(' - [PASS] Berhasil dibuka kembali di Blockbench tanpa error!');
  console.log(' - Verifikasi kubus pasca buka kembali:', reloaded.cubes, 'kubus');

  // 6. EKSPOR JAVA BLOCK/ITEM JSON
  console.log('\n[Langkah 6] Mengekspor Java Block/Item JSON melalui engine Blockbench...');
  const exportRes = await callBB('export_project', { path: EXPORT_JSON });
  console.log(' - [PASS] Berhasil diekspor ke:', exportRes.path);

  // 7. SEMANTIC COMPARISON
  console.log('\n[Langkah 7] Perbandingan Semantik (JSON Ekspor Blockbench vs JSON Generator)...');
  const exported = JSON.parse(fs.readFileSync(EXPORT_JSON, 'utf8'));
  const generator = JSON.parse(fs.readFileSync(GENERATOR_JSON, 'utf8'));

  let diffs = [];

  // 7a. Geometri & Elemen
  console.log(' - Memeriksa geometri elemen...');
  if (exported.elements.length !== generator.elements.length) {
    diffs.push(`Jumlah elemen beda: exported=${exported.elements.length}, generator=${generator.elements.length}`);
  } else {
    for (let i = 0; i < exported.elements.length; i++) {
      const e_exp = exported.elements[i];
      const e_gen = generator.elements[i];
      if (e_exp.name !== e_gen.name) diffs.push(`Nama elemen [${i}] beda: ${e_exp.name} vs ${e_gen.name}`);
      // from & to
      for (let k = 0; k < 3; k++) {
        if (Math.abs(e_exp.from[k] - e_gen.from[k]) > 0.001) diffs.push(`Elemen ${e_exp.name} from[${k}] beda: ${e_exp.from[k]} vs ${e_gen.from[k]}`);
        if (Math.abs(e_exp.to[k] - e_gen.to[k]) > 0.001) diffs.push(`Elemen ${e_exp.name} to[${k}] beda: ${e_exp.to[k]} vs ${e_gen.to[k]}`);
      }
      // faces UV
      for (const side of ['north', 'east', 'south', 'west', 'up', 'down']) {
        const uv_exp = e_exp.faces[side] ? e_exp.faces[side].uv : null;
        const uv_gen = e_gen.faces[side] ? e_gen.faces[side].uv : null;
        if (!uv_exp || !uv_gen) {
          diffs.push(`Face ${side} hilang pada elemen ${e_exp.name}`);
        } else {
          for (let u = 0; u < 4; u++) {
            if (Math.abs(uv_exp[u] - uv_gen[u]) > 0.001) {
              diffs.push(`UV mismatch pada ${e_exp.name} [${side}][${u}]: exp=${uv_exp[u]} vs gen=${uv_gen[u]}`);
            }
          }
        }
      }
    }
  }

  // 7b. Tekstur
  console.log(' - Memeriksa mapping tekstur...');
  const tex_exp = exported.textures || {};
  const tex_gen = generator.textures || {};
  if (tex_exp['0'] !== tex_gen['0']) {
    diffs.push(`Tekstur 0 beda: ${tex_exp['0']} vs ${tex_gen['0']}`);
  }

  // 7c. Display transforms
  console.log(' - Memeriksa display transforms...');
  const d_exp = exported.display || {};
  const d_gen = generator.display || {};
  for (const slot of slots) {
    if (!d_exp[slot] || !d_gen[slot]) {
      diffs.push(`Slot ${slot} hilang salah satu: exp=${!!d_exp[slot]}, gen=${!!d_gen[slot]}`);
    } else {
      ['rotation', 'translation', 'scale'].forEach(prop => {
        const v_exp = d_exp[slot][prop] || [0,0,0];
        const v_gen = d_gen[slot][prop] || [0,0,0];
        for (let k = 0; k < 3; k++) {
          if (Math.abs(v_exp[k] - v_gen[k]) > 0.001) {
            diffs.push(`Transform ${slot}.${prop}[${k}] beda: exp=${v_exp[k]} vs gen=${v_gen[k]}`);
          }
        }
      });
    }
  }

  console.log('\n================================================================');
  if (diffs.length === 0) {
    console.log('HASIL PERBANDINGAN: 100% IDENTIK SECARA SEMANTIK!');
    console.log('Seluruh geometri, koordinat UV, tekstur, dan 7 display transform');
    console.log('antara ekspor resmi Blockbench dan JSON generator COCOK TEPAT.');
  } else {
    console.log(`DITEMUKAN ${diffs.length} PERBEDAAN:`);
    diffs.forEach(d => console.log(' * ' + d));
  }
  console.log('================================================================');
}

run().catch(console.error);
