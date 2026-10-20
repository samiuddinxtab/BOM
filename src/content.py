"""KARKHANA — site content model.

Every product, fabric and process figure here is a real manufacturing value
(GSM, denier, SPI, AQL, MOQ, lead time) rather than marketing copy. The site
renders from this single source so the Spec Builder and the catalogue can
never disagree.
"""

BRAND = {
    "name": "Karkhana",
    "legal": "Karkhana Custom Bag Works",
    "tagline": "Made to your spec. Built to survive the spec.",
    "established": 2009,
    "works": "MIE Part B, Bahadurgarh",
    "works_full": "Plot 214, MIE Part B, Bahadurgarh, Haryana 124507",
    "studio": "Okhla Phase II, New Delhi 110020",
    "email": "works@karkhana.in",
    "email_export": "export@karkhana.in",
    "phone": "+91 98110 44207",
    "hours": "Mon–Sat · 09:30 – 18:30 IST",
    "gst": "06AABCK4821M1ZP",
}

NAV = [
    ("index.html", "Home", "01"),
    ("products.html", "Products", "02"),
    ("customise.html", "Spec Builder", "03"),
    ("process.html", "Process", "04"),
    ("works.html", "The Works", "05"),
    ("industries.html", "Who We Build For", "06"),
    ("contact.html", "Enquire", "07"),
]

# ---------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------
CATEGORIES = ["All", "School", "College", "Business", "Travel", "Sports", "Corporate"]

