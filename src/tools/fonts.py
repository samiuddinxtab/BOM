#!/usr/bin/env python3
"""Self-host the webfonts: download woff2 subsets and rewrite the CSS to local paths."""
import os
import re
import urllib.request

SRC = "/workspace/src/assets/fonts"
os.makedirs(SRC, exist_ok=True)

CSS = """/* Self-hosted webfonts — no third-party connection, no render-blocking CDN hop. */
"""

with open("/tmp/gf.css", encoding="utf-8") as f:
    raw = f.read()

blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", raw, re.S)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
seen = {}
out = []

for subset, block in blocks:
    if subset not in ("latin", "latin-ext"):
        continue
    url_m = re.search(r"url\((https://[^)]+)\)", block)
    if not url_m:
        continue
    url = url_m.group(1)
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    wt = re.search(r"font-weight:\s*([^;]+);", block).group(1).strip()
    st = re.search(r"font-style:\s*([^;]+);", block).group(1).strip()
    slug = f"{fam.lower().replace(' ', '-')}-{wt.replace(' ', '')}-{st}-{subset}.woff2"
    if slug not in seen:
        path = os.path.join(SRC, slug)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        seen[slug] = len(data)
        print(f"  {slug:52s} {len(data)//1024:>4d} KB")
    local = f"../fonts/{slug}"
    out.append(block.replace(url, local).replace("font-display: swap;", "font-display: swap;"))

CSS += "\n\n".join(out) + "\n"

with open("/workspace/src/assets/css/00_fonts.css", "w", encoding="utf-8") as f:
    f.write(CSS)

print(f"\n{len(seen)} files, {sum(seen.values())//1024} KB total")
