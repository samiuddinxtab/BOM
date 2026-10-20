#!/usr/bin/env python3
"""KARKHANA static site generator.

Source of truth: content.py.  Output: ../dist  (a flat, deployable static site).
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = HERE
DIST = os.path.abspath(os.path.join(HERE, "..", "dist"))

MANIFEST = json.load(open(os.path.join(SRC, "assets/img/manifest.json")))

# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
ICONS = {
    "school": '<path d="M22 10L12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/><path d="M22 10v6"/>',
    "college": '<path d="M3 21h18"/><path d="M5 21V8l7-4 7 4v13"/><path d="M10 12h4"/><path d="M10 16h4"/>',
    "corp": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M2 13h20"/>',
    "dtc": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "export": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18Z"/>',
    "promo": '<rect x="2" y="8" width="20" height="13" rx="1"/><path d="M2 12h20"/><path d="M12 8v13"/><path d="M12 8S9.5 3 7.5 3.5 8 8 12 8Zm0 0s2.5-5 4.5-4.5S16 8 12 8Z"/>',
    "ruler": '<path d="m3 15 6-6 6 6 6-6"/><path d="M3 21h18"/><path d="M7 9h2"/><path d="M11 5h2"/><path d="M15 9h2"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "box": '<path d="M21 8v8a2 2 0 0 1-1 1.73l-7 4a2 2 0 0 1-2 0l-7-4A2 2 0 0 1 3 16V8a2 2 0 0 1 1-1.73l7-4a2 2 0 0 1 2 0l7 4A2 2 0 0 1 21 8Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h5"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7Z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
    "swap": '<path d="M7 16H3l4-4"/><path d="M3 16h14a4 4 0 0 0 0-8H9"/><path d="m17 8 4 4-4 4"/>',
}


def icon(name, cls=""):
    p = ICONS.get(name, "")
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{p}</svg>')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fig(name, ratio="4/3", cls="", lazy=True, alt=None, zoom=True):
    """Image with inline LQIP, intrinsic dimensions and lazy loading."""
    m = MANIFEST[name]
    alt = alt if alt is not None else ""
    z = " fig-zoom" if zoom else ""
    return (
        f'<figure class="fig fig-ratio-{ratio.replace("/", "-")}{z} {cls}" '
        f'style="background-image:url({m["lqip"]});background-size:cover">'
        f'<img src="{m["src"]}" alt="{alt}" width="{m["w"]}" height="{m["h"]}" '
        f'loading="{"lazy" if lazy else "eager"}" decoding="async" '
        f'data-lqip="{m["lqip"]}"></figure>'
    )


def spec_rows(rows, dense=False):
    out = [f'<dl class="spec{" spec-dense" if dense else ""}">']
    for row in rows:
        k, v = row[0], row[1]
        hl = row[2] if len(row) > 2 else False
        cls = ' class="hl"' if hl else ""
        out.append(f'<div class="spec-row"><dt>{k}</dt><dd{cls}>{v}</dd></div>')
    out.append("</dl>")
    return "".join(out)


def nav_html(current):
    items = []
    for href, label, num in C.NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<a class="nav-link" href="{href}"{cur}>{label}</a>')
    return "".join(items)


def drawer_html(current):
    items = []
    for href, label, num in C.NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<a class="drawer-link" href="{href}"{cur}><span>{num}</span>{label}</a>')
    return "".join(items)


def brand_mark():
    return ('<svg class="brand-mark" viewBox="0 0 32 32" fill="none" stroke="currentColor" '
            'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M4 9h24v18a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9Z"/>'
            '<path d="M4 13h24"/><path d="M12 13v2M16 13v2M20 13v2"/>'
            '<path d="M11 9V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3"/>'
            '<path d="M4 17h24"/></svg>')


def marquee(items):
    track = "".join(f'<span class="marquee-item">{i}</span>' for i in items)
    return f'<div class="marquee"><div class="marquee-track">{track}{track}</div></div>'


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def layout(page, title, desc, body, cls="", scripts="", og_image="hero-bag"):
    m = MANIFEST[og_image]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — {C.BRAND['name']}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0D1014">
<meta property="og:title" content="{title} — {C.BRAND['name']}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{m['src']}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/archivo-800-normal-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/archivo-400-normal-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/ibm-plex-mono-500-normal-latin.woff2" crossorigin>
<link rel="stylesheet" href="assets/css/00_fonts.css">
<link rel="stylesheet" href="assets/css/01_foundations.css">
<link rel="stylesheet" href="assets/css/02_components.css">
<link rel="stylesheet" href="assets/css/03_pages.css">
</head>
<body class="{cls}" data-page="{page}">
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress" id="progress" aria-hidden="true"></div>

<header class="hdr" id="hdr">
  <div class="shell hdr-bar">
    <a class="brand" href="index.html" aria-label="{C.BRAND['name']} home">
      {brand_mark()}
      <span>
        <span class="brand-name">{C.BRAND['name']}</span>
        <span class="brand-sub">Custom Bag Works</span>
      </span>
    </a>
    <nav class="nav" aria-label="Primary">{nav_html(page)}</nav>
    <div class="hdr-cta">
      <a class="btn btn-primary btn-sm" href="contact.html">Request a Quote</a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">
        <span></span>
      </button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  {drawer_html(page)}
  <div class="drawer-foot">
    <a class="btn btn-primary btn-block" href="contact.html">Request a Quote</a>
    <p class="mono muted" style="margin-top:18px">{C.BRAND['phone']}<br>{C.BRAND['email']}</p>
  </div>
</div>

<main id="main">
{body}
</main>

<footer class="ftr">
  <div class="shell">
    <div class="ftr-grid">
      <div class="ftr-col">
        <a class="brand" href="index.html">
          {brand_mark()}
          <span>
            <span class="brand-name">{C.BRAND['name']}</span>
            <span class="brand-sub">Custom Bag Works</span>
          </span>
        </a>
        <p class="lead measure-sm" style="margin-top:20px;font-size:1rem">
          A bag manufacturer with a design room attached. School bags, college bags,
          file bags, duffels and trolleys built to a written specification.
        </p>
        <p class="mono muted" style="margin-top:24px;line-height:1.9">
          {C.BRAND['works_full']}<br>{C.BRAND['studio']}
        </p>
      </div>
      <div class="ftr-col">
        <h3>Products</h3>
        <a class="ftr-link" href="products.html">School Bags</a>
        <a class="ftr-link" href="products.html">College Bags</a>
        <a class="ftr-link" href="products.html">File &amp; Document Bags</a>
        <a class="ftr-link" href="products.html">Duffle &amp; Gym Bags</a>
        <a class="ftr-link" href="products.html">Soft Trolleys</a>
        <a class="ftr-link" href="products.html">Corporate Totes</a>
      </div>
      <div class="ftr-col">
        <h3>Capability</h3>
        <a class="ftr-link" href="process.html">How We Work</a>
        <a class="ftr-link" href="works.html">The Works</a>
        <a class="ftr-link" href="works.html#materials">Materials</a>
        <a class="ftr-link" href="works.html#certs">Certifications</a>
        <a class="ftr-link" href="customise.html">Spec Builder</a>
        <a class="ftr-link" href="industries.html">Industries</a>
      </div>
      <div class="ftr-col">
        <h3>Contact</h3>
        <a class="ftr-link" href="contact.html">Request a Quote</a>
        <a class="ftr-link" href="mailto:{C.BRAND['email']}">{C.BRAND['email']}</a>
        <a class="ftr-link" href="mailto:{C.BRAND['email_export']}">{C.BRAND['email_export']}</a>
        <a class="ftr-link" href="tel:{C.BRAND['phone'].replace(' ', '')}">{C.BRAND['phone']}</a>
        <a class="ftr-link" href="design-system.html">Design System</a>
      </div>
    </div>
    <div class="ftr-wordmark" aria-hidden="true">{C.BRAND['name']}</div>
    <div class="ftr-bottom">
      <span>&copy; {C.BRAND['established']}–2026 {C.BRAND['legal']} · GST {C.BRAND['gst']}</span>
      <span>Bahadurgarh, Haryana · New Delhi · Exports to 30+ countries</span>
    </div>
  </div>
</footer>

<div class="dock" id="dock">
  <div class="dock-card">
    <div class="txt">
      <b>Ready to scope a run?</b>
      <span>Spec Builder · live pricing</span>
    </div>
    <a class="btn btn-primary btn-sm" href="customise.html">Open Builder</a>
  </div>
</div>

<script src="assets/js/main.js" type="module"></script>
{scripts}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Shared sections
# ---------------------------------------------------------------------------
def cta_band(title="Ready to put a spec behind it?",
             body="Tell us the bag, the volume and the deadline. You will get a manufacturability review, a costed price band and a lead time in writing — usually within two working days."):
    return f"""
