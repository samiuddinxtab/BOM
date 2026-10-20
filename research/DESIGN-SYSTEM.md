# KARKHANA — Design System

**The Technical Atelier** · a design system for a bag manufacturer.

> A bag is a manufactured object with tolerances, not a photograph on a catalogue page.
> This system is built on that claim: the spec *is* the interface.

Live implementation: **`/design-system.html`** in the deployed site.

---

## 1. Concept

The visual language of a spec sheet — dimension lines, tick marks, monospace labels,
measured swatches — rendered with the material richness of a textile mill.

The category problem: every competitor in Indian bag manufacturing ships the same
archetype (stock photos, a category grid, a MOQ table) and competes on price. The
real gap is credibility expressed as *specification* — GSM, stitch density, AQL,
shade band, lead time. Publishing those numbers is the positioning.

### Signature devices

| Device | Description |
|---|---|
| **Saddle-stitch rule** | Dashed 2px divider, borrowed from leatherwork. The site's recognisable motif, used at every section boundary. |
| **Dimension callout** | Hairline with an end tick and a monospace measurement. Frames products as objects with dimensions. |
| **Material swatch chip** | Real GSM and denier values, never vague descriptors like "durable". |
| **Blueprint grid** | 1px grid at 4% opacity on dark sections — the cutting table. |
| **Spec row** | Two-column data block, monospace key, tabular-numeral value. |

---

## 2. Colour

Two grounds — deep ink and warm paper — alternating down the page in a day/night
rhythm. The accent is a turmeric marigold, a working Indian dye reference rather
than a decorative one. Indigo carries the structural notes; madder is reserved for
scarcity and error states only.

### Primitives

| Token | Value | Role |
|---|---|---|
| `--ink` | `#0D1014` | Primary dark ground |
| `--ink-2` | `#161B22` | Raised dark surface |
| `--ink-3` | `#1F252D` | Raised dark surface, lighter |
| `--ink-line` | `#2A323C` | Hairline on dark |
| `--paper` | `#F2EEE6` | Light spec-sheet ground |
| `--paper-2` | `#E7E1D5` | Kraft / secondary light |
| `--paper-3` | `#DAD3C4` | Deeper kraft |
| `--paper-line` | `#D5CDBC` | Hairline on light |
| `--marigold` | `#E9A319` | Primary accent — turmeric / marigold dye |
| `--marigold-hi` | `#FFC155` | Accent on dark grounds |
| `--marigold-dk` | `#B97B0A` | Accent text on paper |
| `--indigo` | `#16264A` | Secondary — dye-vat indigo, structural |
| `--indigo-lt` | `#2C4374` | Indigo, light |
| `--madder` | `#B8402C` | Signal / scarcity only |
| `--madder-lt` | `#E06A52` | Madder, light |
| `--slate` | `#7C8590` | Muted metadata |
| `--slate-d` | `#545C66` | Muted metadata, darker |
| `--slate-l` | `#9AA1A9` | Muted metadata, lighter |

### Semantic tokens and the light-ground override

`--accent` is **theme-aware**, and that matters: the bright marigold `#E9A319`
reaches only **1.87:1** against paper, which is unusable as text. On the light
ground the accent switches to a deeper marigold.

| Semantic | Dark ground | Light ground |
|---|---|---|
| `--bg` | `var(--ink)` | `var(--paper)` |
| `--bg-soft` | `var(--ink-2)` | `var(--paper-2)` |
| `--bg-raise` | `var(--ink-3)` | `#FBF9F4` |
| `--fg` | `#EDE9E1` | `#171B20` |
| `--fg-muted` | `var(--slate-l)` | `#5C636C` |
| `--line` | `var(--ink-line)` | `var(--paper-line)` |
| `--accent` | `var(--marigold)` | `#7E5406` |
| `--accent-fg` | `var(--ink)` | `#171B20` |

### Measured contrast

| Pair | Ratio | AA |
|---|---|---|
| `#E9A319` on `#0D1014` (marigold on ink) | 8.82:1 | pass |
| `#FFC155` on `#0D1014` (marigold-hi on ink) | 11.81:1 | pass |
| `#9AA1A9` on `#0D1014` (slate-l on ink) | 7.30:1 | pass |
| `#7E5406` on `#F2EEE6` (accent on paper) | 5.75:1 | pass |
| `#5C636C` on `#F2EEE6` (muted on paper) | 5.25:1 | pass |
| `#E06A52` on `#0D1014` (madder-lt on ink) | 5.77:1 | pass |
| `#E9A319` on `#F2EEE6` (marigold on paper) | 1.87:1 | **fail — never used as text on light** |

