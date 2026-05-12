from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Inches(0.85)
section.bottom_margin = Inches(0.85)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x1A, 0x1A, 0x2E)
BLUE   = RGBColor(0x1F, 0x77, 0xB4)
ORANGE = RGBColor(0xD6, 0x62, 0x00)
RED    = RGBColor(0xD6, 0x27, 0x28)
GRAY   = RGBColor(0x55, 0x55, 0x55)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

def set_font(run, name="Calibri", size=11, bold=False, italic=False, color=None):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def add_para(text="", style="Normal", align=WD_ALIGN_PARAGRAPH.LEFT,
             space_before=0, space_after=6):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        p.add_run(text)
    return p

def shade_cell(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        if val:
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:val"),   val.get("val",   "single"))
            el.set(qn("w:sz"),    val.get("sz",    "4"))
            el.set(qn("w:space"), val.get("space", "0"))
            el.set(qn("w:color"), val.get("color", "auto"))
            borders.append(el)
    tcPr.append(borders)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER BAND
# ══════════════════════════════════════════════════════════════════════════════
tbl = doc.add_table(rows=1, cols=1)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.style     = "Table Grid"
cell = tbl.cell(0, 0)
shade_cell(cell, "1A1A2E")

p = cell.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after  = Pt(4)
r = p.add_run("MERIDIAN TECHNOLOGIES")
set_font(r, size=9, bold=True, color=RGBColor(0x88, 0xBB, 0xDD))

p2 = cell.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after  = Pt(10)
r2 = p2.add_run("Annual Board Strategic Review  |  Opening Remarks  |  Catherine Park, CEO")
set_font(r2, size=8, color=RGBColor(0xCC, 0xCC, 0xCC))

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# HEADLINE
# ══════════════════════════════════════════════════════════════════════════════
p = add_para(space_before=2, space_after=4)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Meridian has a profitable foundation and a narrowing window.")
set_font(r, size=16, bold=True, color=NAVY)

p2 = add_para(space_before=0, space_after=14)
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run(
    "The enterprise franchise is real. The AI transition is urgent. "
    "The board's alignment on three decisions will determine the next chapter."
)
set_font(r2, size=11, italic=True, color=GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# FRAMING PARAGRAPH
# ══════════════════════════════════════════════════════════════════════════════
p = add_para(space_before=0, space_after=12)
r = p.add_run(
    "I have spent my first year listening, diagnosing, and making early moves — "
    "segment P&Ls, the Helio acquisition, Copilot GA. I want to use this session "
    "to be direct with the board about where we are, what the three biggest issues "
    "are, and what I need from you today."
)
set_font(r, size=11, color=NAVY)

# ══════════════════════════════════════════════════════════════════════════════
# CHART
# ══════════════════════════════════════════════════════════════════════════════
p_chart = add_para(space_before=0, space_after=4)
p_chart.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_picture("/home/user/Claude-session/meridian/board_chart.png", width=Inches(6.2))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

p_cap = add_para(space_before=2, space_after=16)
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap = p_cap.add_run(
    "Exhibit 1 — The Core Strategic Tension: profitability expanding while growth decelerates "
    "and GTM efficiency erodes. Source: Meridian internal data, 2022Q1–2025Q4."
)
set_font(r_cap, size=8, italic=True, color=GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# ISSUE BLOCKS  (3-row table per issue)
# ══════════════════════════════════════════════════════════════════════════════
issues = [
    {
        "number": "01",
        "label":  "AI IS EXISTENTIAL — AND WE ARE STILL EARLY",
        "body": (
            "The entire collaboration software category is repricing around agentic AI. "
            "We shipped Copilot to GA in September 2025. We ended the year with 710 paying seats "
            "and ~$3.5M in Copilot ARR — real proof of concept, but less than 1% of revenue. "
            "The enterprise governance suite — the feature regulated customers need to standardize "
            "on Copilot — is our Q1 2026 priority. Until it ships, our most valuable customers "
            "cannot fully commit. Meanwhile Atlassian announced agentic Jira last month and will "
            "be in our enterprise deals more directly than before."
        ),
        "evidence": [
            "710 paying Copilot seats at year-end vs. zero twelve months prior; 44% attach rate on enterprise renewals in Q4 (target: 40%)",
            "Asana shipped full agent suite November 2025; Monday now larger than Meridian by ARR; ClearAI raised $120M at $1B+ valuation",
            "31% of engineering open-ends cited 'roadmap thrash' — three AI pivots in 18 months — as top frustration (Employee Survey, Oct 2025)",
            "CPO: net engineering hires in 2026 will be ~25, vs. 80 assumed in the plan — execution capacity is constrained",
        ],
        "color_hex": "1F77B4",
        "color_rgb": BLUE,
    },
    {
        "number": "02",
        "label":  "TWO OF THREE SEGMENTS ARE BROKEN — GROWTH DEPENDS ON 140 LOGOS",
        "body": (
            "SMB ARR declined 23% in 2025. NRR is 84%. Gross logo churn is 22% annually. "
            "Mid-market — our largest segment at 47% of ARR — grew only 6% with NRR compressed "
            "from 115% (2022) to 102% (Q4 2025). Our entire growth story now rests on "
            "approximately 140 enterprise customers. The GTM efficiency numbers confirm the "
            "problem: magic number crossed below 1.0 in Q2 2025 and CAC payback has risen "
            "from 18 to 22 months. We are spending more on sales and marketing than we are "
            "generating in new ARR."
        ),
        "evidence": [
            "SMB: ARR fell from $68M (Q4 2024) to $52M (Q4 2025); NRR 84%; gross logo churn 22.1% annualized",
            "Mid-market NRR: 115% in 2022 → 102% in Q4 2025; primary cause is customers demanding AI features bundled at no cost",
            "Enterprise: NRR 125%, ARR +21% YoY — the single healthy segment, representing 40% of total ARR",
            "Magic number 0.92 (Q4 2025), down from 1.20 eighteen months ago; CAC payback 22.4 months vs. 18.2 months",
        ],
        "color_hex": "D66200",
        "color_rgb": ORANGE,
    },
    {
        "number": "03",
        "label":  "EXECUTION CAPACITY IS THE BINDING CONSTRAINT",
        "body": (
            "We are running a platform transition, a business model shift to consumption pricing, "
            "an acquisition integration, a microservices refactor, and a segment reorganization — "
            "simultaneously. In 2025, 6 of 12 roadmap commitments slipped one quarter, two were "
            "deferred outright. Engineering net adds in 2026 will be approximately 25, not the "
            "80 the plan assumed. Senior engineering compensation is below market. The people team "
            "has flagged 15–25 specific attrition risks in Q1 2026. The Helio retention equity "
            "has a cliff in 2026 — the engineers who accelerate our AI roadmap have an exit window."
        ),
        "evidence": [
            "Resource management module and GxP environment both deferred from 2025; workflow automation slipped 2 quarters",
            "Employee survey: 27% of senior engineers cited compensation as a concern; people team warns of specific Q1 2026 attrition risk",
            "Helio: retention equity vests over 4 years — compensation cliff in 2026 creates attrition risk for the agent-builder roadmap",
            "2026 draft roadmap has 6 major commitments; CPO's own risk section states engineering capacity cannot support all 6 on current trajectory",
        ],
        "color_hex": "D62728",
        "color_rgb": RED,
    },
]

for iss in issues:
    # Label row
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.cell(0, 0)
    shade_cell(hdr, iss["color_hex"])
    hp = hdr.paragraphs[0]
    hp.paragraph_format.space_before = Pt(5)
    hp.paragraph_format.space_after  = Pt(5)
    r_num = hp.add_run(f"ISSUE {iss['number']}  ")
    set_font(r_num, size=9, bold=True, color=WHITE)
    r_lbl = hp.add_run(iss["label"])
    set_font(r_lbl, size=10, bold=True, color=WHITE)

    # Body row
    tbl2 = doc.add_table(rows=1, cols=2)
    tbl2.style = "Table Grid"
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl2.columns[0].width = Inches(3.5)
    tbl2.columns[1].width = Inches(3.1)

    body_cell = tbl2.cell(0, 0)
    shade_cell(body_cell, "F4F8FC")
    bp = body_cell.paragraphs[0]
    bp.paragraph_format.space_before = Pt(6)
    bp.paragraph_format.space_after  = Pt(6)
    br = bp.add_run(iss["body"])
    set_font(br, size=10, color=NAVY)

    evid_cell = tbl2.cell(0, 1)
    shade_cell(evid_cell, "FFFFFF")
    ep = evid_cell.paragraphs[0]
    ep.paragraph_format.space_before = Pt(4)
    ep.paragraph_format.space_after  = Pt(2)
    er = ep.add_run("Key evidence")
    set_font(er, size=8, bold=True, color=iss["color_rgb"])

    for bullet in iss["evidence"]:
        bp2 = evid_cell.add_paragraph(style="List Bullet")
        bp2.paragraph_format.space_before = Pt(1)
        bp2.paragraph_format.space_after  = Pt(1)
        bp2.paragraph_format.left_indent  = Inches(0.15)
        br2 = bp2.add_run(bullet)
        set_font(br2, size=8.5, color=NAVY)

    doc.add_paragraph()  # spacer between issues

# ══════════════════════════════════════════════════════════════════════════════
# THE ASK
# ══════════════════════════════════════════════════════════════════════════════
ask_tbl = doc.add_table(rows=1, cols=1)
ask_tbl.style = "Table Grid"
ask_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
ask_cell = ask_tbl.cell(0, 0)
shade_cell(ask_cell, "1A1A2E")

ap = ask_cell.paragraphs[0]
ap.paragraph_format.space_before = Pt(8)
ap.paragraph_format.space_after  = Pt(4)
ar = ap.add_run("MY ONE ASK OF THE BOARD TODAY")
set_font(ar, size=10, bold=True, color=RGBColor(0x88, 0xBB, 0xDD))

ap2 = ask_cell.add_paragraph()
ap2.paragraph_format.space_before = Pt(0)
ap2.paragraph_format.space_after  = Pt(8)
ar2 = ap2.add_run(
    "I am not asking for approval of a new strategic plan today — that comes at Q1 2026. "
    "I am asking the board to align on three decisions before we leave this room, "
    "because each one is blocking execution:"
)
set_font(ar2, size=10, color=WHITE)

decisions = [
    (
        "Decision 1 — AI positioning:",
        "Are we an agentic work platform (AI-first, PM as one surface) or a PM tool with AI features? "
        "This changes R&D priorities, sales motion, and pricing model. I have a strong view. "
        "I need the board's conviction before Investor Day on March 11.",
        [
            "28% of sales reps cannot articulate Meridian's AI differentiation vs. Asana — cited in 28% of sales open-ends (Employee Survey, Oct 2025)",
            "Copilot 44% attach rate on enterprise Q4 renewals shows AI is already a buying criterion, not a nice-to-have",
            "R&D at 25.4% of revenue (2025) — highest since IPO — without a declared platform identity, spend is unfocused",
            "Investor Day is March 11: public positioning must match internal conviction or we create a credibility gap",
        ],
    ),
    (
        "Decision 2 — Consumption pricing:",
        "The move from per-seat to per-seat-plus-consumption for Copilot is a strategic decision, "
        "not a product decision. The CFO and CRO need board direction to finalize the model. "
        "Every quarter we delay costs us enterprise renewals.",
        [
            "Current Copilot price: $40/seat/month add-on — at 710 seats this yields ~$340K ARR run-rate; consumption model would tie revenue to actual agent usage and scale faster with enterprise adoption",
            "Mid-market renewals already demanding Copilot bundled at no cost (Q3 2025 earnings); without a clear model we are giving it away or losing deals",
            "CPO memo explicitly states: 'The Copilot pricing model is a strategic decision, not a product decision — CPO recommends CFO and CRO jointly own this'",
            "Consumption revenue requires different forecasting discipline and sales compensation design — the longer we wait, the more 2026 quota plans are built on the wrong model",
        ],
    ),
    (
        "Decision 3 — Roadmap prioritization:",
        "The 2026 AI roadmap has six major commitments. Engineering can execute three well or six poorly. "
        "I will present my recommended three. I need the board to hold the line with me "
        "when stakeholders push for the other three.",
        [
            "2025 delivery record: 6 of 12 commitments slipped ≥1 quarter; 2 deferred outright — on a plan with fewer competing priorities than 2026",
            "Engineering net adds in 2026: ~25 actual vs. 80 assumed in the plan (15% annual attrition on 750-person org)",
            "The six 2026 commitments span: Copilot governance suite (Q1), agent builder (Q2), resource mgmt module (Q2), workflow marketplace (Q3), pricing model refresh (Q3), GxP environment (Q4) — each is a multi-quarter engineering effort",
            "Helio retention cliff in 2026: the agent-builder depends on 28 Helio engineers whose cash compensation cliff arrives this year; if they leave, the Q2 commitment is at risk",
        ],
    ),
]

for label, text, data_points in decisions:
    dp = ask_cell.add_paragraph()
    dp.paragraph_format.space_before = Pt(6)
    dp.paragraph_format.space_after  = Pt(2)
    dp.paragraph_format.left_indent  = Inches(0.2)
    dr = dp.add_run(f"{label}  ")
    set_font(dr, size=10, bold=True, color=RGBColor(0x88, 0xBB, 0xDD))
    dr2 = dp.add_run(text)
    set_font(dr2, size=10, color=WHITE)

    for pt in data_points:
        bp = ask_cell.add_paragraph()
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after  = Pt(1)
        bp.paragraph_format.left_indent  = Inches(0.45)
        br = bp.add_run(f"▸  {pt}")
        set_font(br, size=8.5, color=RGBColor(0xCC, 0xDD, 0xEE))

    # spacer after each decision
    sp = ask_cell.add_paragraph()
    sp.paragraph_format.space_before = Pt(2)
    sp.paragraph_format.space_after  = Pt(2)

# ══════════════════════════════════════════════════════════════════════════════
# CLOSING LINE
# ══════════════════════════════════════════════════════════════════════════════
doc.add_paragraph()
p_close = add_para(space_before=4, space_after=0)
p_close.alignment = WD_ALIGN_PARAGRAPH.CENTER
rc = p_close.add_run(
    "The foundation Lenore built is real. The window to lead the agentic transition is open. "
    "Let's use this session well."
)
set_font(rc, size=11, italic=True, color=NAVY)

# ── Footer note ───────────────────────────────────────────────────────────────
doc.add_paragraph()
p_foot = add_para(space_before=8, space_after=0)
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rf = p_foot.add_run(
    "CONFIDENTIAL — For Board of Directors use only  |  Meridian Technologies, Inc.  |  Annual Strategic Review"
)
set_font(rf, size=7.5, color=GRAY)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/home/user/Claude-session/meridian/board_opening_remarks.docx"
doc.save(out)
print(f"Saved: {out}")
