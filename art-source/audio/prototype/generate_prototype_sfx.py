import os
import wave
import struct
import math
import random
import numpy as np

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype"
os.makedirs(out_dir, exist_ok=True)

SAMPLE_RATE = 44100

def write_wav(filename, samples):
    path = os.path.join(out_dir, filename)
    # Normalize samples to -32767 to 32767
    max_amp = max(abs(s) for s in samples) if samples else 1.0
    if max_amp == 0:
        max_amp = 1.0
    norm_factor = 28000.0 / max_amp
    
    with wave.open(path, 'wb') as wav:
        wav.setnchannels(1) # mono
        wav.setsampwidth(2) # 16-bit
        wav.setframerate(SAMPLE_RATE)
        raw_data = bytearray()
        for s in samples:
            val = int(s * norm_factor)
            val = max(-32767, min(32767, val))
            raw_data.extend(struct.pack('<h', val))
        wav.writeframes(raw_data)
    print(f"Generated WAV: {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")
    return path

# 1. FIRE JAB (Short punchy whoosh + flame pop, 0.35s)
def gen_fire_jab():
    dur = 0.35
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 14.0) * (1.0 - math.exp(-t * 80.0))
        # Pitch drops rapidly from 350Hz to 90Hz
        freq = 90.0 + 260.0 * math.exp(-t * 18.0)
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 10.0)
        s = (sine * 0.7 + noise * 0.5) * env
        samples.append(s)
    return samples

# 2. FLAME SWEEP (Expansive 180 deg flame whoosh with crackle, 0.65s)
def gen_flame_sweep():
    dur = 0.65
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        # Envelope rises then falls
        env = math.sin(math.pi * (t / dur)) ** 1.5
        # Low roar + white noise shaped
        freq = 140.0 + 100.0 * math.sin(math.pi * (t / dur))
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0)
        # Random crackle bursts
        crackle = 2.0 if random.random() < 0.03 else 0.0
        s = (sine * 0.4 + noise * 0.6 + crackle * 0.3) * env
        samples.append(s)
    return samples

# 3. FIRE JET (Sustained rocket-like propulsion blast, 0.80s)
def gen_fire_jet():
    dur = 0.80
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.1:
            env = t / 0.1
        elif t > 0.6:
            env = (dur - t) / 0.2
        else:
            env = 1.0
        freq = 75.0 + 30.0 * math.sin(2.0 * math.pi * 3.0 * t)
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0)
        s = (sine * 0.35 + noise * 0.65) * env
        samples.append(s)
    return samples

# 4. FIRE IMPACT (Combustion detonation & burn crackle, 0.50s)
def gen_fire_impact():
    dur = 0.50
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 9.0)
        # Deep boom (60Hz)
        boom = math.sin(2.0 * math.pi * 60.0 * t) * math.exp(-t * 15.0)
        noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 7.0)
        s = (boom * 0.6 + noise * 0.4) * env
        samples.append(s)
    return samples

# 5. STAFF THRUST (Sharp crisp wooden piercing whoosh, 0.30s)
def gen_staff_thrust():
    dur = 0.30
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 18.0) * (1.0 - math.exp(-t * 120.0))
        freq = 450.0 - 250.0 * (t / dur)
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 22.0)
        s = (sine * 0.75 + noise * 0.35) * env
        samples.append(s)
    return samples

# 6. STAFF SPIN (Cyclic dual-whirring propeller whoosh, 0.75s)
def gen_staff_spin():
    dur = 0.75
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        # 3 rotation cycles (approx 4Hz spin modulation)
        spin_mod = 0.5 + 0.5 * math.sin(2.0 * math.pi * 5.0 * t)
        freq = 280.0 + 80.0 * spin_mod
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * spin_mod
        s = (sine * 0.5 + noise * 0.5) * env
        samples.append(s)
    return samples

# 7. STAFF SWEEP (Wide airy wooden stave swing, 0.45s)
def gen_staff_sweep():
    dur = 0.45
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.3
        freq = 320.0 - 140.0 * (t / dur)
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0)
        s = (sine * 0.6 + noise * 0.4) * env
        samples.append(s)
    return samples

# 8. AIR VORTEX (Resonant swirling tornado gale, 1.20s)
def gen_air_vortex():
    dur = 1.20
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.2
        # Swirling pitch modulation
        vortex_lfo = math.sin(2.0 * math.pi * 3.5 * t)
        freq = 180.0 + 70.0 * vortex_lfo
        sine = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0)
        s = (sine * 0.45 + noise * 0.55) * env
        samples.append(s)
    return samples

# 9. STAFF IMPACT (Solid wooden thud on flesh/armor, 0.25s)
def gen_staff_impact():
    dur = 0.25
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 28.0)
        # Wood resonance pitch (190Hz and 380Hz)
        wood = 0.7 * math.sin(2.0 * math.pi * 190.0 * t) + 0.3 * math.sin(2.0 * math.pi * 380.0 * t)
        click = (random.random() * 2.0 - 1.0) * math.exp(-t * 60.0)
        s = (wood * 0.75 + click * 0.4) * env
        samples.append(s)
    return samples

# Generate all 9 prototypes
write_wav("fire_jab.wav", gen_fire_jab())
write_wav("flame_sweep.wav", gen_flame_sweep())
write_wav("fire_jet.wav", gen_fire_jet())
write_wav("fire_impact.wav", gen_fire_impact())

write_wav("staff_thrust.wav", gen_staff_thrust())
write_wav("staff_spin.wav", gen_staff_spin())
write_wav("staff_sweep.wav", gen_staff_sweep())
write_wav("air_vortex.wav", gen_air_vortex())
write_wav("staff_impact.wav", gen_staff_impact())
print("All prototype audio files generated successfully.")