<section class="cta-band theme-paper blueprint">
  <div class="shell cta-band-inner">
    <div>
      <span class="eyebrow">Next step</span>
      <h2 class="display-m" style="margin-top:18px;max-width:20ch">{title}</h2>
      <p class="lead" style="margin-top:18px">{body}</p>
    </div>
    <div class="stack stack-3" style="min-width:220px">
      <a class="btn btn-primary btn-lg btn-block" href="contact.html">Request a Quote</a>
      <a class="btn btn-lg btn-block" href="customise.html">Open the Spec Builder</a>
    </div>
  </div>
</section>"""


def capability_cards():
    out = []
    for c in C.CAPABILITY:
        out.append(f"""
<div class="idx-card" data-reveal>
  <span class="idx">{c['n']}</span>
  <h3 style="font-size:1.15rem">{c['title']}</h3>
  <p class="muted" style="font-size:.95rem;line-height:1.6">{c['body']}</p>
  <div style="margin-top:auto;padding-top:14px;border-top:1px solid var(--line)">
    <div style="font-family:var(--f-display);font-weight:800;font-size:1.5rem;letter-spacing:-.03em">{c['stat']}</div>
    <div class="mono muted" style="font-size:.62rem;letter-spacing:.12em">{c['statLabel']}</div>
  </div>
</div>""")
    return f'<div class="grid g-2" style="gap:0">{"".join(out)}</div>'


def product_card(p, delay=0):
    f = next((x for x in C.FABRICS if x["id"] == p["default_fabric"]), C.FABRICS[0])
    return f"""
<article class="p-card" data-cat="{p['cat']}" data-slug="{p['slug']}" data-reveal style="--reveal-delay:{delay}ms">
  <div class="p-card-media">
    <span class="p-card-cat">{p['cat']}</span>
    {fig(p['img'], '4/3', alt=p['name'] + ' — custom ' + p['cat'].lower() + ' bag manufactured by Karkhana', lazy=True)}
  </div>
  <div class="p-card-body">
    <h3 class="p-card-title">{p['name']}</h3>
    <p class="p-card-desc">{p['blurb']}</p>
    <dl class="p-card-specs">
      <div><dt>Capacity</dt><dd>{p['capacity']} L</dd></div>
      <div><dt>Weight</dt><dd>{p['weight']:.2f} kg</dd></div>
      <div><dt>MOQ</dt><dd>{p['moq']} pcs</dd></div>
    </dl>
    <div class="p-card-foot">
      <span class="mono muted" style="font-size:.68rem">From {f['name']} · {p['lead']}</span>
      <span class="tlink" style="font-size:.68rem">Configure</span>
    </div>
  </div>
</article>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_home():
    p = C.PRODUCTS
    hero_stats = [
        ("Minimum order", "100", "pcs / style", 100),
        ("Bulk lead time", "20–32", "days", None),
        ("Monthly capacity", "250,000", "units", 250000),
        ("Export markets", "30+", "countries", None),
    ]
    stat_rows = []
    for i, (k, v, u, cnt) in enumerate(hero_stats):
        cls = "hi" if i == 0 else ""
        dc = f' data-count="{cnt}"' if cnt else ""
        stat_rows.append(
            f'<div class="hero-meta-row"><dt>{k}</dt>'
            f'<dd class="{cls}"{dc}>{v} '
            f'<span class="mono muted" style="font-size:.7em">{u}</span></dd></div>'
        )
    stats = "".join(stat_rows)

    body = f"""
<section class="hero">
  <div class="hero-bg">{fig('hero-bag', '3/4', cls='fig-bg', lazy=False, zoom=False)}</div>
  <div class="hero-grain"></div>
  <div class="shell hero-inner">
    <div class="hero-grid">
      <div>
        <span class="eyebrow" data-reveal>Est. {C.BRAND['established']} · Bahadurgarh, India</span>
        <h1 style="margin-top:26px;--reveal-delay:80ms" data-reveal>
          We build bags<br>to a <em>written spec.</em>
        </h1>
        <p class="hero-lede" data-reveal style="--reveal-delay:160ms">
          School bags, college bags, file bags, duffels and trolleys — made in India
          to a specification you approve, at volumes from one hundred pieces.
          No middlemen. No surprises on the ship date.
        </p>
        <div class="hero-actions" data-reveal style="--reveal-delay:240ms">
          <a class="btn btn-primary btn-lg" href="customise.html">Open the Spec Builder</a>
          <a class="btn btn-lg btn-arrow" href="products.html">See the range</a>
        </div>
      </div>
      <dl class="hero-meta" data-reveal style="--reveal-delay:320ms">
        {stats}
      </dl>
    </div>
  </div>
  <div class="scroll-hint" aria-hidden="true">Scroll</div>
</section>

{marquee(['ISO 9001:2015', 'Sedex / SMETA 4-Pillar', 'BSCI', 'GRS 4.0', 'OEKO-TEX Standard 100',
           'REACH', 'CPSIA', 'Prop 65', 'FSC packaging', 'AQL 2.5 inspection', 'DDP available'])}

<section class="section">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">The problem we solve</span>
        <h2 class="display-m" style="margin-top:20px;max-width:19ch" data-reveal>
          Most bag factories are not <em class="serif">design partners.</em>
        </h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Ask a factory for a 600D polyester school bag and you will get a photograph.
          Ask for the stitch density, the bar-tack spec, the zipper brand, the shade band
          and the AQL, and the conversation changes.
        </p>
        <p class="lead" style="margin-top:18px">
          We publish ours. Every quote comes with a tech pack, a graded size sheet, a costed
          price band and a lead time we will hold to in writing. That is the whole difference.
        </p>
      </div>
    </div>

    <div class="grid g-3" style="gap:0">
      <div class="idx-card" data-reveal>
        <span class="idx">01</span>
        <h3 style="font-size:1.15rem">A design room, not a catalogue</h3>
        <p class="muted" style="font-size:.95rem;line-height:1.6">
          Four designers and six pattern makers. You get a graded size sheet, a stitch map,
          a bill of materials and a nesting layout — not a photo of somebody else's bag.
        </p>
      </div>
      <div class="idx-card" data-reveal style="--reveal-delay:80ms">
        <span class="idx">02</span>
        <h3 style="font-size:1.15rem">One roof, not four vendors</h3>
        <p class="muted" style="font-size:.95rem;line-height:1.6">
          Cutting, stitching, branding, foam work and packing all happen in Bahadurgarh.
          A bag is never split across four suppliers, and never assembled by someone who
          did not cut it.
        </p>
      </div>
      <div class="idx-card" data-reveal style="--reveal-delay:160ms">
        <span class="idx">03</span>
        <h3 style="font-size:1.15rem">A price band, not a list price</h3>
        <p class="muted" style="font-size:.95rem;line-height:1.6">
          Costing is built from fabric GSM, hardware, branding process and volume —
          and shown to you in three tiers before you pick one. The Spec Builder does it
          live, with no email required.
        </p>
      </div>
    </div>

    <div class="row" style="margin-top:48px;gap:16px">
      <a class="tlink" href="process.html">How an order actually runs</a>
      <a class="tlink" href="works.html">Inside the works</a>
      <a class="tlink" href="customise.html">Price a bag yourself</a>
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Capability</span>
        <h2 class="display-m" style="margin-top:20px;max-width:18ch" data-reveal>
          What is actually <em class="serif">in-house.</em>
        </h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Capacity claims are cheap. These are the numbers behind them — and every one of
          them is auditable on a factory visit or a third-party inspection.
        </p>
      </div>
    </div>
    {capability_cards()}
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">The range</span>
        <h2 class="display-m" style="margin-top:20px;max-width:16ch" data-reveal>
          Nine silhouettes. <em class="serif">Endless</em> specifications.
        </h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms" class="stack stack-4">
        <p class="lead">
          Every one of these is a starting point, not a fixed product. Fabric, colourway,
          hardware, lining and branding are all specified by you — and every card below
          carries the numbers our floor works to.
        </p>
        <div><a class="tlink" href="products.html">Browse the full catalogue</a></div>
      </div>
    </div>
    <div class="p-grid">
      {''.join(product_card(x, i * 55) for i, x in enumerate(p[:6]))}
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="split split-7-5" style="align-items:center">
      <div data-reveal>
        <span class="eyebrow">The Spec Builder</span>
        <h2 class="display-m" style="margin-top:20px;max-width:17ch">
          Price a bag before you send an email.
        </h2>
        <p class="lead" style="margin-top:20px">
          Choose a silhouette, a fabric, a colourway, a branding method and a hardware finish.
          The builder returns a live spec card, a costed price band at three volumes, your
          real MOQ and a lead time calculated from the actual production path.
        </p>
        <ul class="stack stack-3" style="margin-top:28px">
          {''.join(f'<li class="row" style="gap:12px;flex-wrap:nowrap;align-items:flex-start"><span style="color:var(--accent);flex:none;margin-top:2px">{icon("check")}</span><span class="muted" style="font-size:.95rem">{t}</span></li>' for t in [
              'Costed from fabric GSM, hardware and branding process — not a guess',
              'MOQ recalculated when branding or hardware sets its own minimum',
              'Lead time includes the material, not just the stitching',
              'Export-ready spec you can hand to another factory if you want a second source',
          ])}
        </ul>
        <div class="row" style="margin-top:34px">
          <a class="btn btn-primary btn-lg" href="customise.html">Open the Spec Builder</a>
        </div>
      </div>
      <div data-reveal style="--reveal-delay:120ms">
        <div class="summary">
          <div class="summary-head">
            <span class="mono muted">Live estimate · Kora 22&quot;</span>
            <div class="summary-price"><span class="cur">₹</span>303</div>
            <span class="summary-price per">per unit at 500 pieces</span>
          </div>
          {spec_rows([('Body fabric', '600D Polyester'), ('Colourway', 'Dye-vat Indigo'), ('Branding', 'Screen Print'), ('Hardware', 'Matte Gunmetal'), ('Stitch density', '9 SPI'), ('MOQ', '100 pcs'), ('Lead time', '22–28 days')], dense=True)}
          <div style="padding:16px 20px;border-top:1px solid var(--line);background:var(--bg-soft)">
            <a class="tlink" href="customise.html">Build your own</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Process</span>
        <h2 class="display-m" style="margin-top:20px;max-width:15ch" data-reveal>
          Eight steps. <em class="serif">No surprises.</em>
        </h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          From the first brief to the carton on the dock, this is the order as it actually
          runs — including the parts most factories leave out of the diagram.
        </p>
        <div style="margin-top:20px"><a class="tlink" href="process.html">See the full process</a></div>
      </div>
    </div>
    <div class="grid g-2" style="gap:0 48px">
      {''.join(f'''
      <div class="step" data-reveal>
        <div class="step-num">{s['n']}</div>
        <div class="step-body">
          <h3 style="font-size:1.12rem">{s['title']}</h3>
          <p class="muted" style="font-size:.95rem;line-height:1.6">{s['body']}</p>
          <div class="step-meta">{''.join(f'<span>{m}</span>' for m in s['meta'])}<span class="accent">{s['dur']}</span></div>
        </div>
      </div>''' for s in C.PROCESS[:4])}
    </div>
    <div class="row" style="margin-top:36px"><a class="tlink" href="process.html">Continue to step 05 →</a></div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="split split-6-6" style="align-items:center;gap:clamp(32px,5vw,72px)">
      <div data-reveal>
        {fig('factory-floor', '4/3', alt='A row of industrial lockstitch machines on the Karkhana production floor in Bahadurgarh', zoom=True)}
      </div>
      <div data-reveal style="--reveal-delay:120ms">
        <span class="eyebrow">The works</span>
        <h2 class="display-m" style="margin-top:20px;max-width:15ch">
          Where the <em class="serif">spec</em> gets made.
        </h2>
        <p class="lead" style="margin-top:20px">
          41,000 sq ft in MIE Part B, Bahadurgarh — the densest bag-manufacturing cluster
          in India, where the zippers, separators, buckles and lining all come from within
          sixty kilometres.
        </p>
        <div class="data-strip" style="margin-top:30px">
          <div><dt>Floor area</dt><dd data-count="41000">41,000<span>sq ft</span></dd></div>
          <div><dt>Headcount</dt><dd data-count="320">320<span>people</span></dd></div>
          <div><dt>Lines</dt><dd>8<span>production</span></dd></div>
        </div>
        <div class="row" style="margin-top:30px"><a class="tlink" href="works.html">Tour the facility</a></div>
      </div>
    </div>
  </div>
</section>

{cta_band()}

<section class="section-sm">
  <div class="shell">
    <div class="data-strip">
      <div><dt>Est. year</dt><dd>{C.BRAND['established']}</dd></div>
      <div><dt>Units per month</dt><dd data-count="250000">250,000</dd></div>
      <div><dt>Sample lead time</dt><dd>7–10<span>days</span></dd></div>
      <div><dt>Bulk lead time</dt><dd>20–32<span>days</span></dd></div>
    </div>
  </div>
</section>"""

    return layout("home", "Custom bag manufacturer in India",
                  "Karkhana is a custom bag works in Bahadurgarh, India — school bags, college bags, file bags, duffels and soft trolleys built to a written specification, from 100 pieces.",
                  body, cls="theme-dark")


