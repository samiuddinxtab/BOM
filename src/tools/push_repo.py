#!/usr/bin/env python3
"""Push the project to a GitHub repository through the MCP push_files tool.

Text files are pushed as-is. Binary assets are pushed in their base64 (.b64)
form, which is the only representation that survives the API's UTF-8 string
transport intact.

Usage:
    python3 tools/push_repo.py --owner <login> --repo <name> [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TMP = os.path.join(ROOT, "research", "push_tmp")

TEXT_FILES = [
    ".gitignore",
    "README.md",
    "deploy/pages.yml",
    "research/strategy.md",
    "research/DESIGN-SYSTEM.md",
    "src/content.py",
    "src/build.py",
    "src/assets/css/00_fonts.css",
    "src/assets/css/01_foundations.css",
    "src/assets/css/02_components.css",
    "src/assets/css/03_pages.css",
    "src/assets/js/main.js",
    "src/assets/img/manifest.json",
    "src/assets/img/favicon.svg",
    "src/tools/decode_assets.py",
    "src/tools/optimize.py",
    "src/tools/fonts.py",
    "src/tools/shoot.py",
    "src/tools/overflow.py",
    "src/tools/qa.py",
    "src/tools/dsdoc.py",
    "src/tools/encode_assets.py",
    "src/tools/push_repo.py",
]

# Every base64 part, wherever it lives. The API caps the request payload at
# roughly 200 KB, so batches are cut well below that.
PARTS = sorted(
    [f"src/assets/{d}/{n}" for d in ("img", "fonts")
     for n in os.listdir(os.path.join(ROOT, "src/assets", d))
     if ".b64." in n],
    key=lambda p: (p.split("/")[2], p),
)

# Measured ceiling of the connector's request payload is ~200 KB; stay well
# under it so no single call is rejected.
MAX_PAYLOAD = 150_000


def batches():
    """Yield (label, [paths]) batches, keeping each payload under the cap."""
    chunk, size = [], 0
    for p in TEXT_FILES:
        s = os.path.getsize(os.path.join(ROOT, p))
        if chunk and size + s > MAX_PAYLOAD:
            yield "text", chunk
            chunk, size = [], 0
        chunk.append(p)
        size += s
    if chunk:
        yield "text", chunk

    chunk, size = [], 0
    for p in PARTS:
        s = os.path.getsize(os.path.join(ROOT, p))
        if chunk and size + s > MAX_PAYLOAD:
            yield "assets", chunk
            chunk, size = [], 0
        chunk.append(p)
        size += s
    if chunk:
        yield "assets", chunk


def local_blob_sha(path):
    return subprocess.run(
        ["git", "hash-object", os.path.join(ROOT, path)],
        capture_output=True, text=True, check=True).stdout.strip()


def push(owner, repo, branch, label, paths, dry=False):
    files = []
    for p in paths:
        with open(os.path.join(ROOT, p), "r", encoding="utf-8") as f:
            files.append({"path": p, "content": f.read()})
    args = {
        "owner": owner, "repo": repo, "branch": branch,
        "message": f"Add {label}: {paths[0]}" + (f" + {len(paths)-1} more" if len(paths) > 1 else ""),
        "files": files,
    }
    os.makedirs(TMP, exist_ok=True)
    af = os.path.join(TMP, "args.json")
    with open(af, "w", encoding="utf-8") as f:
        json.dump(args, f, ensure_ascii=False)
    size = os.path.getsize(af)
    if dry:
        print(f"  [dry] {label:6s} {len(files)} file(s)  {size//1024:>5d} KB payload")
        return True
    r = subprocess.run(
        ["mcode-tools", "connector", "call", "connector__github__push_files",
         "--args-file", af],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FAIL {label} {paths[0]}: {r.stderr[:300]}")
        return False
    try:
        out = json.loads(r.stdout)
        payload = json.loads(out[0]["text"]) if isinstance(out, list) else out
        sha = payload.get("commit", {}).get("sha", "?")
    except Exception:
        sha = "?"
    print(f"  ok   {label:6s} {len(files)} file(s)  {size//1024:>5d} KB  commit {sha[:10]}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    print(f"pushing → {a.owner}/{a.repo}@{a.branch}")
    all_paths = []
    for label, paths in batches():
        if not paths:
            continue
        if not push(a.owner, a.repo, a.branch, label, paths, a.dry_run):
            sys.exit(1)
        all_paths.extend(paths)
        if not a.dry_run:
            time.sleep(0.4)

    print(f"\ntotal files pushed: {len(all_paths)}")
    with open(os.path.join(ROOT, "research", "pushed_files.json"), "w") as f:
        json.dump({p: local_blob_sha(p) for p in all_paths}, f, indent=1)
    print("local blob SHAs written to research/pushed_files.json")


if __name__ == "__main__":
    main()
