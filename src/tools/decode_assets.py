#!/usr/bin/env python3
"""Decode base64-encoded binary assets back into their real files.

Why this exists
---------------
The GitHub MCP tools used to publish this project pass file content as a JSON
string and UTF-8 encode it server-side. That makes binary assets (WebP
images, WOFF2 fonts) impossible to push directly — a byte >= 0x80 expands to
two bytes and the file is silently corrupted.

Base64 is pure ASCII, so it survives that transport byte-for-byte. The real
assets are therefore committed as `<name>.b64` and materialised locally by this
script. The decoded files are gitignored — the repository stays source-only
and reproducible:

    python3 tools/decode_assets.py     # materialise assets/
    python3 build.py                   # then build dist/

Both steps are chained automatically by build.py.
"""
import base64
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(SRC, "assets")
SUFFIX = ".b64"


def targets():
    """Every <file>.b64 in assets/, paired with the file it produces."""
    for root, _dirs, files in os.walk(ASSETS):
        for name in sorted(files):
            if name.endswith(SUFFIX):
                full = os.path.join(root, name)
                yield full, full[: -len(SUFFIX)]


def decode_all(force=False, quiet=False):
    written, skipped, changed = [], [], []
    for enc, out in targets():
        if os.path.exists(out) and not force:
            skipped.append(out)
            continue
        with open(enc, "r", encoding="ascii") as f:
            raw = f.read()
        data = base64.b64decode(raw)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as f:
            f.write(data)
        written.append(out)
        digest = hashlib.sha256(data).hexdigest()[:12]
        if not quiet:
            print(f"  decoded {os.path.relpath(out, SRC):<44s} {len(data):>8d} b  sha256:{digest}")
    return written, skipped


def integrity_report():
    """Compare each decoded file against its .b64 source."""
    bad = []
    for enc, out in targets():
        if not os.path.exists(out):
            continue
        with open(enc, "r", encoding="ascii") as f:
            expected = base64.b64decode(f.read())
        with open(out, "rb") as f:
            actual = f.read()
        if expected != actual:
            bad.append(out)
    return bad


if __name__ == "__main__":
    force = "--force" in sys.argv
    w, s = decode_all(force=force)
    if not w and not s:
        print("no encoded assets found")
    else:
        print(f"\n{len(w)} decoded, {len(s)} already present")
    bad = integrity_report()
    if bad:
        print("INTEGRITY FAILURE:")
        for b in bad:
            print("  ", b)
        sys.exit(1)
    print("integrity: all decoded assets match their source")