def page_products():
    cats = "".join(f'<button class="filter" data-filter="{c}" aria-pressed="{"true" if c=="All" else "false"}">{c}</button>' for c in C.CATEGORIES)
    cards = "".join(product_card(p, i * 45) for i, p in enumerate(C.PRODUCTS))

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Products</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">Catalogue · {len(C.PRODUCTS)} silhouettes</span>
        <h1 style="margin-top:20px" data-reveal>Every bag we make, and the numbers behind it.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          These are starting points. Fabric, colourway, hardware, lining and branding are
          specified per order — the capacities, weights and MOQs below are what the
          standard build actually weighs.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="shell">
    <div class="filters" role="group" aria-label="Filter products by category">
      {cats}
      <span class="filter-count" id="filter-count">Showing {len(C.PRODUCTS)} of {len(C.PRODUCTS)}</span>
    </div>
    <h2 class="sr-only">Product catalogue</h2>
    <div class="p-grid" id="product-grid">
      {cards}
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">How we build</span>
        <h2 class="display-m" style="margin-top:20px;max-width:17ch" data-reveal>
          The same eight steps, whatever the bag.
        </h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          A 100-piece conference tote and a 10,000-piece trolley order travel the same
          path: brief, specification, sample, golden sample, procurement, production, QC, dispatch.
        </p>
        <div style="margin-top:20px"><a class="tlink" href="process.html">Read the process</a></div>
      </div>
    </div>
    <div class="grid g-3" style="gap:0">
      {''.join(f'''
      <div class="idx-card" data-reveal>
        <span class="idx">{s['n']}</span>
        <h3 style="font-size:1.05rem">{s['title']}</h3>
        <p class="muted" style="font-size:.9rem;line-height:1.55">{s['body'][:150]}…</p>
      </div>''' for s in C.PROCESS[:6])}
    </div>
  </div>
</section>