PRODUCTS = [
    {
        "slug": "kora-22",
        "name": "Kora 22\" School Backpack",
        "cat": "School",
        "img": "school-backpack",
        "blurb": "A spine-engineered school bag with a moulded EVA back panel, load-lifting S-curve harness and reflective piping at every night-visible edge.",
        "capacity": 22,
        "weight": 0.62,
        "moq": 100,
        "lead": "22–28 days",
        "base": 285,
        "dims": "430 × 300 × 140 mm",
        "default_fabric": "poly600",
        "default_colour": "indigo",
        "badge": "EVA back panel",
        "features": [
            "Moulded EVA back panel with airflow channel",
            "S-curve padded harness, 38 mm webbing",
            "Reflective piping on 3 edges (BS EN 17353)",
            "Reinforced 600D base with bar-tack corners",
            "Zippered front pocket + side mesh bottle pocket",
        ],
    },
    {
        "slug": "vidyut-30",
        "name": "Vidyut 30\" College Backpack",
        "cat": "College",
        "img": "college-backpack",
        "blurb": "A 30-litre day pack that carries a 16-inch laptop, a full day's books and a lunch break without moving off the shoulders.",
        "capacity": 30,
        "weight": 0.86,
        "moq": 100,
        "lead": "25–30 days",
        "base": 465,
        "dims": "460 × 320 × 180 mm",
        "default_fabric": "poly600",
        "default_colour": "teal",
        "badge": "16\" laptop sleeve",
        "features": [
            "Suspended 16-inch laptop sleeve with divider",
            "Full-width zip opening to 180°",
            "Front organiser with 6 pen loops",
            "Tarpaulin-reinforced waterproof base",
            "Stitched-away trolley pass-through",
        ],
    },
    {
        "slug": "ledger-18",
        "name": "Ledger 18\" Business Backpack",
        "cat": "Business",
        "img": "laptop-backpack",
        "blurb": "A clean, architectural commuter pack. Concealed zips, a hidden passport pocket and a trolley sleeve that disappears when you do not need it.",
        "capacity": 18,
        "weight": 0.74,
        "moq": 150,
        "lead": "28–34 days",
        "base": 690,
        "dims": "410 × 290 × 130 mm",
        "default_fabric": "cordura",
        "default_colour": "black",
        "badge": "Quick-access top",
        "features": [
            "Quick-access top pocket with key leash",
            "Padded 15-inch laptop bay, 8 mm foam",
            "Hidden RFID passport pocket",
            "Tonal matte hardware, no visible branding",
            "Luggage pass-through, webbing only",
        ],
    },
    {
        "slug": "dossier-12",
        "name": "Dossier 12\" File Bag",
        "cat": "Business",
        "img": "file-bag",
        "blurb": "A soft-sided document carrier for architects, surveyors and law firms. Expandable gusset, full-length two-way zip, brass hardware.",
        "capacity": 12,
        "weight": 0.58,
        "moq": 200,
        "lead": "24–30 days",
        "base": 420,
        "dims": "400 × 280 × 100 mm",
        "default_fabric": "canvas12",
        "default_colour": "olive",
        "badge": "Expandable gusset",
        "features": [
            "Expandable gusset, +6 cm depth",
            "Full-length two-way zip with lock slider",
            "Interior A4 document bay and 3 sleeves",
            "Detachable shoulder strap with pad",
            "Antique brass hardware, leather-look trim",
        ],
    },
    {
        "slug": "dhoop-45",
        "name": "Dhoop 45L Duffle & Gym Bag",
        "cat": "Sports",
        "img": "duffle-bag",
        "blurb": "A 45-litre gym and weekender duffle with a ventilated shoe compartment, welded tarpaulin base and webbing handles that survive airport handling.",
        "capacity": 45,
        "weight": 1.15,
        "moq": 100,
        "lead": "22–28 days",
        "base": 540,
        "dims": "580 × 300 × 300 mm",
        "default_fabric": "poly600",
        "default_colour": "black",
        "badge": "Shoe compartment",
        "features": [
            "Ventilated base shoe compartment, mesh",
            "Welded tarpaulin base, wipe-clean",
            "38 mm webbing handles with grip pad",
            "End pockets, both sides",
            "Lockable main zip with carabiner loop",
        ],
    },
    {
        "slug": "gadi-40",
        "name": "Gadi 40L Soft Trolley",
        "cat": "Travel",
        "img": "trolley-bag",
        "blurb": "A soft-sided two-wheel trolley that keeps the silhouette of a cabin bag while giving a school bag's flexibility of use.",
        "capacity": 40,
        "weight": 2.40,
        "moq": 150,
        "lead": "30–38 days",
        "base": 1180,
        "dims": "550 × 350 × 230 mm",
        "default_fabric": "poly600",
        "default_colour": "teal",
        "badge": "Inline 2-wheel",
        "features": [
            "Inline 2-wheel system, 70 mm, silent run",
            "Telescopic handle, 3 stops, alloy tube",
            "Top + side carry handles, webbing wrapped",
            "Front organiser panel, zip access",
            "Compression straps on three sides",
        ],
    },
    {
        "slug": "sahi-40",
        "name": "Sahi 40L Travel Backpack",
        "cat": "Travel",
        "img": "travel-backpack",
        "blurb": "A cabin-legal 40-litre travel pack with load-lifter straps, a padded hip belt and a stowable sleeping-bag compartment.",
        "capacity": 40,
        "weight": 1.05,
        "moq": 100,
        "lead": "24–30 days",
        "base": 720,
        "dims": "520 × 320 × 220 mm",
        "default_fabric": "cordura",
        "default_colour": "olive",
        "badge": "Cabin legal",
        "features": [
            "Load-lifter top straps + side compression",
            "Padded, removable hip belt",
            "Stowable sleeping-bag compartment",
            "Triclimate drawstring collar, 35 L expand",
            "Rain cover, packable, in base pocket",
        ],
    },
    {
        "slug": "milap-9",
        "name": "Milap 9L Conference & Gift Tote",
        "cat": "Corporate",
        "img": "corporate-totes",
        "blurb": "A 9-litre conference tote in heavy cotton canvas, 300 gsm self-fabric base and gusset, for welcome kits, event drops and client gifting.",
        "capacity": 9,
        "weight": 0.32,
        "moq": 300,
        "lead": "18–24 days",
        "base": 165,
        "dims": "380 × 340 × 100 mm",
        "default_fabric": "canvas12",
        "default_colour": "ecru",
        "badge": "300 gsm base",
        "features": [
            "300 gsm self-fabric base and gusset",
            "Internal 300 gsm padded divider",
            "Hidden interior zip pocket",
            "Bar-tacked 70 cm handles",
            "Polybag or box packaging options",
        ],
    },
    {
        "slug": "kalam-06",
        "name": "Kalam 6\" Sleeve & Organiser",
        "cat": "Business",
        "img": "laptop-backpack",
        "blurb": "A 6-litre felt and waxed-canvas sleeve set for documents, cables and the small things that get lost in a larger bag.",
        "capacity": 6,
        "weight": 0.28,
        "moq": 250,
        "lead": "20–26 days",
        "base": 190,
        "dims": "350 × 250 × 70 mm",
        "default_fabric": "waxcanvas",
        "default_colour": "olive",
        "badge": "2-piece set",
        "features": [
            "Sleeve + matching organiser pouch",
            "2 mm closed-cell foam padding",
            "YKK-equivalent reverse coil zip",
            "Microfibre lining, wipe-clean",
            "Retail-ready hang tag option",
        ],
    },
]

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
FABRICS = [
    {
        "id": "poly600",
        "name": "600D Polyester",
        "sub": "Virgin / recycled yarn",
        "gsm": "210 g/m²",
        "wr": "5 kPa",
        "index": 1.00,
        "lead": 0,
        "note": "The default for high-volume school and college bags. 39.6% of India's bag material mix. Woven in Erode and Tiruppur, dyed in-house.",
        "cols": ["#2A3350", "#1A1D22", "#3A4A5C", "#4A3B2E"],
    },
    {
        "id": "rpet",
        "name": "600D Recycled RPET",
        "sub": "GRS certified",
        "gsm": "200 g/m²",
        "wr": "4 kPa",
        "index": 1.22,
        "lead": 8,
        "note": "Post-consumer bottle feedstock, GRS chain-of-custody, 32% lower CO2e than virgin yarn. Minimum 8 days for chain-of-custody allocation.",
        "cols": ["#243044", "#3E4A3A", "#5A5A58", "#2F3A46"],
    },
    {
        "id": "cordura",
        "name": "1000D Cordura Nylon",
        "sub": "Ballistic weave",
        "gsm": "340 g/m²",
        "wr": "9 kPa",
        "index": 1.38,
        "lead": 6,
        "note": "Abrasion and tear resistance for luggage and laptop categories. We hold a 6-week rolling buffer on cordura stock.",
        "cols": ["#2B2F36", "#1C2A22", "#43301F", "#31343B"],
    },
    {
        "id": "ripstop",
        "name": "210D Ripstop Nylon",
        "sub": "Silicone/PU coated",
        "gsm": "95 g/m²",
        "wr": "6 kPa",
        "index": 1.12,
        "lead": 4,
        "note": "Light, packable, used for stuff-sacs, rain covers and lined panels where weight matters more than structure.",
        "cols": ["#D8D3C6", "#B8503A", "#2E4A3C", "#31343B"],
    },
    {
        "id": "ballistic",
        "name": "1680D Ballistic Nylon",
        "sub": "Heavy-duty, coated",
        "gsm": "480 g/m²",
        "wr": "14 kPa",
        "index": 1.55,
        "lead": 8,
        "note": "For export and outdoor programs where abrasion life matters more than unit cost. Heaviest body fabric we run.",
        "cols": ["#1E2126", "#2A2E26", "#3A3527", "#14161A"],
    },
    {
        "id": "canvas12",
        "name": "12oz Cotton Canvas",
        "sub": "Undyed / piece-dyed",
        "gsm": "407 g/m²",
        "wr": "1 kPa",
        "index": 1.30,
        "lead": 4,
        "note": "A 3/1 twill that softens with use and takes piece-dye beautifully. Requires 4 days extra for a dye batch.",
        "cols": ["#D9CFB8", "#5B6340", "#2B3239", "#8A6A3C"],
    },
    {
        "id": "waxcanvas",
        "name": "10oz Waxed Canvas",
        "sub": "Wax finish, cotton duck",
        "gsm": "340 g/m²",
        "wr": "3 kPa",
        "index": 1.45,
        "lead": 6,
        "note": "Waxed cotton duck. Re-waxable, ages visibly, and photographs well. Not recommended for print — use leather patch or embroidery.",
        "cols": ["#6E5C3E", "#3A3B34", "#7A4A2C", "#26333A"],
    },
    {
        "id": "nonwoven",
        "name": "80 GSM Non-woven PP",
        "sub": "Spunbond / laminate",
        "gsm": "80 g/m²",
        "wr": "2 kPa",
        "index": 0.72,
        "lead": -2,
        "note": "The lowest cost route. Used for promotional totes, drawstring kits and short-life event stock.",
        "cols": ["#E6E2D8", "#33404F", "#7C4B3A", "#2E3B2E"],
    },
]

