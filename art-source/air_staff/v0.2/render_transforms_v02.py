import os
import math
from PIL import Image, ImageDraw

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff\v0.2"

W2, H2 = 1000, 600
img2 = Image.new("RGBA", (W2, H2), (24, 26, 32, 255))
draw2 = ImageDraw.Draw(img2)

draw2.text((40, 25), "AIR STAFF — ITEM DISPLAY TRANSFORMS MATRIX v0.2 (1.21.1)", fill=(240, 240, 245, 255))
draw2.text((40, 50), "Nama Slot Standar: thirdperson_righthand, thirdperson_lefthand, firstperson, gui, ground, fixed", fill=(140, 150, 170, 255))
draw2.text((40, 70), "Catatan Skala: Ukuran visual dalam game dikontrol oleh matriks scale; bukan ukuran meter statis.", fill=(210, 175, 100, 255))

panels = [
    {
        "title": "thirdperson_righthand",
        "rect": (40, 95, 480, 320),
        "rot": "[0, -90, 55]",
        "trans": "[0.0, 4.0, 0.5]",
        "scale": "[0.85, 0.85, 0.85]",
        "desc": "Digenggam di poros balutan tengah, kemiringan 55 deg ke belakang. Skala 0.85x.",
        "angle": 55
    },
    {
        "title": "firstperson_righthand",
        "rect": (510, 95, 950, 320),
        "rot": "[0, -90, 25]",
        "trans": "[1.13, 3.2, 1.13]",
        "scale": "[0.68, 0.68, 0.68]",
        "desc": "Tongkat condong 25 deg di tepi kanan layar agar tidak menghalangi crosshair pandangan.",
        "angle": 25
    },
    {
        "title": "gui (Inventory / Hotbar)",
        "rect": (40, 340, 480, 565),
        "rot": "[0, 0, -45]",
        "trans": "[0.0, 0.0, 0.0]",
        "scale": "[0.55, 0.55, 0.55]",
        "desc": "Miring 45 deg diagonal dari kiri atas ke kanan bawah standar tampilan GUI senjata vanilla.",
        "angle": -45
    },
    {
        "title": "ground / fixed",
        "rect": (510, 340, 950, 565),
        "rot": "[0, 0, 0]",
        "trans": "[0.0, 3.0, 0.0]",
        "scale": "[0.5, 0.5, 0.5]",
        "desc": "Jatuh tegak lurus di atas permukaan blok tanah, ujung bawah bertumpu rapi.",
        "angle": 0
    }
]

for p in panels:
    x0, y0, x1, y1 = p["rect"]
    draw2.rectangle([x0, y0, x1, y1], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
    draw2.text((x0 + 15, y0 + 15), p["title"].upper(), fill=(240, 210, 120, 255))
    
    mcx = x0 + 80
    mcy = y0 + 130
    rad = math.radians(p["angle"] + 90)
    slen = 60
    sx0 = mcx - slen * math.cos(rad)
    sy0 = mcy - slen * math.sin(rad)
    sx1 = mcx + slen * math.cos(rad)
    sy1 = mcy + slen * math.sin(rad)
    
    draw2.line([(sx0, sy0), (sx1, sy1)], fill=(166, 114, 68, 255), width=6)
    gx0 = mcx - 12 * math.cos(rad)
    gy0 = mcy - 12 * math.sin(rad)
    gx1 = mcx + 12 * math.cos(rad)
    gy1 = mcy + 12 * math.sin(rad)
    draw2.line([(gx0, gy0), (gx1, gy1)], fill=(234, 230, 223, 255), width=8)
    draw2.ellipse([(sx0-4, sy0-4), (sx0+4, sy0+4)], fill=(67, 48, 34, 255))
    draw2.ellipse([(sx1-4, sy1-4), (sx1+4, sy1+4)], fill=(67, 48, 34, 255))
    
    draw2.text((x0 + 170, y0 + 45), f"Rotation:    {p['rot']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 170, y0 + 70), f"Translation: {p['trans']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 170, y0 + 95), f"Scale:       {p['scale']}", fill=(180, 190, 210, 255))
    
    draw2.text((x0 + 170, y0 + 135), "Hasil Visual:", fill=(140, 150, 170, 255))
    words = p["desc"].split(" ")
    line1 = ""
    line2 = ""
    for w in words:
        if len(line1 + " " + w) < 38:
            line1 += (" " if line1 else "") + w
        else:
            line2 += (" " if line2 else "") + w
    draw2.text((x0 + 170, y0 + 158), line1, fill=(220, 225, 235, 255))
    if line2:
        draw2.text((x0 + 170, y0 + 180), line2, fill=(220, 225, 235, 255))

preview_trans_path = os.path.join(out_dir, "preview_transforms_v02.png")
img2.save(preview_trans_path, "PNG")
print("Saved revised transforms preview render to:", preview_trans_path)