{cta_band("Found the silhouette?", "Now price it properly. The Spec Builder turns any of these nine into a costed specification with your real MOQ and lead time.")}"""

    return layout("products", "Products — custom bags, school to trolley",
                  "Nine custom bag silhouettes from Karkhana: school backpacks, college bags, business backpacks, file bags, duffles, soft trolleys, travel packs and corporate totes.",
                  body, cls="theme-dark")


def page_customise():
    fabrics = "".join(f'''
      <button class="opt" data-group="fabric" data-id="{f['id']}" aria-pressed="{"true" if f["id"]=="poly600" else "false"}">
        <span class="opt-name">{f['name']}</span>
        <span class="opt-sub">{f['gsm']} · {f['wr']}</span>
        <span class="opt-delta" data-delta="fabric"></span>
      </button>''' for f in C.FABRICS)

    colours = "".join(f'''
      <div class="swatch-pair">
        <button class="swatch-chip" data-group="colour" data-id="{c['id']}" aria-pressed="{"true" if c["id"]=="indigo" else "false"}"
                style="background:linear-gradient(135deg,{c['body']} 0 62%,{c['accent']} 62% 100%)"
                aria-label="{c['name']} colourway, Pantone {c['pantone']}"></button>
        <span class="swatch-name">{c['name']}</span>
      </div>''' for c in C.COLOURS)

    branding = "".join(f'''
      <button class="opt" data-group="branding" data-id="{b['id']}" aria-pressed="{"true" if b["id"]=="screen" else "false"}">
        <span class="opt-name">{b['name']}</span>
        <span class="opt-sub">{b['sub']}</span>
        <span class="opt-delta" data-delta="branding">+₹{b['unit']} / pc</span>
      </button>''' for b in C.BRANDING)

    hardware = "".join(f'''
      <button class="opt" data-group="hardware" data-id="{h['id']}" aria-pressed="{"true" if h["id"]=="gunmetal" else "false"}">
        <span class="opt-name">{h['name']}</span>
        <span class="opt-sub">{h['sub']}</span>
        <span class="opt-delta" data-delta="hardware">{"Included" if h["unit"]==0 else f"+₹{h['unit']} / pc"}</span>
      </button>''' for h in C.HARDWARE)

    linings = "".join(f'''
      <button class="opt" data-group="lining" data-id="{l['id']}" aria-pressed="{"true" if l["id"]=="plain190" else "false"}">
        <span class="opt-name">{l['name']}</span>
        <span class="opt-sub">{l['sub']}</span>
        <span class="opt-delta" data-delta="lining">{"Included" if l["unit"]==0 else f"+₹{l['unit']} / pc"}</span>
      </button>''' for l in C.LININGS)

    products = "".join(f'''
      <button class="opt" data-group="product" data-id="{p['slug']}" aria-pressed="{"true" if i==0 else "false"}">
        <span class="opt-name">{p['name']}</span>
        <span class="opt-sub">{p['cat']} · {p['capacity']} L · {p['weight']:.2f} kg</span>
        <span class="opt-delta">MOQ {p['moq']}</span>
      </button>''' for i, p in enumerate(C.PRODUCTS))

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Spec Builder</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">Live specification</span>
        <h1 style="margin-top:20px" data-reveal>Build the bag. Watch the cost move.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Six decisions, priced live. The model behind it is the same one that builds your
          quote — fabric weight, hardware, branding process and volume, not a marketing round number.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <h2 class="sr-only">Configure your bag</h2>
    <div class="builder">
      <div class="builder-stage">
        <div class="builder-panel">
          <div class="builder-steps" role="tablist" aria-label="Specification steps">
            <button class="builder-step is-active" data-step="1" role="tab" aria-selected="true"><span class="n">1</span> Silhouette</button>
            <button class="builder-step" data-step="2" role="tab" aria-selected="false"><span class="n">2</span> Fabric</button>
            <button class="builder-step" data-step="3" role="tab" aria-selected="false"><span class="n">3</span> Colourway</button>
            <button class="builder-step" data-step="4" role="tab" aria-selected="false"><span class="n">4</span> Branding</button>
            <button class="builder-step" data-step="5" role="tab" aria-selected="false"><span class="n">5</span> Hardware</button>
            <button class="builder-step" data-step="6" role="tab" aria-selected="false"><span class="n">6</span> Lining</button>
          </div>

          <div class="builder-body">
            <section class="builder-section is-active" data-section="1" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 01 — Choose a silhouette</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                Nine starting points. Each sets a base cost, capacity, weight and minimum order.
              </p>
              <div class="opt-grid opt-grid-3">{products}</div>
            </section>

            <section class="builder-section" data-section="2" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 02 — Choose the body fabric</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                Fabric drives the cost, the weight, the water resistance and the lead time.
                The price factor is the ratio to 600D polyester.
              </p>
              <div class="opt-grid">{fabrics}</div>
            </section>

            <section class="builder-section" data-section="3" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 03 — Choose a colourway</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                Body and accent. Every reference is a Pantone; a lab dip confirms it before bulk.
              </p>
              <div class="swatches">{colours}</div>
              <div class="form-note" style="margin-top:26px">
                {icon("doc")}
                <span>Custom colourways are quoted with a lab dip — 4 to 6 days — so the shade
                band is approved against a physical swatch, not a screen.</span>
              </div>
            </section>

            <section class="builder-section" data-section="4" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 04 — Choose a branding method</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                All branding is done in-house. Setup is a one-time cost; the per-unit figure is what repeats.
              </p>
              <div class="opt-grid">{branding}</div>
            </section>

            <section class="builder-section" data-section="5" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 05 — Choose a hardware finish</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                Buckles, D-rings, zip sliders and rivets. Custom anodised hardware carries its own minimum.
              </p>
              <div class="opt-grid">{hardware}</div>
            </section>

            <section class="builder-section" data-section="6" role="tabpanel">
              <h3 style="font-size:1.15rem;margin-bottom:6px">Step 06 — Choose the lining</h3>
              <p class="muted" style="font-size:.9rem;margin-bottom:22px">
                Plain, printed, recycled or water-resistant. Printed linings add a week for artwork.
              </p>
              <div class="opt-grid">{linings}</div>
            </section>
          </div>

          <div class="builder-nav">
            <button class="btn btn-sm" id="builder-prev" disabled>← Back</button>
            <span class="mono muted" id="builder-count">Step 1 of 6</span>
            <button class="btn btn-primary btn-sm" id="builder-next">Next →</button>
          </div>
        </div>
      </div>

      <aside class="stack stack-4" aria-live="polite">
        <div class="summary" id="builder-summary">
          <div class="summary-head">
            <span class="mono muted" id="sum-name">Kora 22&quot; School Backpack</span>
            <div class="summary-price"><span class="cur">₹</span><span id="sum-price">285</span></div>
            <span class="summary-price per">per unit at <span id="sum-tier">500</span> pieces</span>
          </div>
          <div id="sum-specs"></div>
          <div style="padding:18px 20px;border-top:1px solid var(--line)">
            <table class="tier-table">
              <thead><tr><th>Volume</th><th>₹ / pc</th><th>MOQ</th></tr></thead>
              <tbody id="tier-rows"></tbody>
            </table>
          </div>
          <div style="padding:16px 20px;border-top:1px solid var(--line);background:var(--bg-soft)">
            <a class="btn btn-primary btn-block" id="builder-send" href="contact.html">Send this spec to us</a>
            <p class="mono muted" style="font-size:.62rem;text-align:center;margin-top:12px;line-height:1.7">
              Indicative only. Final costing follows a manufacturability review.
            </p>
          </div>
        </div>

        <div class="card card-tight">
          <span class="mono accent">Delivery estimate</span>
          <div style="font-family:var(--f-display);font-weight:800;font-size:1.7rem;letter-spacing:-.03em;margin-top:8px" id="sum-lead">22–28 days</div>
          <p class="muted" style="font-size:.85rem;margin-top:8px;line-height:1.55" id="sum-lead-note">
            Bulk production, after golden sample approval.
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Honest limits</span>
        <h2 class="display-m" style="margin-top:20px;max-width:18ch" data-reveal>What this estimate is, and is not.</h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms" class="stack stack-4">
        <p class="lead">
          The builder prices a standard build: one colourway, one branding process, one hardware
          finish and standard trims. It is accurate to roughly ±12% for a confirmed configuration.
        </p>
        <ul class="stack stack-3">
          {''.join(f'<li class="row" style="gap:12px;flex-wrap:nowrap;align-items:flex-start"><span style="color:var(--madder);flex:none;margin-top:2px">—</span><span class="muted" style="font-size:.93rem">{t}</span></li>' for t in [
              'Custom hardware moulds, custom webbing widths and multi-colourway runs are quoted separately.',
              'Freight, duty and insurance are excluded — they belong to the shipping quote, not the unit price.',
              'A figure below the minimum order is not offered. We will not quote a MOQ we cannot hold.',
          ])}
        </ul>
      </div>
    </div>
  </div>
</section>

{cta_band("Send us the configuration", "Attach the specification, or just describe the bag in words. We will come back with a manufacturability review, a firm price band and a lead time — within two working days.")}

<script id="builder-data" type="application/json">{json.dumps({
    "products": {p['slug']: {k: p[k] for k in ('name','cat','capacity','weight','moq','lead','base','dims','default_fabric','default_colour')} for p in C.PRODUCTS},
    "fabrics": {f['id']: {k: f[k] for k in ('id','name','sub','gsm','wr','index','lead')} for f in C.FABRICS},
    "colours": {c['id']: {k: c[k] for k in ('id','name','body','accent','pantone')} for c in C.COLOURS},
    "branding": {b['id']: {k: b[k] for k in ('id','name','sub','setup','unit','moq','lead')} for b in C.BRANDING},
    "hardware": {h['id']: {k: h[k] for k in ('id','name','sub','unit','moq','lead')} for h in C.HARDWARE},
    "linings": {l['id']: {k: l[k] for k in ('id','name','sub','unit','lead')} for l in C.LININGS},
    "tiers": C.TIERS,
})}</script>"""

    return layout("customise", "Spec Builder — live custom bag pricing",
                  "Configure a custom bag and see a live spec card, costed price band, MOQ and lead time. School bags, college bags, file bags, duffels and trolleys priced from real manufacturing data.",
                  body, cls="theme-dark")