COLOURS = [
    {"id": "indigo",  "name": "Dye-vat Indigo",  "body": "#243259", "accent": "#E9A319", "pantone": "19-4052 / 13-0647"},
    {"id": "black",   "name": "Jet Black",      "body": "#1A1D22", "accent": "#4A4F58", "pantone": "19-4005 / Cool Gray 9"},
    {"id": "teal",    "name": "Peacock Teal",   "body": "#1E4A52", "accent": "#E07A3C", "pantone": "18-4728 / 15-1345"},
    {"id": "olive",   "name": "Field Olive",    "body": "#4C5138", "accent": "#C9A227", "pantone": "19-0622 / 14-0957"},
    {"id": "ecru",    "name": "Raw Ecru",       "body": "#D9CFB8", "accent": "#3A3A34", "pantone": "11-0605 / Black 4"},
    {"id": "royal",   "name": "Royal Blue",     "body": "#1C3C86", "accent": "#E9C14A", "pantone": "19-4050 / 14-0756"},
    {"id": "rust",    "name": "Rust & Madder",  "body": "#8A3E28", "accent": "#E4D6B8", "pantone": "19-1337 / 11-0605"},
    {"id": "forest",  "name": "Deep Forest",    "body": "#22402E", "accent": "#B87333", "pantone": "19-6052 / 17-1340"},
]

