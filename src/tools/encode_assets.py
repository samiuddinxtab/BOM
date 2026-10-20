#!/usr/bin/env python3
"""Encode binary assets into base64 parts that fit the GitHub API's
per-request payload ceiling.

The GitHub MCP integration passes file content as a JSON string, and its
transport caps the total request size (measured at roughly 200 KB). Two
constraints follow:

  1. Binary files cannot be sent directly — the transport UTF-8 encodes the
     string, corrupting any byte >= 0x80. Base64 is pure ASCII, so it is safe.
  2. A base64 blob for a large image is still too big for one request, so
     each blob is split into numbered parts that are concatenated on decode.

Layout produced:

    assets/img/hero-bag.webp.b64.001
    assets/img/hero-bag.webp.b64.002
    assets/fonts/archivo-400-normal-latin.woff2.b64.001

`tools/decode_assets.py` reassembles them.
"""
import base64
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, ".."))

# Stay well under the observed ~200 KB request ceiling.
PART_BYTES = 100_000
# Base64 lines are wrapped at 76 chars so the files stay diff-friendly.
LINE = 76


def encode_file(path, out_prefix):
    data = open(path, "rb").read()
    b64 = base64.b64encode(data).decode("ascii")
    lines = [b64[i:i + LINE] for i in range(0, len(b64), LINE)]
    blob = "\n".join(lines) + "\n"

    parts, offset, part, n = [], 0, 1, len(blob)
    while offset < n:
        chunk = blob[offset:offset + PART_BYTES]
        # Prefer a line boundary, but never drop or duplicate a character:
        # the parts must concatenate back to the original blob exactly.
        cut = chunk.rfind("\n")
        if cut > 0 and offset + cut + 1 < n:
            chunk = chunk[:cut + 1]
        p = f"{out_prefix}.{part:03d}"
        with open(p, "w", encoding="ascii") as f:
            f.write(chunk)
        parts.append(p)
        offset += len(chunk)
        part += 1
    return parts, len(data)


def main():
    targets = []
    for pat in ("assets/img/*.webp", "assets/fonts/*.woff2"):
        targets.extend(sorted(glob.glob(os.path.join(SRC, pat))))

    # Remove any previously generated blobs and parts.
    for old in glob.glob(os.path.join(SRC, "assets/*/*.b64")) + \
            glob.glob(os.path.join(SRC, "assets/*/*.b64.*")):
        os.remove(old)

    total_raw = total_enc = 0
    for t in targets:
        parts, raw = encode_file(t, t + ".b64")
        total_raw += raw
        total_enc += sum(os.path.getsize(p) for p in parts)
        print(f"  {os.path.relpath(t, SRC):<46s} {raw:>8d} b -> {len(parts)} part(s)")
    print(f"\nraw {total_raw // 1024} KB -> encoded {total_enc // 1024} KB "
          f"in {len(glob.glob(os.path.join(SRC, 'assets/*/*.b64.*')))} parts")


if __name__ == "__main__":
    main()