def page_process():
    steps = "".join(f"""
    <div class="step" id="step-{s['n']}" data-step-block data-reveal>
      <div class="step-num">{s['n']}</div>
      <div class="step-body">
        <h3>{s['title']}</h3>
        <p class="muted">{s['body']}</p>
        <div class="step-meta">{''.join(f'<span>{m}</span>' for m in s['meta'])}<span class="accent">{s['dur']}</span></div>
      </div>
    </div>""".replace("\n    ", "\n      ") for s in C.PROCESS)

    index = "".join(f'<a class="proc-link" href="#step-{s["n"]}" data-proc-link="{s["n"]}"><span class="n">{s["n"]}</span>{s["title"]}</a>' for s in C.PROCESS)

    faq = "".join(f"""
    <div class="acc-item" data-reveal>
      <button class="acc-trigger" aria-expanded="false"><span>{f['q']}</span><span class="acc-icon" aria-hidden="true">+</span></button>
      <div class="acc-panel"><div><div class="acc-content">{f['a']}</div></div></div>
    </div>""".replace("\n    ", "\n    ") for f in C.FAQ)

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Process</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">How an order runs</span>
        <h1 style="margin-top:20px" data-reveal>Eight steps, and none of them are a surprise.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          This is the real sequence, with the real durations. Where most factories leave a
          gap between "sample approved" and "invoice settled", we have put a number on it.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <h2 class="sr-only">The eight steps</h2>
    <div class="proc-layout">
      <nav class="proc-index" aria-label="Process steps">{index}</nav>
      <div class="stack">{steps}</div>
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Quality control</span>
        <h2 class="display-m" style="margin-top:20px;max-width:16ch" data-reveal>Inspection is a gate, not a gesture.</h3>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Material inspection, in-line checks and a final audit, against a written standard
          agreed at the golden sample stage. Third-party inspectors are welcome at any point.
        </p>
      </div>
    </div>
    <div class="grid g-3" style="gap:0">
      {''.join(f'''
      <div class="idx-card" data-reveal>
        <span class="idx">{i:02d}</span>
        <h3 style="font-size:1.05rem">{t}</h3>
        <p class="muted" style="font-size:.9rem;line-height:1.55">{d}</p>
      </div>''' for i, (t, d) in enumerate([
        ("Material inspection", "Every roll is checked on arrival for GSM, width, shade and defects. Off-spec fabric is rejected at the gate, not at the bag."),
        ("In-line checks", "Seam strength, stitch density, bar-tack placement and hardware pull force are verified during the run, not after it."),
        ("Final audit", "AQL 2.5 for major defects and 4.0 for minor, on ANSI/ASQ Z1.4. Colour, logo scale and label placement are checked against the golden sample."),
        ("Third-party welcome", "SGS, Bureau Veritas, Intertek or your own auditor can inspect at any stage, at your cost. We do not restrict the window."),
        ("Barcodes & labelling", "EAN, UPC, RFID, country-of-origin and care labelling to destination-market requirement, applied before packing."),
        ("Export packing", "Polybag, hang tag, gift box, master carton and palletisation, with carton marks and shipping documents prepared in-house."),
      ]))}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Questions</span>
        <h2 class="display-m" style="margin-top:20px;max-width:16ch" data-reveal>The eight questions every buyer asks.</h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Answered without hedging. If something depends on your project, we will say so
          rather than give a number that will not hold.
        </p>
      </div>
    </div>
    <div>
      {faq}
    </div>
  </div>
</section>

{cta_band("Start at step one", "Send the brief in whatever form you have it — a sketch, a photo, a tech pack from another factory, or a bag you like. We will tell you what it will take to build it.")}"""

    return layout("process", "Process — from brief to dispatch",
                  "How a custom bag order actually runs at Karkhana: brief, manufacturability review, sampling, golden sample, procurement, bulk production, AQL inspection and dispatch.",
                  body, cls="theme-dark")


def page_works():
    mats = "".join(f"""
      <div class="mat-cell" data-reveal>
        <div class="mat-fabrics">{''.join(f'<span style="background:{c}"></span>' for c in m['cols'])}</div>
        <h3>{m['name']}</h3>
        <span class="mono muted" style="font-size:.62rem;letter-spacing:.12em">{m['sub']}</span>
        <p>{m['body']}</p>
      </div>""".replace("\n      ", "\n      ") for m in C.MATERIALS)

    certs = "".join(f"""
      <div class="proof" data-reveal>
        <span class="proof-icon">{icon("check")}</span>
        <div>
          <div style="font-weight:600;font-size:.98rem">{n}</div>
          <div class="mono muted" style="font-size:.62rem;letter-spacing:.1em;margin-top:3px">{d}</div>
        </div>
      </div>""".replace("\n      ", "\n      ") for n, d in C.CERTIFICATIONS)

    mach = "".join(f"""
      <div class="mach" data-reveal>
        <span class="q">{icon("box")}</span>
        <span class="n">{n}</span>
        <span class="c">{c}</span>
      </div>""".replace("\n      ", "\n      ") for n, c, _ in C.MACHINES)

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>The Works</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">Bahadurgarh · Haryana</span>
        <h1 style="margin-top:20px" data-reveal>41,000 sq ft inside India's densest bag cluster.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          MIE Part B, Bahadurgarh — the industrial estate where India's school bags, trolley
          bags and travel bags are actually made. Zippers from Jalandhar. Fabric from Erode.
          Trims from next door.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <div class="split split-7-5">
      <div data-reveal>{fig('factory-floor', '4/3', alt='The Karkhana production floor in Bahadurgarh with industrial lockstitch machines running')}</div>
      <div class="stack stack-6" data-reveal style="--reveal-delay:120ms">
        <div class="data-strip">
          <div><dt>Floor area</dt><dd>41,000<span>sq ft</span></dd></div>
          <div><dt>Headcount</dt><dd>320<span>people</span></dd></div>
        </div>
        <div class="data-strip">
          <div><dt>Production lines</dt><dd>8<span>lines</span></dd></div>
          <div><dt>Shifts</dt><dd>4<span>daily</span></dd></div>
        </div>
        <div>
          <span class="mono accent">Capacity</span>
          <p class="muted" style="margin-top:10px;line-height:1.65">
            250,000 units a month, quoted against a live capacity board rather than a
            theoretical ceiling. When we give you a lead time, it is the one the board shows.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="materials">
  <div class="shell">
    <div class="sec-head has-side">
      <div>
        <span class="eyebrow">Materials library</span>
        <h2 class="display-m" style="margin-top:20px;max-width:16ch" data-reveal>What we can build from.</h2>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Eight input families, each with a real specification. If something is not on this
          list, it is almost certainly still possible — we source a great deal outside it.
        </p>
      </div>
    </div>
    <div class="mat-grid">{mats}</div>
    <div class="row" style="margin-top:34px">
      <a class="tlink" href="customise.html">See fabric pricing in the Spec Builder</a>
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="split split-6-6" style="gap:clamp(32px,5vw,72px)">
      <div data-reveal>
        <span class="eyebrow">Machinery</span>
        <h2 class="display-m" style="margin-top:20px;max-width:15ch">The plant floor, itemised.</h2>
        <div class="mach-list" style="margin-top:32px">{mach}</div>
      </div>
      <div class="stack stack-6" data-reveal style="--reveal-delay:120ms">
        <div>
          {fig('material-macro', '4/3', alt='Macro detail of coated polyester, waxed canvas and ripstop fabric swatches with saddle stitching')}
        </div>
        <div>
          {fig('hardware-macro', '1/1', alt='Macro detail of a matte gunmetal zipper pull, D-ring, buckle and bartack reinforcement')}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="certs">
  <div class="shell">
    <div class="split split-5-7">
      <div data-reveal>
        <span class="eyebrow">Compliance</span>
        <h2 class="display-m" style="margin-top:20px;max-width:13ch">Current, dated and in scope.</h2>
        <p class="lead" style="margin-top:20px">
          A factory that held BSCI two years ago is not the same as one that maintains it.
          Ask any of these for the certificate with its expiry date and scope, and you will get it.
        </p>
        <div class="row" style="margin-top:28px">
          <a class="tlink" href="contact.html">Request the compliance pack</a>
        </div>
      </div>
      <div data-reveal style="--reveal-delay:100ms">{certs}</div>
    </div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="split split-6-6" style="align-items:center;gap:clamp(32px,5vw,72px)">
      <div data-reveal>
        {fig('design-studio', '4/3', alt='The Karkhana design studio with fabric swatches, tech-pack drawings and a laptop on the work table')}
      </div>
      <div data-reveal style="--reveal-delay:120ms">
        <span class="eyebrow">Design room</span>
        <h2 class="display-m" style="margin-top:20px;max-width:14ch">Where the tech pack is born.</h2>
        <p class="lead" style="margin-top:20px">
          Four industrial designers and six pattern makers, in Okhla, New Delhi. They produce
          a graded size sheet, a stitch map, a bill of materials and a CAD nesting layout for
          every order — and the tech pack is yours to keep.
        </p>
        <ul class="stack stack-3" style="margin-top:26px">
          {''.join(f'<li class="row" style="gap:12px;flex-wrap:nowrap;align-items:flex-start"><span style="color:var(--accent);flex:none;margin-top:2px">{icon("check")}</span><span class="muted" style="font-size:.94rem">{t}</span></li>' for t in [
              "Graded size sheet with stated tolerances",
              "Bill of materials — GSM, denier, hardware spec",
              "Stitch map and branding placement sheet",
              "CAD nesting layout, 88% average marker efficiency",
          ])}
        </ul>
      </div>
    </div>
  </div>
</section>

{cta_band("Come and see it", "Factory visits are welcome and encouraged. We will show you the cutting floor, the sewing lines and the QC bench — and let you talk to the people running them.")}"""

    return layout("works", "The Works — factory, materials, compliance",
                  "Inside Karkhana: 41,000 sq ft in Bahadurgarh, eight production lines, 250,000 units a month, a full materials library and current ISO, Sedex, BSCI and GRS certification.",
                  body, cls="theme-dark")