BRANDING = [
    {"id": "screen",  "name": "Screen Print",     "sub": "Up to 4 colours",   "setup": 2500,  "unit": 18, "moq": 100, "lead": 0},
    {"id": "hdscreen","name": "HD Screen Print",  "sub": "Fine detail",       "setup": 3500,  "unit": 26, "moq": 100, "lead": 3},
    {"id": "embroid", "name": "Embroidery",       "sub": "Up to 5,000 stitches","setup": 1800, "unit": 34, "moq": 150, "lead": 3},
    {"id": "woven",   "name": "Woven Label",      "sub": "Satin / damask",    "setup": 4200,  "unit": 22, "moq": 200, "lead": 5},
    {"id": "patch",   "name": "Leather Patch",    "sub": "PU, stitched",      "setup": 5500,  "unit": 38, "moq": 200, "lead": 4},
    {"id": "badge",   "name": "Metal Badge",      "sub": "Antique / matte",   "setup": 9000,  "unit": 52, "moq": 300, "lead": 7},
    {"id": "deboss",  "name": "Deboss / Emboss",  "sub": "PU leather",        "setup": 6000,  "unit": 44, "moq": 250, "lead": 5},
    {"id": "heat",    "name": "Heat Transfer",    "sub": "DTF, full colour",  "setup": 1200,  "unit": 12, "moq": 100, "lead": 2},
]

HARDWARE = [
    {"id": "gunmetal", "name": "Matte Gunmetal", "sub": "Standard finish", "unit": 0,  "moq": 100, "lead": 0},
    {"id": "black",    "name": "Satin Black",    "sub": "Anti-glare",      "unit": 4,  "moq": 100, "lead": 2},
    {"id": "brass",    "name": "Antique Brass",  "sub": "Vintage tone",    "unit": 6,  "moq": 150, "lead": 3},
    {"id": "nickel",   "name": "Nickel",         "sub": "Bright finish",   "unit": 8,  "moq": 150, "lead": 3},
    {"id": "custom",   "name": "Custom Anodised","sub": "Pantone matched", "unit": 22, "moq": 500, "lead": 9},
]

LININGS = [
    {"id": "plain190", "name": "190T Polyester",  "sub": "Plain, standard",  "unit": 0,  "lead": 0},
    {"id": "printed",  "name": "210D Printed",    "sub": "Custom artwork",   "unit": 14, "lead": 7},
    {"id": "rpetlin",  "name": "Recycled 150D",   "sub": "RPET lining",      "unit": 18, "lead": 6},
    {"id": "tpu",      "name": "TPU Coated",      "sub": "Water-resistant",  "unit": 26, "lead": 5},
]

