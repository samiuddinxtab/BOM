# KARKHANA — Strategy & Design Rationale

## 1. Market reality (researched, Oct 2026)

**Category:** India luggage & bags ≈ USD 4.3–4.8B (2025), CAGR ~10.8% to 2032.
Backpacks = 24.8% share of India bags market (largest product type). School bags 18.9% (resilient,
replacement-driven). West India 34.5% regional share; North India 28.7%.
Polyester = 39.6% of material mix — the default input for high-volume Indian bag manufacturing.

**Manufacturing geography (real):**
- **Bahadurgarh, Haryana (MIE Part A/B)** — India's densest bag-manufacturing cluster. Separators,
  zippers (Kwality Threads / MAX Zippers, est. 1984), hardware, lining, trims all local.
- Jalandhar & Ludhiana, Punjab — zippers, buckles, D-rings, trims.
- Erode / Tiruppur, TN — technical polyester, canvas, RPET.
- Export hubs: Nhava Sheva (Mumbai), Mundra, Kandla.

**Competitive set (all researched):** Optima Bags (Delhi NCR, 30 yrs, ISO/BSCI/Sedex),
Galaxy Bags, Bag Manufacturers Co. (Mumbai), Meghraj Exports (Jalandhar), Unileather,
Girlfriend Bag Factory (Delhi), and dozens of Jalandhar/Bahadurgarh exporters.

## 2. The strategic problem

Every competitor in this category ships the *same* website archetype:
stock product photos, a category grid, a MOQ table, a WhatsApp number. They sell price and lead
time. Result: the Indian bag sector is structurally squeezed — unorganised factories race to the
bottom on price, while brands that want *good* bags import from Vietnam/Turkey because they
do not believe an Indian factory can execute a design brief.

**The gap is not price. The gap is credibility expressed as specification.**

Nobody is showing the buyer the *engineering* of the product: GSM, denier, stitch density (SPI),
bar-tack specification, zipper brand, hardware pull-force, AQL level, tolerance on a seam, pattern
grading, and what a tech pack actually contains.

**Insight:** A bag is a manufactured object with tolerances, not a photo on a catalogue page.
A manufacturer that exposes its spec sheet *is* the credibility.

## 3. Positioning

> **KARKHANA** — a custom bag *works*, not a trading company.
> We brief like a design studio and build like a factory.

- Not "we make bags to your design." → "We will hand you a tech pack our machines can actually build."
- Not "MOQ from 100 pieces, call for price." → a live configurator that outputs a real spec card,
  a price band, and a MOQ/lead-time estimate.
- The buyer is a **founder, brand owner, institutional buyer, or sourcing manager** who needs to
  de-risk a production run. The site's job: make the risk legible.

**Tagline:** *Made to your spec. Built to survive the spec.*

## 4. Narrative architecture (7 acts)

1. **Promise** — hero: one bag, one hard light, a statement + 3 proof numbers.
2. **The gap** — "Most bag factories are not design partners." Honest positioning against the category.
3. **The range** — filterable catalogue, every card carrying a spec block.
4. **The method** — 8-step journey, brief → golden sample → bulk → dispatch. Sticky index.
5. **The works** — floor, machines, capacity, certifications, materials library.
6. **The proof** — QC protocol, AQL, third-party inspection welcome, export record.
7. **The ask** — a real RFQ form that mirrors the tech-pack structure (so the buyer's next
   step is structured, not a blank email).

## 5. Design system concept — "THE TECHNICAL ATELIER"

**Premise:** The visual language of a spec sheet (dimension lines, tick marks, monospace labels,
measured swatches) rendered with the material richness of a textile mill.

**Signature devices**
- **Saddle-stitch rule** — a dashed 2px line as the section divider. Reads as hand-stitched leather.
  Used at every section boundary. This is the site's recognisable motif.
- **Dimension callouts** — hairline rules with end ticks and monospace measurements, framing the
  hero product as an object with dimensions.
- **Material swatch chips** — real GSM/denier values, not vague descriptors.
- **Blueprint grid** — 1px grid overlay at 4% opacity on dark sections, evoking a cutting table.

**Colour**
| Token | Hex | Role |
|---|---|---|
| `--ink` | `#0D1014` | primary dark ground |
| `--ink-2` | `#161B22` | raised dark surfaces |
| `--paper` | `#F2EEE6` | light spec-sheet ground |
| `--paper-2` | `#E7E1D5` | kraft / secondary light |
| `--marigold` | `#E9A319` | primary accent — Indian dye reference (turmeric/marigold) |
| `--marigold-hi` | `#FFC155` | accent hover / on-dark text |
| `--indigo` | `#16264A` | secondary — dye-vat indigo, structural |
| `--madder` | `#B8402C` | signal / scarcity / alerts only |
| `--slate` | `#7C8590` | muted text, metadata |

**Type**
- Display — `Archivo` (700–800, tight tracking, industrial grotesque)
- Editorial accent — `Instrument Serif` (italic) for pull-quotes and section numerals
- Body — `Archivo` 400/500 at 1.65 line-height
- Spec/data — `IBM Plex Mono` 500, uppercase, 0.14em tracking, for every label, number, unit

**Grid:** 12-col, 1440 max, 32px gutter, asymmetric 7/5 and 8/4 splits. 8px baseline.
**Radius:** 2px (technical) / 999px (pill) only. Nothing in between — this is the discipline.
**Elevation:** borders and 1px hairlines, not shadows. One shadow only: the floating RFQ dock.

**Motion**
- Reveal: 18px rise + opacity, 620ms `cubic-bezier(.16,1,.3,1)`, 60ms stagger.
- Section numerals count up on enter.
- Hero: bag scales 1.06 → 1.0 with callouts drawing in.
- Marquee: capability tags, paused on hover, `prefers-reduced-motion` respected.
- All motion transform/opacity only.

## 6. Signature interactive — THE SPEC BUILDER (`customise.html`)

A live configurator, the site's proof-of-competence:
1. Choose a **base silhouette** (8 bags).
2. Choose **body fabric** → updates GSM, weight, water-resistance, price index, lead-time.
3. Choose **accent colourway** (Pantone-referenced) → live swatch.
4. Choose **branding method** (screen print / embroidery / woven label / metal badge / deboss) →
   updates setup cost and MOQ.
5. Choose **hardware finish** and **lining**.
6. **Live output:** a spec card (dimensions, litres, weight, SPI, zipper, hardware, fabric GSM),
   a **price band** (₹/pc at 500 / 1,000 / 5,000), **MOQ**, **lead time**, and **sample lead time**.

This is the strategic payload: it lets a buyer price and scope before ever emailing, and it
demonstrates manufacturing literacy — which is exactly the credibility gap identified in §2.

## 7. Information architecture

- `/` Home
- `/products.html` Catalogue — filter by category, sort, spec-bearing cards
- `/customise.html` The Spec Builder (signature)
- `/process.html` How it works — 8 steps, sticky index, QC gate detail
- `/works.html` The Works — facility, machinery, materials library, certifications
- `/industries.html` Who we build for — schools, colleges, corporates, D2C, exporters
- `/contact.html` Request a quote — structured RFQ mirroring the tech pack
- `/design-system.html` The design system, documented and live

## 8. Non-negotiables

- Mobile-first; breakpoints 640 / 900 / 1200 / 1440.
- WCAG AA contrast on every text/background pair.
- Every image has alt, width, height, lazy loading, LQIP.
- Keyboard-operable nav, filters, tabs, form.
- No fake 3D, no stock-photo humans, no generic "quality" claims without a measurable spec beside them.