---

## 3. Typography

Three voices. If it is a number, it is monospace.

| Role | Family | Weights | Tracking |
|---|---|---|---|
| Display, headings, body | Archivo | 400–800 | −0.035em display / −0.02em heading |
| Editorial counterpoint (italic only) | Instrument Serif | 400 | −0.01em |
| All data, labels, units | IBM Plex Mono | 400–600 | +0.14em uppercase |

### Scale

| Token | Value |
|---|---|
| `--fs-display-xl` | `clamp(3.1rem, 8.6vw, 8.25rem)` |
| `--fs-display-l` | `clamp(2.5rem, 5.8vw, 5rem)` |
| `--fs-display-m` | `clamp(1.95rem, 3.9vw, 3.35rem)` |
| `--fs-h2` | `clamp(1.7rem, 3.1vw, 2.85rem)` |
| `--fs-h3` | `clamp(1.2rem, 1.9vw, 1.7rem)` |
| `--fs-h4` | `clamp(1.02rem, 1.3vw, 1.16rem)` |
| `--fs-lead` | `clamp(1.05rem, 1.35vw, 1.3rem)` |
| `--fs-body` | `1.03125rem` |
| `--fs-sm` | `0.9375rem` |
| `--fs-xs` | `0.875rem` |
| `--fs-mono` | `0.765rem` |
| `--fs-mono-lg` | `0.875rem` |

```css
/* Mono is the connective tissue of the system. Every spec key, unit,
   measurement and label is monospace and uppercase. */
.mono {
  font-family: var(--f-mono);
  font-size: var(--fs-mono);
  font-weight: 500;
  letter-spacing: var(--tracking-mono);
  text-transform: uppercase;
}
```

---

## 4. Space, grid & geometry

An 8px baseline, a 12-column grid at 1440px, and a gutter that flexes
20px → 48px. Section rhythm is fluid, 64px on mobile to 136px on desktop.
Asymmetric splits (7/5 and 8/4) carry most compositions; centred symmetry is
reserved for the hero and the closing band.

| Token | Value |
|---|---|
| `--s-1` | `4px` |
| `--s-2` | `8px` |
| `--s-3` | `12px` |
| `--s-4` | `16px` |
| `--s-5` | `24px` |
| `--s-6` | `32px` |
| `--s-7` | `40px` |
| `--s-8` | `48px` |
| `--s-9` | `64px` |
| `--s-10` | `80px` |
| `--s-11` | `104px` |
| `--s-12` | `136px` |
| `--s-13` | `176px` |

| Geometry | Value |
|---|---|
| `--shell` | `1440px` |
| `--gutter` | `clamp(20px, 4vw, 48px)` |
| `--section-y` | `clamp(64px, 9vw, 136px)` |
| `--r-sm` | `2px` — technical default, hard corners |
| `--r-pill` | `999px` — pills and chips |
| elevation | hairline borders, not shadows |

> **Radius discipline:** nothing between 2px and 999px. A bag is either a
> technical object or a soft object; the geometry says which.

---

## 5. Motion

Motion exists to direct attention, never to entertain.

| Token | Value |
|---|---|
| `--ease-out` | `cubic-bezier(.16, 1, .3, 1)` |
| `--t-fast` | `180ms` |
| `--t-med` | `380ms` |
| `--t-slow` | `620ms` |
| `--t-reveal` | `700ms` |

- Reveal: 18px rise + opacity, 700ms ease-out, 60ms stagger
- Section numerals count up on enter (1100ms, cubic ease-out)
- Capability marquee runs at a reading pace, pauses on hover
- Hero image scales 1.05 on card hover, 1.045 on figure hover
- **Transform and opacity only** — never width, height or top
- `prefers-reduced-motion` collapses the whole system to ~0ms

---

## 6. Components

