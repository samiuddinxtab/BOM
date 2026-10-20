#!/usr/bin/env python3
"""Optimize generated raw art into web-ready WebP + LQIP placeholders."""
import base64
import io
import json
import os
from PIL import Image

SRC = "/workspace/site/assets/img"
OUT = "/workspace/src/assets/img"
os.makedirs(OUT, exist_ok=True)

# name -> max width
PLAN = {
    "school-backpack": 1500, "college-backpack": 1500, "laptop-backpack": 1500,
    "file-bag": 1500, "duffle-bag": 1500, "trolley-bag": 1500,
    "travel-backpack": 1500, "corporate-totes": 1500, "material-macro": 1500,
    "hardware-macro": 1100, "factory-floor": 2000, "design-studio": 2000,
    "hero-bag": 1400,
}

manifest = {}
for name, maxw in PLAN.items():
    raw = None
    for ext in (".raw", ".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(SRC, name + ext)
        if os.path.exists(p):
            raw = p
            break
    if not raw:
        print("MISSING", name)
        continue

    im = Image.open(raw).convert("RGB")
    if im.width > maxw:
        h = round(im.height * maxw / im.width)
        im = im.resize((maxw, h), Image.LANCZOS)
    w, h = im.size

    webp_path = os.path.join(OUT, name + ".webp")
    im.save(webp_path, "WEBP", quality=82, method=6)

    # tiny LQIP
    t = im.copy()
    t.thumbnail((28, 28), Image.LANCZOS)
    buf = io.BytesIO()
    t.save(buf, "WEBP", quality=30)
    lqip = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

    manifest[name] = {
        "src": f"assets/img/{name}.webp",
        "w": w, "h": h,
        "lqip": lqip,
        "bytes": os.path.getsize(webp_path),
    }
    print(f"{name:18s} {w}x{h}  {os.path.getsize(webp_path)//1024:>4d} KB")

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print("\nTotal:", sum(v["bytes"] for v in manifest.values()) // 1024, "KB")
