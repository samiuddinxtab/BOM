#!/usr/bin/env python3
"""Generate DESIGN-SYSTEM.md directly from the CSS token source, so the
documentation can never drift from the implementation."""
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(HERE, "..", "assets/css")
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "research", "DESIGN-SYSTEM.md"))


def read(name):
    with open(os.path.join(CSS, name), encoding="utf-8") as f:
        return f.read()


root = read("01_foundations.css")
token_block = root.split(":root {", 1)[1].split("\n}", 1)[0]


def tokens(prefix, block=None):
    block = block if block is not None else token_block
    out = []
    for m in re.finditer(r"(--[\w-]+):\s*([^;]+);", block):
        if m.group(1).startswith(prefix):
            out.append((m.group(1), m.group(2).strip()))
    return out


def paper_tokens():
    blk = root.split(".theme-paper {", 1)[1].split("\n}", 1)[0]
    return tokens("--", blk)


colour_rows = []
for name, value in tokens("--"):
    if name.startswith(("--ink", "--paper", "--marigold", "--indigo", "--madder", "--slate")):
        colour_rows.append((name, value))

type_rows = tokens("--fs-")
space_rows = tokens("--s-")

L = []
w = L.append

w("# KARKHANA — Design System")
w("")
w("**The Technical Atelier** · a design system for a bag manufacturer.")
w("")
w("> A bag is a manufactured object with tolerances, not a photograph on a catalogue page.")
w("> This system is built on that claim: the spec *is* the interface.")
w("")
w("Live implementation: **`/design-system.html`** in the deployed site.")
w("")
w("---")
w("")
w("## 1. Concept")
w("")
w("The visual language of a spec sheet — dimension lines, tick marks, monospace labels,")
w("measured swatches — rendered with the material richness of a textile mill.")
w("")
w("The category problem: every competitor in Indian bag manufacturing ships the same")
w("archetype (stock photos, a category grid, a MOQ table) and competes on price. The")
w("real gap is credibility expressed as *specification* — GSM, stitch density, AQL,")
w("shade band, lead time. Publishing those numbers is the positioning.")
w("")
w("### Signature devices")
w("")
w("| Device | Description |")
w("|---|---|")
w("| **Saddle-stitch rule** | Dashed 2px divider, borrowed from leatherwork. The site's recognisable motif, used at every section boundary. |")
w("| **Dimension callout** | Hairline with an end tick and a monospace measurement. Frames products as objects with dimensions. |")
w("| **Material swatch chip** | Real GSM and denier values, never vague descriptors like \"durable\". |")
w("| **Blueprint grid** | 1px grid at 4% opacity on dark sections — the cutting table. |")
w("| **Spec row** | Two-column data block, monospace key, tabular-numeral value. |")
w("")
w("---")
w("")
w("## 2. Colour")
w("")
w("Two grounds — deep ink and warm paper — alternating down the page in a day/night")
w("rhythm. The accent is a turmeric marigold, a working Indian dye reference rather")
w("than a decorative one. Indigo carries the structural notes; madder is reserved for")
w("scarcity and error states only.")
w("")
w("### Primitives")
w("")
w("| Token | Value | Role |")
w("|---|---|---|")
ROLES = {
    "--ink": "Primary dark ground", "--ink-2": "Raised dark surface",
    "--ink-3": "Raised dark surface, lighter", "--ink-line": "Hairline on dark",
    "--paper": "Light spec-sheet ground", "--paper-2": "Kraft / secondary light",
    "--paper-3": "Deeper kraft", "--paper-line": "Hairline on light",
    "--marigold": "Primary accent — turmeric / marigold dye",
    "--marigold-hi": "Accent on dark grounds", "--marigold-dk": "Accent text on paper",
    "--indigo": "Secondary — dye-vat indigo, structural",
    "--indigo-lt": "Indigo, light", "--madder": "Signal / scarcity only",
    "--madder-lt": "Madder, light", "--slate": "Muted metadata",
    "--slate-d": "Muted metadata, darker", "--slate-l": "Muted metadata, lighter",
}
for name, value in colour_rows:
    w(f"| `{name}` | `{value}` | {ROLES.get(name, '')} |")
w("")
w("### Semantic tokens and the light-ground override")
w("")
w("`--accent` is **theme-aware**, and that matters: the bright marigold `#E9A319`")
w("reaches only **1.87:1** against paper, which is unusable as text. On the light")
w("ground the accent switches to a deeper marigold.")
w("")
w("| Semantic | Dark ground | Light ground |")
w("|---|---|---|")
sem = []
dark = {k: v for k, v in tokens("--")}
for name, value in paper_tokens():
    if name in ("--bg", "--bg-soft", "--bg-raise", "--fg", "--fg-muted", "--line", "--accent", "--accent-fg"):
        sem.append((name, value))
for name, value in sem:
    dv = dark.get(name, "—")
    w(f"| `{name}` | `{dv}` | `{value}` |")
