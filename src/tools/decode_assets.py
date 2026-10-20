#!/usr/bin/env python3
"""Decode base64-encoded binary assets back into their real files.

Why this exists
---------------
The GitHub API integration available here passes file content as a JSON string
and UTF-8 encodes it server-side, and caps the request payload at roughly
200 KB. Binary assets (WebP images, WOFF2 fonts) therefore cannot be pushed
directly — a byte >= 0x80 expands to two bytes and the file is silently
corrupted — and a large base64 blob does not fit in one request either.

So the repository stores each binary as base64, split into numbered parts:

    assets/img/hero-bag.webp.b64.001
    assets/img/hero-bag.webp.b64.002

This script concatenates the parts, decodes them, and writes the real file
next to them. Every decoded file is verified with a SHA-256 comparison
against its source on each run.

    python3 tools/decode_assets.py     # materialise assets/
    python3 build.py                   # then build dist/ (decodes automatically)
"""
import base64
import glob
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(SRC, "assets")
PART_RE = re.compile(r"^(?P<target>.+)\.b64\.(?P<num>\d{3})$")


def groups():
    """Map target path -> ordered list of part files."""
    out = {}
    for path in glob.glob(os.path.join(ASSETS, "**", "*.b64.*"), recursive=True):
        m = PART_RE.match(os.path.basename(path))
        if not m:
            continue
        target = os.path.join(os.path.dirname(path), m.group("target"))
        out.setdefault(target, []).append((int(m.group("num")), path))
    # Single-file blobs (no numeric suffix) are supported too.
    for path in glob.glob(os.path.join(ASSETS, "**", "*.b64"), recursive=True):
        if PART_RE.match(os.path.basename(path)):
            continue
        out.setdefault(path, []).append((0, path))
    return {k: [p for _, p in sorted(v)] for k, v in out.items()}


def decode_all(force=False, quiet=False):
    written, skipped = [], []
    for target, parts in sorted(groups().items()):
        if os.path.exists(target) and not force:
            skipped.append(target)
            continue
        blob = "".join(open(p, "r", encoding="ascii").read() for p in parts)
        data = base64.b64decode(blob)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
        written.append(target)
        if not quiet:
            digest = hashlib.sha256(data).hexdigest()[:12]
            print(f"  decoded {os.path.relpath(target, SRC):<44s} "
                  f"{len(data):>8d} b  sha256:{digest}")
    return written, skipped


def integrity_report():
    """Compare each decoded file against its .b64 source."""
    bad = []
    for target, parts in groups().items():
        if not os.path.exists(target):
            continue
        blob = "".join(open(p, "r", encoding="ascii").read() for p in parts)
        if base64.b64decode(blob) != open(target, "rb").read():
            bad.append(target)
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
