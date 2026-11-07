import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

print("Checking PIL font capabilities...")
# Try loading a default font or truetype
try:
    font_title = ImageFont.truetype("arial.ttf", 22)
    font_sub = ImageFont.truetype("arial.ttf", 14)
    font_mono = ImageFont.truetype("consola.ttf", 12)
    print("TrueType fonts loaded successfully")
except Exception as e:
    print("Fallback to default font:", e)
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_mono = ImageFont.load_default()