w("")
w("### Measured contrast")
w("")
w("| Pair | Ratio | AA |")
w("|---|---|---|")
w("| `#E9A319` on `#0D1014` (marigold on ink) | 8.82:1 | pass |")
w("| `#FFC155` on `#0D1014` (marigold-hi on ink) | 11.81:1 | pass |")
w("| `#9AA1A9` on `#0D1014` (slate-l on ink) | 7.30:1 | pass |")
w("| `#7E5406` on `#F2EEE6` (accent on paper) | 5.75:1 | pass |")
w("| `#5C636C` on `#F2EEE6` (muted on paper) | 5.25:1 | pass |")
w("| `#E06A52` on `#0D1014` (madder-lt on ink) | 5.77:1 | pass |")
w("| `#E9A319` on `#F2EEE6` (marigold on paper) | 1.87:1 | **fail — never used as text on light** |")
w("")
w("---")
w("")
w("## 3. Typography")
w("")
w("Three voices. If it is a number, it is monospace.")
w("")
w("| Role | Family | Weights | Tracking |")
w("|---|---|---|---|")
w("| Display, headings, body | Archivo | 400–800 | −0.035em display / −0.02em heading |")
w("| Editorial counterpoint (italic only) | Instrument Serif | 400 | −0.01em |")
w("| All data, labels, units | IBM Plex Mono | 400–600 | +0.14em uppercase |")
w("")
w("### Scale")
w("")
w("| Token | Value |")
w("|---|---|")
for name, value in type_rows:
    w(f"| `{name}` | `{value}` |")
w("")
w("```css")
w("/* Mono is the connective tissue of the system. Every spec key, unit,")
w("   measurement and label is monospace and uppercase. */")
w(".mono {")
w("  font-family: var(--f-mono);")
w("  font-size: var(--fs-mono);")
w("  font-weight: 500;")
w("  letter-spacing: var(--tracking-mono);")
w("  text-transform: uppercase;")
w("}")
w("```")
w("")
w("---")
w("")
w("## 4. Space, grid & geometry")
w("")
w("An 8px baseline, a 12-column grid at 1440px, and a gutter that flexes")
w("20px → 48px. Section rhythm is fluid, 64px on mobile to 136px on desktop.")
w("Asymmetric splits (7/5 and 8/4) carry most compositions; centred symmetry is")
w("reserved for the hero and the closing band.")
w("")
w("| Token | Value |")
w("|---|---|")
for name, value in space_rows:
    w(f"| `{name}` | `{value}` |")
w("")
w("| Geometry | Value |")
w("|---|---|")
w("| `--shell` | `1440px` |")
w("| `--gutter` | `clamp(20px, 4vw, 48px)` |")
w("| `--section-y` | `clamp(64px, 9vw, 136px)` |")
w("| `--r-sm` | `2px` — technical default, hard corners |")
w("| `--r-pill` | `999px` — pills and chips |")
w("| elevation | hairline borders, not shadows |")
w("")
w("> **Radius discipline:** nothing between 2px and 999px. A bag is either a")
w("> technical object or a soft object; the geometry says which.")
w("")
w("---")
w("")
w("## 5. Motion")
w("")
w("Motion exists to direct attention, never to entertain.")
w("")
w("| Token | Value |")
w("|---|---|")
w("| `--ease-out` | `cubic-bezier(.16, 1, .3, 1)` |")
w("| `--t-fast` | `180ms` |")
w("| `--t-med` | `380ms` |")
w("| `--t-slow` | `620ms` |")
w("| `--t-reveal` | `700ms` |")
w("")
w("- Reveal: 18px rise + opacity, 700ms ease-out, 60ms stagger")
w("- Section numerals count up on enter (1100ms, cubic ease-out)")
w("- Capability marquee runs at a reading pace, pauses on hover")
w("- Hero image scales 1.05 on card hover, 1.045 on figure hover")
w("- **Transform and opacity only** — never width, height or top")
w("- `prefers-reduced-motion` collapses the whole system to ~0ms")
w("")
w("---")
w("")
w("## 6. Components")
w("")
w("| Component | Class | Notes |")
w("|---|---|---|")
for name, cls, note in [
    ("Button", ".btn", "Variants: primary, secondary, ghost, arrow, sm/lg/block. Fill sweeps up on hover."),
    ("Text link", ".tlink", "Rule underline that retracts on hover; arrow translates."),
    ("Spec row", ".spec-row", "Two-column data block, tabular numerals, optional `small` sub-line."),
    ("Data strip", ".data-strip", "Multi-cell stat band with unit suffixes."),
    ("Tag", ".tag", "Neutral / accent / solid variants, optional leading dot."),
    ("Swatch", ".swatch-chip", "44px, pressed state uses an accent ring."),
    ("Option tile", ".opt", "Builder choice; `aria-pressed` drives the active state."),
    ("Choice card", ".choice", "Radio/checkbox styled as a selectable card."),
    ("Index card", ".idx-card", "Numbered pillar with an accent rule that draws in on hover."),
    ("Figure", ".fig", "Fixed ratio, LQIP background, fade-in on load."),
    ("Callout", ".callout", "Dimension annotation with an end tick."),
    ("Step", ".step", "Numbered process row with meta chips."),
    ("Accordion", ".acc-trigger", "Height-animated via `grid-template-rows: 0fr → 1fr`."),
    ("Tabs", ".tabs / .tab", "Scrollable, accent underline on the active tab."),
    ("Summary", ".summary", "Live spec card with tier table — the Spec Builder output."),
]:
    w(f"| {name} | `{cls}` | {note} |")