def page_industries():
    inds = "".join(f"""
      <article class="ind-card" data-reveal>
        <span class="ind-icon">{icon(i['icon'])}</span>
        <h3>{i['title']}</h3>
        <p class="muted">{i['body']}</p>
        <div class="ind-list">{''.join(f'<span>{t}</span>' for t in i['tags'])}</div>
      </article>""".replace("\n      ", "\n      ") for i in C.INDUSTRIES)

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Who We Build For</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">Programs</span>
        <h1 style="margin-top:20px" data-reveal>Different buyers, the same factory.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          A school's replacement cycle and a D2C brand's first colourway run are different
          problems. The manufacturing underneath is the same — and so is the specification.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <h2 class="sr-only">Programs we run</h2>
    <div class="grid g-3">{inds}</div>
  </div>
</section>

<section class="section theme-paper blueprint" style="border-top:1px solid var(--paper-line)">
  <div class="shell">
    <div class="split split-7-5" style="align-items:center;gap:clamp(32px,5vw,72px)">
      <div data-reveal>
        <span class="eyebrow">Volume reality</span>
        <h2 class="display-m" style="margin-top:20px;max-width:16ch">Where your order sits in the market.</h2>
        <p class="lead" style="margin-top:20px">
          India's bag market runs to roughly USD 4.8 billion, growing at about 10.8% a year.
          Backpacks are the largest product type at 24.8% of the market, and school bags add
          a 18.9% band of replacement demand that does not care about the fashion cycle.
        </p>
        <p class="lead" style="margin-top:16px">
          That mix is why we keep a 100-piece MOQ on standard constructions. The volume exists
          — it is just distributed across a very large number of buyers.
        </p>
      </div>
      <div data-reveal style="--reveal-delay:120ms">
        <div class="data-strip">
          <div><dt>India bags market</dt><dd>$4.8<span>bn 2025</span></dd></div>
          <div><dt>Growth</dt><dd>10.8<span>% CAGR</span></dd></div>
        </div>
        <div class="data-strip" style="margin-top:1px">
          <div><dt>Backpacks</dt><dd>24.8<span>% share</span></dd></div>
          <div><dt>School bags</dt><dd>18.9<span>% share</span></dd></div>
        </div>
        <div class="data-strip" style="margin-top:1px">
          <div><dt>Polyester input</dt><dd>39.6<span>% of mix</span></dd></div>
          <div><dt>West India</dt><dd>34.5<span>% share</span></dd></div>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_band("Tell us the program", "Annual school replacement, a D2C capsule, an export line, a one-off corporate gift run — describe it and we will tell you what it takes to make it repeatable.")}"""

    return layout("industries", "Who we build for",
                  "Custom bag manufacturing programs for schools and institutions, colleges, corporates, D2C brands, exporters, promotional gifting and travel brands.",
                  body, cls="theme-dark")


def page_contact():
    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Enquire</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">Request a quote</span>
        <h1 style="margin-top:20px" data-reveal>Tell us the bag. We will send back the numbers.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          This form is structured like a tech pack, because that is what we will send you
          back. The more you fill in, the sharper the first response.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <div class="split split-7-5" style="gap:clamp(32px,5vw,72px)">
      <div>
        <form class="card card-pad-lg" id="rfq-form" novalidate>
          <div class="row-between" style="margin-bottom:28px">
            <h2 style="font-size:1.35rem">RFQ · Request for Quotation</h2>
            <span class="tag tag-accent">Reply in 2 working days</span>
          </div>

          <div class="form-note" style="margin-bottom:28px">
            {icon("doc")}
            <span>Attach a sketch, a reference photo, a tech pack or a sample by email to
            <a class="tlink" style="font-size:.8rem" href="mailto:{C.BRAND['email']}">{C.BRAND['email']}</a>
            and reference this form. We will build from it directly.</span>
          </div>

          <div class="stack stack-6">
            <div class="form-grid">
              <div class="field">
                <label for="f-name">Name <span class="req">*</span></label>
                <input class="input" id="f-name" name="name" type="text" required autocomplete="name" placeholder="Your full name">
                <span class="field-error" data-error-for="f-name"></span>
              </div>
              <div class="field">
                <label for="f-org">Company</label>
                <input class="input" id="f-org" name="org" type="text" autocomplete="organization" placeholder="Brand, institution or company">
                <span class="field-error" data-error-for="f-org"></span>
              </div>
              <div class="field">
                <label for="f-email">Email <span class="req">*</span></label>
                <input class="input" id="f-email" name="email" type="email" required autocomplete="email" placeholder="you@company.com">
                <span class="field-error" data-error-for="f-email"></span>
              </div>
              <div class="field">
                <label for="f-phone">Phone / WhatsApp</label>
                <input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+91 …">
                <span class="field-error" data-error-for="f-phone"></span>
              </div>
              <div class="field">
                <label for="f-type">Bag type <span class="req">*</span></label>
                <select class="select" id="f-type" name="type" required>
                  <option value="">Select a category…</option>
                  {''.join(f'<option value="{c}">{c} bag</option>' for c in C.CATEGORIES[1:])}
                  <option value="Other">Something else</option>
                </select>
                <span class="field-error" data-error-for="f-type"></span>
              </div>
              <div class="field">
                <label for="f-qty">Quantity per style <span class="req">*</span></label>
                <select class="select" id="f-qty" name="qty" required>
                  <option value="">Select a volume…</option>
                  {''.join(f'<option value="{t["label"]}">{t["label"]} pieces</option>' for t in C.TIERS)}
                  <option value="Other">Not sure yet</option>
                </select>
                <span class="field-error" data-error-for="f-qty"></span>
              </div>
              <div class="field">
                <label for="f-market">Target market</label>
                <select class="select" id="f-market" name="market">
                  <option value="">Select a market…</option>
                  <option>India — domestic</option>
                  <option>Europe / UK</option>
                  <option>North America</option>
                  <option>Middle East / GCC</option>
                  <option>Africa</option>
                  <option>Asia Pacific</option>
                  <option>Other</option>
                </select>
                <span class="field-error" data-error-for="f-market"></span>
              </div>
              <div class="field">
                <label for="f-when">Delivery needed by</label>
                <input class="input" id="f-when" name="when" type="text" placeholder="e.g. 15 December, or “flexible”">
                <span class="field-error" data-error-for="f-when"></span>
              </div>
              <div class="field span-2">
                <label for="f-spec">What do you need built?</label>
                <textarea class="textarea" id="f-spec" name="spec" placeholder="Bag type, size, fabric, branding method, colours, features — as much or as little as you know."></textarea>
                <span class="field-error" data-error-for="f-spec"></span>
              </div>
              <div class="field span-2">
                <label>Do you already have a design?</label>
                <div class="grid g-3" style="gap:10px">
                  <label class="choice"><input type="radio" name="design" value="Tech pack" checked><span class="box"></span><span class="choice-body"><span class="choice-title">Tech pack</span><span class="choice-sub">We have files</span></span></label>
                  <label class="choice"><input type="radio" name="design" value="Reference image"><span class="box"></span><span class="choice-body"><span class="choice-title">Reference</span><span class="choice-sub">Image or sample</span></span></label>
                  <label class="choice"><input type="radio" name="design" value="From scratch"><span class="box"></span><span class="choice-body"><span class="choice-title">From scratch</span><span class="choice-sub">You design it</span></span></label>
                </div>
              </div>
              <div class="field span-2">
                <label for="f-notes">Anything else</label>
                <textarea class="textarea" id="f-notes" name="notes" placeholder="Compliance needs, packaging, barcodes, delivery window, budget band — all useful."></textarea>
                <span class="field-error" data-error-for="f-notes"></span>
              </div>
            </div>

            <div class="row-between" style="gap:16px;padding-top:8px">
              <p class="mono muted" style="font-size:.62rem;line-height:1.7;max-width:40ch">
                We reply within two working days. Your details are not shared or sold — see our
                confidentiality terms.
              </p>
              <button class="btn btn-primary btn-lg" type="submit">Send the brief</button>
            </div>
          </div>

          <div class="form-success" id="form-success" role="status">
            <span style="color:var(--accent);flex:none">{icon("check")}</span>
            <div>
              <h3 style="font-size:1.1rem">Brief received.</h3>
              <p class="muted" style="margin-top:8px;font-size:.95rem;line-height:1.6">
                Thank you. A manufacturability review, a costed price band and a lead time will
                reach you at the address you gave, usually within two working days. If it is
                urgent, call <a class="tlink" style="font-size:.78rem" href="tel:{C.BRAND['phone'].replace(' ', '')}">{C.BRAND['phone']}</a>.
              </p>
            </div>
          </div>
        </form>
      </div>

      <aside class="stack stack-6">
        <div class="card">
          <span class="mono accent">Works</span>
          <dl class="stack" style="margin-top:16px">
            <div class="contact-item"><dt>Factory</dt><dd>{C.BRAND['works_full']}</dd></div>
            <div class="contact-item"><dt>Design studio</dt><dd>{C.BRAND['studio']}</dd></div>
            <div class="contact-item"><dt>Email</dt><dd><a href="mailto:{C.BRAND['email']}">{C.BRAND['email']}</a></dd></div>
            <div class="contact-item"><dt>Export desk</dt><dd><a href="mailto:{C.BRAND['email_export']}">{C.BRAND['email_export']}</a></dd></div>
            <div class="contact-item"><dt>Phone</dt><dd><a href="tel:{C.BRAND['phone'].replace(' ', '')}">{C.BRAND['phone']}</a></dd></div>
            <div class="contact-item"><dt>Hours</dt><dd>{C.BRAND['hours']}</dd></div>
          </dl>
        </div>

        <div class="card card-tight">
          <span class="mono accent">What happens next</span>
          <div class="stack stack-4" style="margin-top:18px">
            {''.join(f'''
            <div class="row" style="gap:14px;flex-wrap:nowrap;align-items:flex-start">
              <span class="mono accent" style="flex:none;padding-top:2px">{n}</span>
              <span class="muted" style="font-size:.93rem;line-height:1.55">{t}</span>
            </div>''' for n, t in [
              ("01", "We read the brief for buildability and reply — with questions if any."),
              ("02", "You receive a manufacturability review, a price band and a lead time."),
              ("03", "A sample is cut and shipped for approval, usually inside ten days."),
              ("04", "On approval the golden sample is signed and bulk production is scheduled."),
            ])}
          </div>
        </div>

        <div class="card card-tight">
          <span class="mono accent">Before you write</span>
          <p class="muted" style="margin-top:14px;font-size:.93rem;line-height:1.6">
            If you would rather price a bag yourself first, the
            <a class="tlink" style="font-size:.8rem" href="customise.html">Spec Builder</a>
            gives you a live cost band, MOQ and lead time without waiting for anyone.
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return layout("contact", "Enquire — request a quote",
                  "Request a custom bag quote from Karkhana. Backpacks, school bags, college bags, file bags, duffles and trolleys manufactured in Bahadurgarh, India, from 100 pieces.",
                  body, cls="theme-dark")


def page_design_system():
    colours = [
        ("--ink", "#0D1014", "Primary dark ground"),
        ("--ink-2", "#161B22", "Raised dark surface"),
        ("--ink-3", "#1F252D", "Raised surface, lighter"),
        ("--paper", "#F2EEE6", "Light spec-sheet ground"),
        ("--paper-2", "#E7E1D5", "Kraft / secondary light"),
        ("--marigold", "#E9A319", "Primary accent — turmeric dye"),
        ("--marigold-hi", "#FFC155", "Accent on dark grounds"),
        ("--marigold-dk", "#B97B0A", "Accent text on paper"),
        ("--indigo", "#16264A", "Secondary — dye-vat indigo"),
        ("--indigo-lt", "#2C4374", "Indigo, light"),
        ("--madder", "#B8402C", "Signal / scarcity only"),
        ("--slate", "#7C8590", "Muted metadata"),
    ]
    type_rows = [
        ("Display XL", "clamp(3.1rem, 8.6vw, 8.25rem)", "Archivo 800 · -0.035em", "display-xl", "Bag, built to a spec."),
        ("Display L", "clamp(2.5rem, 5.8vw, 5rem)", "Archivo 800 · -0.035em", "display-l", "Built to a spec"),
        ("Display M", "clamp(1.95rem, 3.9vw, 3.35rem)", "Archivo 700 · -0.035em", "display-m", "Built to a spec"),
        ("Heading 2", "clamp(1.7rem, 3.1vw, 2.85rem)", "Archivo 700 · -0.02em", "h2", "Specification"),
        ("Heading 3", "clamp(1.2rem, 1.9vw, 1.7rem)", "Archivo 700 · -0.02em", "h3", "Specification"),
        ("Lead", "clamp(1.05rem, 1.35vw, 1.3rem)", "Archivo 400 · 1.52", "lead", "Every bag we make is built to a specification you can read, sign and hold us to."),
        ("Body", "1.03125rem", "Archivo 400 · 1.66", "p", "Every bag we make is built to a specification you can read, sign and hold us to."),
        ("Spec / Mono", "0.765rem", "IBM Plex Mono 500 · 0.14em", "mono", "600D POLYESTER · 210 GSM"),
    ]
    space_rows = [
        ("--s-1", "4px"), ("--s-2", "8px"), ("--s-3", "12px"), ("--s-4", "16px"),
        ("--s-5", "24px"), ("--s-6", "32px"), ("--s-7", "40px"), ("--s-8", "48px"),
        ("--s-9", "64px"), ("--s-10", "80px"), ("--s-11", "104px"), ("--s-12", "136px"),
    ]

    def type_row(label, size, meta, cls, sample):
        return f"""
      <div class="ds-type-row">
        <div class="meta">{label}<br>{size}<br>{meta}</div>
        <div class="specimen"><div class="{cls}">{sample}</div></div>
      </div>"""

    body = f"""