# ---------------------------------------------------------------------------
# Process
# ---------------------------------------------------------------------------
PROCESS = [
    {
        "n": "01", "title": "Brief & Feasibility", "dur": "1–2 days",
        "body": "You send a sketch, a reference photo, a tech pack, or a bag you already like. We read it for buildability — not whether we like it, but whether our machines can hold it, and at what cost.",
        "meta": ["No obligation", "24-hour acknowledgement"],
    },
    {
        "n": "02", "title": "Specification & Costing", "dur": "2–4 days",
        "body": "You get a manufacturability review: proposed materials with GSM and denier, a graded size sheet, a costed price band across three volume tiers, and a lead time we will hold to in writing.",
        "meta": ["Price band, not a list price", "Written lead time"],
    },
    {
        "n": "03", "title": "Pattern & First Sample", "dur": "7–10 days",
        "body": "Our pattern room grades the design to your size chart, nests the panels in CAD and cuts a first sample. This round proves structure, proportion and hand-feel. Expect it to be approximately right.",
        "meta": ["CAD nested", "Photo + video record"],
    },
    {
        "n": "04", "title": "Revisions & Golden Sample", "dur": "7 days / round",
        "body": "Two refinement rounds are included. When you sign the golden sample in writing, that physical bag becomes the production standard — every measurement, seam placement and colour is matched against it on the floor.",
        "meta": ["2 rounds included", "Signed golden sample"],
    },
    {
        "n": "05", "title": "Material Procurement", "dur": "7–14 days",
        "body": "Body fabric is cut from Erode and Tiruppur mills, zippers and hardware from Jalandhar, trims from Bahadurgarh. Every roll is inspected on arrival for GSM, width, shade and defects before it is released to cutting.",
        "meta": ["Roll-by-roll inspection", "Shade band approved at step 2"],
    },
    {
        "n": "06", "title": "Bulk Production", "dur": "20–32 days",
        "body": "Cutting, stitching, branding, assembly and packing run across eight lines with live work-in-progress reporting. You can ask for photographs of your batch at any point in the run.",
        "meta": ["8 production lines", "Live WIP reporting", "In-house branding"],
    },
    {
        "n": "07", "title": "QC & Pre-Shipment Inspection", "dur": "2–3 days",
        "body": "Material inspection, in-line checks and a final audit. AQL 2.5 for major defects and 4.0 for minor, on ANSI/ASQ Z1.4. Third-party inspections from SGS, Bureau Veritas or your own auditor are welcome at any stage.",
        "meta": ["AQL 2.5 / 4.0", "Third-party welcome"],
    },
    {
        "n": "08", "title": "Dispatch & Aftercare", "dur": "5–12 days",
        "body": "Export packing, carton marks, barcodes, country-of-origin labelling and shipping documents. Your production file — patterns, shade references, trims — is archived so a repeat order next season is a re-run, not a re-design.",
        "meta": ["Air, sea, land", "DDP on request", "Repeat-order archive"],
    },
]

# ---------------------------------------------------------------------------
# Capability
# ---------------------------------------------------------------------------
CAPABILITY = [
    {
        "n": "01", "title": "Design & Pattern Room",
        "body": "Four industrial designers and six pattern makers. You get a graded size sheet, a tech pack and a nesting layout — not just a photo of a bag someone else made.",
        "stat": "14 in-house", "statLabel": "designers & pattern makers",
    },
    {
        "n": "02", "title": "Eight Production Lines",
        "body": "Lockstitch, overlock, bartack, buttonhole, high-frequency welding and foam lamination. All under one roof in Bahadurgarh, so a bag is never split across four vendors.",
        "stat": "8 lines", "statLabel": "single-roof production",
    },
    {
        "n": "03", "title": "In-House Branding",
        "body": "Six-colour screen printing, 40-head embroidery, heat transfer, badge stamping and label sewing. Setup is done here, which is why a 100-piece run can carry a real woven label.",
        "stat": "6 + 40", "statLabel": "print & embroidery heads",
    },
    {
        "n": "04", "title": "Capacity That Holds",
        "body": "Two hundred and fifty thousand units a month across four shifts. We quote against a live capacity board, not a theoretical ceiling, so lead times mean something.",
        "stat": "250,000", "statLabel": "units per month",
    },
]