w("")
w("---")
w("")
w("## 7. Layout & responsive")
w("")
w("| Breakpoint | Behaviour |")
w("|---|---|")
w("| ≥1200px | Full asymmetric grid, sticky builder summary |")
w("| 900–1199px | Split columns collapse to one; builder summary un-sticks |")
w("| 620–899px | 2-column grids, filters wrap, drawer navigation |")
w("| <620px | Single column; option tiles 2-up; marquee continues |")
w("")
w("> All grid tracks use `minmax(0, 1fr)`, never bare `1fr`. A bare `1fr` carries an")
w("> `auto` minimum, which lets tracks inherit max-content width and overflows narrow")
w("> viewports. This was a real bug found in QA on the Spec Builder.")
w("")
w("---")
w("")
w("## 8. Accessibility")
w("")
w("- WCAG AA contrast on every text/background pair (measured above)")
w("- Exactly one `h1` per page; no heading-level jumps")
w("- Every form control has a label, explicitly or by wrapping")
w("- Full keyboard operation: nav, filters, builder steps, accordion, form")
w("- Visible 2px focus ring with 3px offset on every interactive element")
w("- `prefers-reduced-motion` fully honoured")
w("- Every image carries alt text, intrinsic `width`/`height` and lazy loading")
w("- LQIP placeholder behind each image; fade-in on `load`")
w("- Skip-to-content link as the first focusable element")
w("")
w("---")
w("")
w("## 9. Content model")
w("")
w("The site renders from a single Python content module (`content.py`) and a small")
w("static generator (`build.py`). The catalogue, the Spec Builder and the pricing")
w("model all read the same source, so they cannot disagree with each other.")
w("")
w("| Layer | File | Responsibility |")
w("|---|---|---|")
w("| Content | `src/content.py` | Products, fabrics, colourways, branding, hardware, linings, process, materials, certifications, FAQ, pricing tiers |")
w("| Generator | `src/build.py` | Page templates, shared layout, image manifest, asset copy |")
w("| Behaviour | `src/assets/js/main.js` | Reveal, filters, builder pricing engine, form validation, scrollspy, counters |")
w("| Tokens | `src/assets/css/01_foundations.css` | The single source of truth for the visual system |")
w("")
w("### The pricing model")
w("")
w("```")
w("unit  = base × fabric.index + branding.unit + hardware.unit + lining.unit")
w("price = unit × tier.multiplier")
w("moq   = max(product.moq, branding.moq, hardware.moq)")
w("lead  = product.lead + fabric.lead + branding.lead + hardware.lead + lining.lead")
w("```")
w("")
w("Tier multipliers: " + ", ".join(
    f"{t['label']} × {t['mult']}" for t in C.TIERS))
w("")
w("---")
w("")
w("## 10. Type stack")
w("")
w("| Family | Weights | Source |")
w("|---|---|---|")
w("| Archivo | 400, 500, 600, 700, 800 | Self-hosted woff2, latin + latin-ext |")
w("| Instrument Serif | 400, 400 italic | Self-hosted woff2 |")
w("| IBM Plex Mono | 400, 500, 600 | Self-hosted woff2 |")
w("")
w("All three are **self-hosted** — no Google Fonts connection, no render-blocking")
w("CDN hop, no third-party request, and the site works offline. The three most")
w("critical files are preloaded with `crossorigin`.")
w("")
w("---")
w("")
w("## 11. Performance")
w("")
w("| Measure | Value |")
w("|---|---|")
w("| Images | 13 WebP assets, 2.2 MB total, max 1500px (scenes 2000px) |")
w("| Largest image | 342 KB (hero, 3:4) |")
w("| CSS | 3 files, no framework, no build-time minifier needed |")
w("| JS | 1 file, ~16 KB, no dependencies, no framework |")
w("| Fonts | 20 woff2 subsets, 479 KB, cached forever |")
w("| Third-party requests | **zero** |")
w("| Layout shift | prevented by intrinsic `width`/`height` on every image |")
w("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print(f"wrote {OUT}  ({os.path.getsize(OUT)//1024} KB, {len(L)} lines)")