<section class="phead blueprint">
  <div class="shell">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Design System</span></nav>
    <div class="phead-grid">
      <div>
        <span class="eyebrow">The Technical Atelier</span>
        <h1 style="margin-top:20px" data-reveal>A design system for a manufacturer.</h1>
      </div>
      <div data-reveal style="--reveal-delay:100ms">
        <p class="lead">
          Built on the visual language of a spec sheet — dimension lines, tick marks, monospace
          labels, measured swatches — rendered with the material richness of a textile mill.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-top:0">
  <div class="shell">
    <div class="split split-7-5" style="gap:clamp(32px,5vw,72px)">
      <div class="stack stack-10">

        <div>
          <span class="eyebrow">01 — Concept</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">The premise</h2>
          <p class="lead">
            A bag is a manufactured object with tolerances, not a photograph on a catalogue page.
            This site is built on that claim: the spec is the interface. Every data point on the
            site is a real manufacturing value — GSM, denier, SPI, AQL, MOQ, lead time — because
            the credibility gap in this category is credibility expressed as specification.
          </p>
          <p class="lead" style="margin-top:16px">
            The recurring motif is the <strong style="color:var(--accent)">saddle-stitch rule</strong>
            — a dashed 2px line borrowed from leatherwork — used at every section boundary. The
            second device is the <strong style="color:var(--accent)">dimension callout</strong>,
            which frames products as objects with measurements rather than as pictures.
          </p>
        </div>

        <div>
          <span class="eyebrow">02 — Colour</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">Dye-vat palette</h2>
          <p class="muted" style="margin-bottom:22px">
            Two grounds — deep ink and warm paper — alternating down the page in a day/night
            rhythm. The accent is a turmeric marigold, a working Indian dye reference rather
            than a decorative one. Indigo carries the structural notes; madder is reserved for
            scarcity and error states, and is never used for anything else.
          </p>
          <div>
            {''.join(f'''
            <div class="ds-token">
              <div class="ds-color" style="background:{hex}"></div>
              <div>
                <div class="mono" style="color:var(--fg)">{name}</div>
                <div class="mono muted" style="font-size:.66rem;margin-top:3px">{hex} — {use}</div>
              </div>
            </div>''' for name, hex, use in colours)}
          </div>
        </div>

        <div>
          <span class="eyebrow">03 — Typography</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">Three voices</h2>
          <p class="muted" style="margin-bottom:26px">
            <strong style="color:var(--fg)">Archivo</strong> carries every structural voice —
            display, headings and body. <strong style="color:var(--fg)">Instrument Serif</strong>
            appears only in italic, as a counterpoint inside display lines. <strong style="color:var(--fg)">IBM Plex Mono</strong>
            is reserved exclusively for data: labels, units, measurements, spec keys and anything
            that would sit in a tech pack. If it is a number, it is monospace.
          </p>
          {''.join(type_row(*r) for r in type_rows)}
        </div>

        <div>
          <span class="eyebrow">04 — Space &amp; Grid</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">Eight-point baseline</h2>
          <p class="muted" style="margin-bottom:24px">
            An 8px baseline, a 12-column grid at 1440px, and a 32px gutter that flexes to 48px
            on wide screens. Section rhythm is fluid, from 64px on mobile to 136px on desktop.
            Asymmetric splits (7/5 and 8/4) carry most page compositions; centred symmetry is
            reserved for the hero and the closing band.
          </p>
          <div class="grid g-4" style="gap:1px;background:var(--line);border:1px solid var(--line)">
            {''.join(f'<div style="background:var(--bg-soft);padding:14px 10px"><div class="mono accent" style="font-size:.66rem">{n}</div><div class="mono muted" style="font-size:.6rem;margin-top:4px">{v}</div></div>' for n, v in space_rows)}
          </div>
        </div>

        <div>
          <span class="eyebrow">05 — Components</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">The working set</h2>
          <div class="grid g-2" style="gap:var(--s-5)">
            <div class="card card-tight">
              <span class="mono muted">Buttons</span>
              <div class="row" style="margin-top:14px">
                <button class="btn btn-primary">Primary</button>
                <button class="btn">Secondary</button>
                <button class="btn btn-arrow">Arrow</button>
              </div>
            </div>
            <div class="card card-tight">
              <span class="mono muted">Tags</span>
              <div class="row" style="margin-top:14px">
                <span class="tag">Neutral</span>
                <span class="tag tag-accent tag-dot">Accent</span>
                <span class="tag tag-solid">Solid</span>
              </div>
            </div>
            <div class="card card-tight">
              <span class="mono muted">Spec row</span>
              {spec_rows([('Capacity', '30 L', True), ('Weight', '0.86 kg', False), ('MOQ', '100 pcs', False)], dense=True)}
            </div>
            <div class="card card-tight">
              <span class="mono muted">Choice</span>
              <label class="choice" style="margin-top:14px"><input type="radio" name="ds" checked><span class="box"></span><span class="choice-body"><span class="choice-title">Selected option</span><span class="choice-sub">Radio card</span></span></label>
            </div>
            <div class="card card-tight" style="grid-column:1/-1">
              <span class="mono muted">Saddle-stitch rule</span>
              <div class="stitch" style="margin-top:16px"></div>
              <div class="row" style="margin-top:16px;gap:16px">
                <span class="numeral">01</span>
                <span class="mono muted">The motif repeats at every section boundary</span>
              </div>
            </div>
          </div>
        </div>

        <div>
          <span class="eyebrow">06 — Motion</span>
          <h2 class="display-m" style="margin-top:16px;margin-bottom:20px">Restraint as a principle</h2>
          <p class="muted" style="margin-bottom:20px">
            Motion exists to direct attention, never to entertain. Elements reveal with an
            18px rise and a 620ms ease-out, staggered at 60ms. Section numerals count. The
            capability marquee runs at a reading pace and pauses on hover. Everything animates
            on transform and opacity only — never width, height or top — and the entire system
            collapses to a near-zero duration under <code style="font-family:var(--f-mono);font-size:.85em">prefers-reduced-motion</code>.
          </p>
          <div class="card card-tight">
            <div class="row-between">
              <span class="mono muted">Easing</span>
              <span class="mono accent">cubic-bezier(.16, 1, .3, 1)</span>
            </div>
            <div class="row-between" style="margin-top:10px">
              <span class="mono muted">Reveal</span>
              <span class="mono accent">18px rise · 620ms · 60ms stagger</span>
            </div>
            <div class="row-between" style="margin-top:10px">
              <span class="mono muted">Radius</span>
              <span class="mono accent">2px technical / 999px pill</span>
            </div>
            <div class="row-between" style="margin-top:10px">
              <span class="mono muted">Elevation</span>
              <span class="mono accent">Hairlines, not shadows</span>
            </div>
          </div>
        </div>
      </div>

      <aside class="stack stack-6">
        <div class="card card-tight">
          <span class="mono accent">Signature devices</span>
          <div class="stack stack-4" style="margin-top:16px">
            <div><strong style="font-size:.95rem">Saddle-stitch rule</strong><div class="muted" style="font-size:.85rem;line-height:1.5;margin-top:3px">Dashed 2px divider. The site's recognisable motif.</div></div>
            <div><strong style="font-size:.95rem">Dimension callout</strong><div class="muted" style="font-size:.85rem;line-height:1.5;margin-top:3px">Hairline with an end tick and a monospace measurement.</div></div>
            <div><strong style="font-size:.95rem">Material swatch chip</strong><div class="muted" style="font-size:.85rem;line-height:1.5;margin-top:3px">Real GSM and denier values, never vague descriptors.</div></div>
            <div><strong style="font-size:.95rem">Blueprint grid</strong><div class="muted" style="font-size:.85rem;line-height:1.5;margin-top:3px">1px grid at 4% opacity on dark sections — the cutting table.</div></div>
          </div>
        </div>
        <div class="card card-tight">
          <span class="mono accent">Accessibility</span>
          <div class="stack stack-3" style="margin-top:16px">
            {''.join(f'<div class="row" style="gap:10px;flex-wrap:nowrap;align-items:flex-start"><span style="color:var(--accent);flex:none;margin-top:1px">{icon("check")}</span><span class="muted" style="font-size:.88rem;line-height:1.5">{t}</span></div>' for t in [
              "WCAG AA contrast on every text/background pair",
              "Full keyboard operation for nav, filters, tabs and forms",
              "Visible focus ring on every interactive element",
              "Motion fully disabled under prefers-reduced-motion",
              "Every image carries alt text, dimensions and lazy loading",
            ])}
          </div>
        </div>
        <div class="card card-tight">
          <span class="mono accent">Type stack</span>
          <div class="stack stack-3" style="margin-top:16px">
            <div class="row-between"><span class="muted" style="font-size:.88rem">Archivo</span><span class="mono" style="font-size:.66rem">400–800</span></div>
            <div class="row-between"><span class="muted" style="font-size:.88rem">Instrument Serif</span><span class="mono" style="font-size:.66rem">400 italic</span></div>
            <div class="row-between"><span class="muted" style="font-size:.88rem">IBM Plex Mono</span><span class="mono" style="font-size:.66rem">400–600</span></div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>

