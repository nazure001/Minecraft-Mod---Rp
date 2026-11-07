const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://127.0.0.1:8787/command';
const HANDOFF_DIR = 'D:/repo/Minecraft Mod & Rp/art-source/air_staff/handoff_claude';
const SOURCE_PNG = 'D:/repo/Minecraft Mod & Rp/art-source/test_blockbench_interactive/air_staff_candidate.png';
const TEMPLATE_BB = 'D:/repo/Minecraft Mod & Rp/art-source/test_blockbench_interactive/air_staff_copy.bbmodel';

const TARGET_PNG = path.join(HANDOFF_DIR, 'air_staff.png');
const TARGET_BB = path.join(HANDOFF_DIR, 'air_staff.bbmodel');
const TARGET_JSON = path.join(HANDOFF_DIR, 'air_staff.json');
const TARGET_SCREENSHOT = path.join(HANDOFF_DIR, 'air_staff_clean_viewport.png');

async function callBB(action, params = {}) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: 'req-' + Date.now(), action, params })
  });
  const data = await res.json();
  if (!data.ok) {
    throw new Error(`[Blockbench Error in ${action}]: ` + (data.error || JSON.stringify(data)));
  }
  return data.result;
}

async function main() {
  console.log('=== MEMULAI PEMBEKUAN DAN PENYIAPAN HANDOFF KE CLAUDE CODE ===\n');

  // 1. Copy Candidate 2 PNG to air_staff.png
  console.log('[1] Menyalin tekstur kandidat ke runtime name air_staff.png...');
  fs.copyFileSync(SOURCE_PNG, TARGET_PNG);
  const pngBuf = fs.readFileSync(TARGET_PNG);
  const pngB64 = 'data:image/png;base64,' + pngBuf.toString('base64');
  console.log(' - OK: air_staff.png ukuran', pngBuf.length, 'bytes');

  // 2. Prepare air_staff.bbmodel
  console.log('\n[2] Menyiapkan source model air_staff.bbmodel...');
  const bbData = JSON.parse(fs.readFileSync(TEMPLATE_BB, 'utf8'));
  bbData.name = 'air_staff';
  bbData.model_identifier = 'avatar_elements:item/air_staff';
  
  // Setup texture reference
  if (!bbData.textures || bbData.textures.length === 0) {
    throw new Error('No textures found in template bbmodel');
  }
  bbData.textures[0].name = 'air_staff';
  bbData.textures[0].path = 'air_staff.png';
  bbData.textures[0].folder = 'item';
  bbData.textures[0].namespace = 'avatar_elements';
  bbData.textures[0].particle = true;
  bbData.textures[0].source = pngB64;
  
  fs.writeFileSync(TARGET_BB, JSON.stringify(bbData, null, 2), 'utf8');
  console.log(' - OK: air_staff.bbmodel tersimpan di', TARGET_BB);

  // 3. Load into Blockbench
  console.log('\n[3] Memuat air_staff.bbmodel ke Blockbench 5.2.2...');
  const loadRes = await callBB('load_project', { path: TARGET_BB });
  console.log(' - Project loaded:', loadRes.name, `(${loadRes.cubes} cubes)`);
  if (loadRes.cubes !== 5) throw new Error('Expected 5 cubes, got ' + loadRes.cubes);

  // 4. Run check_model audit
  console.log('\n[4] Memeriksa model dengan check_model...');
  const checkRes = await callBB('check_model', {});
  console.log(' - Hasil check_model: issue_count =', checkRes.issue_count);
  if (checkRes.issue_count !== 0) {
    console.warn(' - Peringatan plugin:', checkRes.issues);
  } else {
    console.log(' - [PASS] Model lolos audit plugin Blockbench.');
  }

  // 5. Export JSON using Blockbench Java Block/Item codec
  console.log('\n[5] Mengekspor Java Block/Item JSON langsung via Blockbench...');
  const exportRes = await callBB('export_project', { path: TARGET_JSON });
  console.log(' - OK: Export berhasil ke', TARGET_JSON);

  // 6. Verify exported JSON
  console.log('\n[6] Verifikasi isi file JSON hasil ekspor...');
  const exportedJson = JSON.parse(fs.readFileSync(TARGET_JSON, 'utf8'));
  console.log(' - Textures map:', JSON.stringify(exportedJson.textures));
  console.log(' - Elements count:', exportedJson.elements.length);
  console.log(' - Display slots:', Object.keys(exportedJson.display || {}));
  
  if (exportedJson.textures['0'] !== 'avatar_elements:item/air_staff') {
    throw new Error('Texture reference mismatch! Expected avatar_elements:item/air_staff, got ' + exportedJson.textures['0']);
  }

  // 7. Capture Clean Screenshot (annotate: false)
  console.log('\n[7] Mengambil screenshot BERSIH tanpa anotasi bertumpuk (annotate: false)...');
  const shotRes = await callBB('screenshot', {
    view: 'front_right',
    width: 1200,
    height: 900,
    annotate: false
  });
  if (!shotRes.base64) throw new Error('Failed to capture screenshot');
  const shotBuf = Buffer.from(shotRes.base64, 'base64');
  fs.writeFileSync(TARGET_SCREENSHOT, shotBuf);
  console.log(' - OK: Screenshot bersih disimpan di', TARGET_SCREENSHOT, `(${shotBuf.length} bytes)`);

  console.log('\n=== PEMBEKUAN DAN VERIFIKASI SELESAI DENGAN SUKSES ===');
}

main().catch(err => {
  console.error('[GAGAL]:', err);
  process.exit(1);
});