| Component | Class | Notes |
|---|---|---|
| Button | `.btn` | Variants: primary, secondary, ghost, arrow, sm/lg/block. Fill sweeps up on hover. |
| Text link | `.tlink` | Rule underline that retracts on hover; arrow translates. |
| Spec row | `.spec-row` | Two-column data block, tabular numerals, optional `small` sub-line. |
| Data strip | `.data-strip` | Multi-cell stat band with unit suffixes. |
| Tag | `.tag` | Neutral / accent / solid variants, optional leading dot. |
| Swatch | `.swatch-chip` | 44px, pressed state uses an accent ring. |
| Option tile | `.opt` | Builder choice; `aria-pressed` drives the active state. |
| Choice card | `.choice` | Radio/checkbox styled as a selectable card. |
| Index card | `.idx-card` | Numbered pillar with an accent rule that draws in on hover. |
| Figure | `.fig` | Fixed ratio, LQIP background, fade-in on load. |
| Callout | `.callout` | Dimension annotation with an end tick. |
| Step | `.step` | Numbered process row with meta chips. |
| Accordion | `.acc-trigger` | Height-animated via `grid-template-rows: 0fr → 1fr`. |
| Tabs | `.tabs / .tab` | Scrollable, accent underline on the active tab. |
| Summary | `.summary` | Live spec card with tier table — the Spec Builder output. |

---

## 7. Layout & responsive

| Breakpoint | Behaviour |
|---|---|
| ≥1200px | Full asymmetric grid, sticky builder summary |
| 900–1199px | Split columns collapse to one; builder summary un-sticks |
| 620–899px | 2-column grids, filters wrap, drawer navigation |
| <620px | Single column; option tiles 2-up; marquee continues |

> All grid tracks use `minmax(0, 1fr)`, never bare `1fr`. A bare `1fr` carries an
> `auto` minimum, which lets tracks inherit max-content width and overflows narrow
> viewports. This was a real bug found in QA on the Spec Builder.

---

## 8. Accessibility

- WCAG AA contrast on every text/background pair (measured above)
- Exactly one `h1` per page; no heading-level jumps
- Every form control has a label, explicitly or by wrapping
- Full keyboard operation: nav, filters, builder steps, accordion, form
- Visible 2px focus ring with 3px offset on every interactive element
- `prefers-reduced-motion` fully honoured
- Every image carries alt text, intrinsic `width`/`height` and lazy loading
- LQIP placeholder behind each image; fade-in on `load`
- Skip-to-content link as the first focusable element

---

## 9. Content model

The site renders from a single Python content module (`content.py`) and a small
static generator (`build.py`). The catalogue, the Spec Builder and the pricing
model all read the same source, so they cannot disagree with each other.

| Layer | File | Responsibility |
|---|---|---|
| Content | `src/content.py` | Products, fabrics, colourways, branding, hardware, linings, process, materials, certifications, FAQ, pricing tiers |
| Generator | `src/build.py` | Page templates, shared layout, image manifest, asset copy |
| Behaviour | `src/assets/js/main.js` | Reveal, filters, builder pricing engine, form validation, scrollspy, counters |
| Tokens | `src/assets/css/01_foundations.css` | The single source of truth for the visual system |

### The pricing model

```
unit  = base × fabric.index + branding.unit + hardware.unit + lining.unit
price = unit × tier.multiplier
moq   = max(product.moq, branding.moq, hardware.moq)
lead  = product.lead + fabric.lead + branding.lead + hardware.lead + lining.lead
```

Tier multipliers: 100 × 1.18, 300 × 1.1, 500 × 1.0, 1,000 × 0.92, 5,000 × 0.8, 10,000 × 0.72

---

## 10. Type stack

| Family | Weights | Source |
|---|---|---|
| Archivo | 400, 500, 600, 700, 800 | Self-hosted woff2, latin + latin-ext |
| Instrument Serif | 400, 400 italic | Self-hosted woff2 |
| IBM Plex Mono | 400, 500, 600 | Self-hosted woff2 |

All three are **self-hosted** — no Google Fonts connection, no render-blocking
CDN hop, no third-party request, and the site works offline. The three most
critical files are preloaded with `crossorigin`.

---

## 11. Performance

| Measure | Value |
|---|---|
| Images | 13 WebP assets, 2.2 MB total, max 1500px (scenes 2000px) |
| Largest image | 342 KB (hero, 3:4) |
| CSS | 3 files, no framework, no build-time minifier needed |
| JS | 1 file, ~16 KB, no dependencies, no framework |
| Fonts | 20 woff2 subsets, 479 KB, cached forever |
| Third-party requests | **zero** |
| Layout shift | prevented by intrinsic `width`/`height` on every image |