{cta_band("Build on the system", "The tokens, the grid and the components behind this site are documented above. If you are building a bag brand's own site, this is a usable foundation.")}"""

    return layout("design-system", "Design System — The Technical Atelier",
                  "The complete design system behind the Karkhana website: concept, dye-vat colour palette, three-voice typography, eight-point spacing grid, component set and motion principles.",
                  body, cls="theme-dark")


def page_404():
    body = """
<section class="nf blueprint">
  <div class="shell">
    <div class="numeral" style="opacity:1;margin-bottom:20px">Lost in the sewing room</div>
    <h1 class="display-l" style="max-width:16ch;margin-inline:auto">This page is not on the production schedule.</h1>
    <h2 class="sr-only">Page not found</h2>
    <p class="lead" style="margin:22px auto 0">
      The link you followed either moved or never existed. Nothing was cut in error.
    </p>
    <div class="row" style="justify-content:center;margin-top:34px">
      <a class="btn btn-primary" href="index.html">Back to the works</a>
      <a class="btn" href="products.html">See the range</a>
    </div>
  </div>
</section>"""
    return layout("404", "Page not found", "The page you are looking for does not exist on the Karkhana site.",
                  body, cls="theme-dark")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    # Materialise binary assets if they are only present in their encoded
    # (.b64) form — the form that survives the GitHub text transport.
    try:
        sys.path.insert(0, os.path.join(HERE, "tools"))
        from decode_assets import decode_all, integrity_report
        written, _skipped = decode_all(quiet=True)
        if written:
            print(f"  decoded {len(written)} binary asset(s) from .b64 sources")
        bad = integrity_report()
        if bad:
            raise SystemExit(f"asset integrity check failed: {bad}")
    except ImportError:
        pass

    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST, exist_ok=True)

    pages = {
        "index.html": page_home(),
        "products.html": page_products(),
        "customise.html": page_customise(),
        "process.html": page_process(),
        "works.html": page_works(),
        "industries.html": page_industries(),
        "contact.html": page_contact(),
        "design-system.html": page_design_system(),
        "404.html": page_404(),
    }
    for name, html in pages.items():
        with open(os.path.join(DIST, name), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {name:22s} {len(html)//1024:>4d} KB")

    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DIST, "assets"))

    # favicon lives in src/assets/img/ and is copied with the rest of the assets

    # robots + sitemap
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n")
    print(f"\nBuilt → {DIST}")


if __name__ == "__main__":
    build()