MATERIALS = [
    {
        "name": "Polyester", "sub": "Virgin & recycled yarn",
        "body": "210–340 g/m² woven and coated polyester from Tiruppur and Erode mills. India's default bag input at 39.6% of material mix.",
        "cols": ["#2A3350", "#1A1D22", "#3A4A5C"],
    },
    {
        "name": "Nylon", "sub": "210D – 1680D",
        "body": "Ripstop, cordura and ballistic weaves, silicone and PU coated. Abrasion-tested for luggage and export programs.",
        "cols": ["#31343B", "#1C2A22", "#43301F"],
    },
    {
        "name": "Cotton Canvas", "sub": "8oz – 16oz",
        "body": "3/1 twill, piece-dyed and washed. Softens with use, and the only fabric we piece-dye to a Pantone.",
        "cols": ["#D9CFB8", "#5B6340", "#2B3239"],
    },
    {
        "name": "Non-woven PP", "sub": "60 – 120 GSM",
        "body": "Spunbond and laminate for promotional, event and short-life programmes where unit cost governs.",
        "cols": ["#E6E2D8", "#33404F", "#2E3B2E"],
    },
    {
        "name": "Foam & Padding", "sub": "EVA, PU, PE foam",
        "body": "Moulded EVA back panels, closed-cell cushioning and high-density PU. Contoured in-house for spinal load distribution.",
        "cols": ["#2A2E34", "#4A4F55", "#1E2126"],
    },
    {
        "name": "Hardware", "sub": "Buckles, D-rings, rivets",
        "body": "YKK-equivalent zippers, alloy buckles, D-rings, eyelets and rivets from Ludhiana and Jalandhar, in four standard finishes.",
        "cols": ["#8A9099", "#3A3F46", "#B08D57"],
    },
    {
        "name": "Webbing & Thread", "sub": "20 – 38 mm",
        "body": "Polyester webbing from 20 to 38 mm, Tex 40–70 thread, bonded nylon for load points, bartack reinforcement as standard.",
        "cols": ["#2E4A3C", "#1F2126", "#B8503A"],
    },
    {
        "name": "Lining", "sub": "190T – 210D",
        "body": "Plain, printed and recycled linings. Custom artwork is printed on-site and matched to your brand palette.",
        "cols": ["#E2DDD0", "#2C4374", "#3A3F46"],
    },
]

CERTIFICATIONS = [
    ("ISO 9001:2015", "Quality management system, certified since 2011"),
    ("ISO 14001:2015", "Environmental management, certified since 2019"),
    ("Sedex / SMETA 4-Pillar", "Social compliance audit, renewed every 12 months"),
    ("BSCI", "Business Social Compliance Initiative, current"),
    ("GRS 4.0", "Global Recycled Standard for RPET chain of custody"),
    ("OEKO-TEX Standard 100", "Class II certified lining and thread"),
    ("REACH / CPSIA / Prop 65", "Tested on request for EU, US and CA markets"),
    ("FSC", "FSC-certified export packaging and cartons"),
]

MACHINES = [
    ("Industrial lockstitch", "1,240 machines", "Cut, stitch and topstitch"),
    ("Overlock / serger", "180 machines", "Seam finishing, 4–5 thread"),
    ("Bartack & buttonhole", "96 machines", "Load-point reinforcement"),
    ("CAD cutting & nesting", "4 Gerber lines", "Marker efficiency, 88% average"),
    ("Screen printing carousel", "6 colour stations", "Up to 6 colours per pass"),
    ("Embroidery", "40-head × 6 machines", "Up to 5,000 stitches"),
    ("High-frequency welding", "5 presses", "TPU and tarpaulin seams"),
    ("Foam lamination & contouring", "3 presses", "EVA back panels, 3D foam"),
]

