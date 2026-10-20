/* ==========================================================================
   KARKHANA — main.js
   Progressive enhancement only. Every page works without it.
   ========================================================================== */
(() => {
  "use strict";

  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------------
     1. Header, drawer, progress
     --------------------------------------------------------------------- */
  const hdr = $("#hdr");
  const burger = $("#burger");
  const drawer = $("#drawer");
  const progress = $("#progress");

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      if (hdr) hdr.classList.toggle("is-stuck", y > 24);
      if (progress) {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.width = h > 0 ? `${(y / h) * 100}%` : "0%";
      }
      const dock = $("#dock");
      if (dock) dock.classList.toggle("is-on", y > 620);
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function setDrawer(open) {
    if (!drawer || !burger) return;
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    burger.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("no-scroll", open);
  }
  burger?.addEventListener("click", () =>
    setDrawer(burger.getAttribute("aria-expanded") !== "true")
  );
  drawer?.addEventListener("click", (e) => {
    if (e.target.closest("a")) setDrawer(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && drawer?.classList.contains("is-open")) {
      setDrawer(false);
      burger?.focus();
    }
  });

  /* ---------------------------------------------------------------------
     2. Reveal on scroll
     --------------------------------------------------------------------- */
  const revealables = $$("[data-reveal]");
  if (revealables.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      revealables.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
      );
      revealables.forEach((el) => io.observe(el));
    }
  }

  /* ---------------------------------------------------------------------
     3. Image fade-in (LQIP → full)
     --------------------------------------------------------------------- */
  function hydrateImage(img) {
    if (img.dataset.hydrated) return;
    img.dataset.hydrated = "1";
    img.classList.add("is-loaded");
  }
  $$("img[loading]").forEach((img) => {
    if (img.complete && img.naturalWidth > 0) hydrateImage(img);
    else img.addEventListener("load", () => hydrateImage(img), { once: true });
  });
  window.addEventListener("load", () =>
    $$("img[loading]").forEach((img) => {
      if (img.complete && img.naturalWidth > 0) hydrateImage(img);
    })
  );

  /* ---------------------------------------------------------------------
     4. Count-up
     --------------------------------------------------------------------- */
  const counters = $$("[data-count]");
  if (counters.length) {
    const fmt = (n) => n.toLocaleString("en-US");
    const run = (el, target) => {
      const dur = 1100;
      const t0 = performance.now();
      // Update only the leading text node so a trailing <span> unit survives.
      const node = Array.from(el.childNodes).find(
        (n) => n.nodeType === 3 && n.textContent.trim().length
      );
      const tick = (t) => {
        const p = Math.min((t - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        const v = fmt(Math.round(target * eased));
        if (node) node.textContent = v;
        else el.textContent = v;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if (reduced || !("IntersectionObserver" in window)) {
      counters.forEach((el) => run(el, +el.dataset.count));
    } else {
      const cio = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          run(entry.target, +entry.target.dataset.count);
          cio.unobserve(entry.target);
        });
      }, { threshold: 0.4 });
      counters.forEach((el) => cio.observe(el));
    }
  }

  /* ---------------------------------------------------------------------
     5. Product filters
     --------------------------------------------------------------------- */
  const grid = $("#product-grid");
  if (grid) {
    const cards = $$(".p-card", grid);
    const countEl = $("#filter-count");
    $$(".filter").forEach((btn) => {
      btn.addEventListener("click", () => {
        const f = btn.dataset.filter;
        $$(".filter").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        let shown = 0;
        cards.forEach((card) => {
          const match = f === "All" || card.dataset.cat === f;
          card.classList.toggle("is-hidden", !match);
          if (match) {
            shown++;
            card.style.animation = "none";
            void card.offsetWidth;
            card.style.animation = "";
          }
        });
        if (countEl) countEl.textContent = `Showing ${shown} of ${cards.length}`;
      });
    });
  }

  /* ---------------------------------------------------------------------
     6. Accordion
     --------------------------------------------------------------------- */
  $$(".acc-trigger").forEach((tr) => {
    tr.addEventListener("click", () => {
      const open = tr.getAttribute("aria-expanded") === "true";
      tr.setAttribute("aria-expanded", String(!open));
    });
  });

  /* ---------------------------------------------------------------------
     7. Process index scrollspy
     --------------------------------------------------------------------- */
  const procLinks = $$("[data-proc-link]");
  if (procLinks.length) {
    const blocks = $$("[data-step-block]");
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const n = entry.target.id.replace("step-", "");
          procLinks.forEach((l) =>
            l.classList.toggle("is-active", l.dataset.procLink === n)
          );
        });
      },
      { rootMargin: "-20% 0px -65% 0px" }
    );
    blocks.forEach((b) => io.observe(b));
  }

  /* ---------------------------------------------------------------------
     8. Spec Builder
     --------------------------------------------------------------------- */
  const dataEl = $("#builder-data");
  if (dataEl) {
    const D = JSON.parse(dataEl.textContent);
    const state = {
      product: Object.keys(D.products)[0],
      fabric: "poly600",
      colour: "indigo",
      branding: "screen",
      hardware: "gunmetal",
      lining: "plain190",
    };
    const STEP_COUNT = 6;
    let step = 1;

    const el = {
      price: $("#sum-price"),
      name: $("#sum-name"),
      tier: $("#sum-tier"),
      specs: $("#sum-specs"),
      tierRows: $("#tier-rows"),
      lead: $("#sum-lead"),
      leadNote: $("#sum-lead-note"),
      prev: $("#builder-prev"),
      next: $("#builder-next"),
      count: $("#builder-count"),
    };

    const money = (n) =>
      "₹" + Math.round(n).toLocaleString("en-US");

    function parseLead(str) {
      const m = String(str).match(/(\d+)\D+(\d+)/);
      if (!m) return [20, 30];
      return [+m[1], +m[2]];
    }

    function compute() {
      const p = D.products[state.product];
      const f = D.fabrics[state.fabric];
      const b = D.branding[state.branding];
      const h = D.hardware[state.hardware];
      const l = D.linings[state.lining];
      const c = D.colours[state.colour];

      const unit =
        p.base * f.index + b.unit + h.unit + l.unit;
      const moq = Math.max(p.moq, b.moq, h.moq);
      const [pmin, pmax] = parseLead(p.lead);
      const leadMin = pmin + f.lead + b.lead + h.lead + l.lead;
      const leadMax = pmax + f.lead + b.lead + h.lead + l.lead;

      return { p, f, b, h, l, c, unit, moq, leadMin, leadMax };
    }

    function render() {
      const r = compute();
      const tiers = D.tiers.map((t) => ({
        ...t,
        price: r.unit * t.mult,
        feasible: t.qty >= r.moq,
      }));

      // headline = 500-tier price (or nearest feasible tier at/above 500)
      const head =
        tiers.find((t) => t.qty === 500) || tiers[tiers.length - 1];
      el.price.textContent = Math.round(head.price).toLocaleString("en-US");
      el.tier.textContent = head.label;
      el.name.textContent = r.p.name;

      el.specs.innerHTML = `
        <div class="spec spec-dense">
          <div class="spec-row"><dt>Body fabric</dt><dd>${r.f.name}<small>${r.f.gsm} · ${r.f.wr}</small></dd></div>
          <div class="spec-row"><dt>Colourway</dt><dd>${r.c.name}<small>Pantone ${r.c.pantone}</small></dd></div>
          <div class="spec-row"><dt>Branding</dt><dd>${r.b.name}<small>${money(b_setup(r.b))} setup</small></dd></div>
          <div class="spec-row"><dt>Hardware</dt><dd>${r.h.name}</dd></div>
          <div class="spec-row"><dt>Lining</dt><dd>${r.l.name}</dd></div>
          <div class="spec-row"><dt>Dimensions</dt><dd>${r.p.dims}</dd></div>
          <div class="spec-row"><dt>Capacity</dt><dd>${r.p.capacity} L</dd></div>
          <div class="spec-row"><dt>Weight</dt><dd>${r.p.weight.toFixed(2)} kg</dd></div>
          <div class="spec-row"><dt>Stitch density</dt><dd>9 SPI</dd></div>
          <div class="spec-row"><dt>MOQ</dt><dd class="hl">${r.moq} pcs</dd></div>
        </div>`;

      el.tierRows.innerHTML = tiers
        .map((t) => {
          const cls = t.qty === 500 ? "best-row" : "";
          const best = t.qty === 5000 ? "best" : "";
          const val = t.feasible
            ? Math.round(t.price).toLocaleString("en-US")
            : "—";
          const moqCell = t.feasible ? "✓" : `<span style="color:var(--madder)">${r.moq}</span>`;
          return `<tr class="${cls}"><td>${t.label}</td><td class="${best}">${val}</td><td>${moqCell}</td></tr>`;
        })
        .join("");

      el.lead.textContent = `${r.leadMin}–${r.leadMax} days`;
      el.leadNote.textContent =
        r.leadMin > 40
          ? "Extended — reflects a material or tooling lead on this configuration."
          : "Bulk production, after golden sample approval.";

      // option deltas
      $$("[data-delta='fabric']").forEach((n) => {
        const id = n.closest("[data-id]")?.dataset.id;
        const fab = D.fabrics[id];
        n.textContent =
          fab.index === 1 ? "Base" : `×${fab.index.toFixed(2)} material`;
      });

      // send-to-contact link
      const cta = $("#builder-send");
      if (cta) {
        const q = new URLSearchParams({
          product: r.p.name,
          fabric: r.f.name,
          colour: r.c.name,
          branding: r.b.name,
          hardware: r.h.name,
          lining: r.l.name,
          price: money(head.price),
          moq: String(r.moq),
          lead: `${r.leadMin}–${r.leadMax} days`,
        });
        cta.setAttribute("href", `contact.html?${q.toString()}`);
      }
    }

    function b_setup(b) {
      return b.setup;
    }

    // option handling
    $$("[data-group]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const group = btn.dataset.group;
        const id = btn.dataset.id;
        state[group] = id;
        $$(`[data-group="${group}"]`).forEach((b) =>
          b.setAttribute("aria-pressed", String(b === btn))
        );
        render();
      });
    });

    // steps
    function goStep(n) {
      step = Math.min(Math.max(n, 1), STEP_COUNT);
      $$(".builder-section").forEach((s) =>
        s.classList.toggle("is-active", s.dataset.section === String(step))
      );
      $$(".builder-step").forEach((s) => {
        const sn = +s.dataset.step;
        s.classList.toggle("is-active", sn === step);
        s.classList.toggle("is-done", sn < step);
        s.setAttribute("aria-selected", String(sn === step));
      });
      el.count.textContent = `Step ${step} of ${STEP_COUNT}`;
      el.prev.disabled = step === 1;
      el.next.textContent = step === STEP_COUNT ? "Finish" : "Next →";
    }
    el.prev?.addEventListener("click", () => goStep(step - 1));
    el.next?.addEventListener("click", () => {
      if (step === STEP_COUNT) {
        goStep(1);
        $(".summary")?.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
      } else goStep(step + 1);
    });
    $$(".builder-step").forEach((s) =>
      s.addEventListener("click", () => goStep(+s.dataset.step))
    );

    // initialise from product defaults
    const first = D.products[state.product];
    state.fabric = first.default_fabric;
    state.colour = first.default_colour;
    $$(`[data-group="fabric"]`).forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.id === state.fabric))
    );
    $$(`[data-group="colour"]`).forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.id === state.colour))
    );
    goStep(1);
    render();
  }

  /* ---------------------------------------------------------------------
     9. RFQ form
     --------------------------------------------------------------------- */
  const form = $("#rfq-form");
  if (form) {
    // prefill from the Spec Builder
    const params = new URLSearchParams(location.search);
    const map = {
      product: "f-spec",
      fabric: "f-spec",
      colour: "f-spec",
      branding: "f-spec",
      hardware: "f-spec",
      lining: "f-spec",
      price: "f-spec",
      moq: "f-spec",
      lead: "f-spec",
    };
    const specKeys = Object.keys(map);
    if (specKeys.some((k) => params.get(k))) {
      const ta = $("#f-spec");
      if (ta) {
        const lines = [];
        const label = {
          product: "Bag", fabric: "Fabric", colour: "Colourway", branding: "Branding",
          hardware: "Hardware", lining: "Lining", price: "Indicative price",
          moq: "MOQ", lead: "Lead time",
        };
        specKeys.forEach((k) => {
          const v = params.get(k);
          if (v) lines.push(`${label[k]}: ${v}`);
        });
        ta.value = lines.join("\n");
      }
    }

    const setError = (input, msg) => {
      const box = document.querySelector(`[data-error-for="${input.id}"]`);
      input.setAttribute("aria-invalid", msg ? "true" : "false");
      if (box) box.textContent = msg || "";
    };

    const validate = (input) => {
      const v = input.value.trim();
      if (input.hasAttribute("required") && !v) {
        setError(input, "Required");
        return false;
      }
      if (input.type === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
        setError(input, "Check this email address");
        return false;
      }
      setError(input, "");
      return true;
    };

    $$("input, select, textarea", form).forEach((input) => {
      input.addEventListener("blur", () => validate(input));
      input.addEventListener("input", () => {
        if (input.getAttribute("aria-invalid") === "true") validate(input);
      });
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let ok = true;
      let firstBad = null;
      $$("input, select, textarea", form).forEach((input) => {
        if (!validate(input) && ok) {
          ok = false;
          firstBad = input;
        }
      });
      if (!ok) {
        firstBad?.focus();
        firstBad?.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
        return;
      }
      const success = $("#form-success");
      success?.classList.add("is-on");
      form.querySelector(".stack")?.setAttribute("hidden", "hidden");
      success?.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
    });
  }
})();