# ---------------------------------------------------------------------------
# Industries
# ---------------------------------------------------------------------------
INDUSTRIES = [
    {
        "icon": "school", "title": "Schools & Institutions",
        "body": "Annual replacement cycles, house colours, student name labels and batch delivery into a fixed academic calendar. We hold your shade band so year three matches year one.",
        "tags": ["House colours", "Name labels", "Batch delivery"],
    },
    {
        "icon": "college", "title": "Colleges & Campuses",
        "body": "Laptop-ready day packs for a student population that cares about how a bag looks. Faster sampling, lower MOQ per colour, and repeat runs on the same tooling.",
        "tags": ["Laptop-ready", "Campus drops", "Reorder file"],
    },
    {
        "icon": "corp", "title": "Corporates & IT",
        "body": "Welcome kits, conference totes, employee onboarding and client gifting. Unbranded or branded, with barcode labelling and internal packaging your logistics team can handle.",
        "tags": ["Welcome kits", "Barcodes", "Client gifting"],
    },
    {
        "icon": "dtc", "title": "D2C & Retail Brands",
        "body": "You bring the design, we bring the manufacturing. Small first runs to test a colourway, then scale to thousands on the same pattern, trims and shade references.",
        "tags": ["Small first runs", "Scale to 10k", "Colorways"],
    },
    {
        "icon": "export", "title": "Export & Distribution",
        "body": "Export-ready packing, DDP on request, REACH and Prop 65 documentation, and packing lists that clear customs without a follow-up call.",
        "tags": ["DDP", "REACH / Prop 65", "Carton marks"],
    },
    {
        "icon": "promo", "title": "Promotional & Gifting",
        "body": "Low MOQ on totes, drawstrings and kit bags, with printing, labels and packaging handled under one purchase order.",
        "tags": ["MOQ 100", "One PO", "Full packaging"],
    },
]

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
FAQ = [
    {
        "q": "What is the minimum order quantity?",
        "a": "100 pieces per style for standard constructions, from 150 for full-custom patterns, and 300 where branding needs its own tooling such as a metal badge. We will not quote a MOQ we cannot hold — if your volume is 60, we would rather tell you now than discover it in week three.",
    },
    {
        "q": "How long does sampling actually take?",
        "a": "Seven to ten working days for a first sample from an existing pattern, and fifteen to twenty-five where the structure is new and a cutting die has to be made. Two refinement rounds are included before the golden sample. Bulk production runs 20 to 32 days after that approval.",
    },
    {
        "q": "Do you sign an NDA before we share our design?",
        "a": "Yes, before the brief is opened. Our NDA is mutual, and we will work to a design ownership clause that assigns the product rights to you on final payment, in writing, before tooling is cut.",
    },
    {
        "q": "Can you match a Pantone colour?",
        "a": "We can, with one honest caveat: only on a dyeable fabric. Polyester and nylon are solution-dyed or piece-dyed, and a Pantone match on 600D polyester needs a lab dip and a shade band approved against a physical swatch. Canvas can be piece-dyed to Pantone reliably. We quote a lab dip rather than promise a match off a screen.",
    },
    {
        "q": "Which compliance documents can you support?",
        "a": "ISO 9001:2015, ISO 14001:2015, Sedex/SMETA 4-Pillar and BSCI are current and maintained. GRS and OEKO-TEX apply to specific material routes and are confirmed at RFQ stage rather than claimed blanket-style. REACH, CPSIA and Prop 65 testing is arranged through a third-party lab on request — we will not put a certificate on a product the test does not cover.",
    },
    {
        "q": "Can you ship DDP to our warehouse?",
        "a": "Yes, for most destinations, with a DDP or DAP quotation as standard on export orders. We handle customs clearance in-house through our CHA and pass the landed cost through without a margin on the freight.",
    },
    {
        "q": "Do we receive a tech pack?",
        "a": "Every project, without exception. You get a graded size sheet with tolerances, a bill of materials with fabric GSM and hardware specs, a stitch map, a branding placement sheet, and a nesting layout. The tech pack is yours — it is also what lets another factory make the bag if you ever want a second source.",
    },
    {
        "q": "What happens on a repeat order?",
        "a": "We archive your patterns, shade band, trims, labels and packaging files. A repeat order is a re-run against the golden sample, so a bag made in 2026 and a bag made in 2029 come out of the same shade band. That archive is why our second-year pricing is usually better than our first.",
    },
]

# ---------------------------------------------------------------------------
# Pricing model (shared by Spec Builder)
# ---------------------------------------------------------------------------
TIERS = [
    {"qty": 100,   "label": "100",   "mult": 1.18},
    {"qty": 300,   "label": "300",   "mult": 1.10},
    {"qty": 500,   "label": "500",   "mult": 1.00},
    {"qty": 1000,  "label": "1,000", "mult": 0.92},
    {"qty": 5000,  "label": "5,000", "mult": 0.80},
    {"qty": 10000, "label": "10,000", "mult": 0.72},
]
