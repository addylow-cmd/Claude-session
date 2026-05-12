import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(18, 11))
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis("off")
fig.patch.set_facecolor("#F7F9FC")

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY       = "#1A1A2E"
BLUE       = "#1F77B4"
ORANGE     = "#D66200"
GREEN      = "#2CA02C"
RED        = "#D62728"
PURPLE     = "#7B2D8B"
LGRAY      = "#E8EEF4"
MGRAY      = "#C5CDD8"
WHITE      = "#FFFFFF"
OPTB_COL   = "#D6EAF8"   # light blue  — closer to Option B
OPTA_COL   = "#FEF9E7"   # light yellow — closer to Option A
MERIDIAN   = "#1A3A5C"

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(9, 10.55, "Competitive AI Landscape — Meridian Technologies",
        ha="center", va="center", fontsize=17, fontweight="bold", color=NAVY)
ax.text(9, 10.15, "Where each competitor sits relative to Meridian's Option A (PM+AI) vs Option B (Agentic Platform)  |  Source: cached competitor snapshots, ~Feb 2026",
        ha="center", va="center", fontsize=9, color="#555555")

# ── Column definitions ─────────────────────────────────────────────────────────
COL_X      = [0.25, 3.1, 5.85, 9.55, 13.25, 15.8]
COL_W      = [2.7,  2.6,  3.5,   3.5,   2.4,   2.0]
HEADERS    = ["Competitor", "AI Positioning", "Pricing Posture",
              "Latest Flagship Announcement", "Closer to\nMeridian Option", "Meridian\nDifferentiator"]

ROW_TOP    = 9.55
ROW_H      = 1.52
ROW_Y      = [ROW_TOP - i * ROW_H for i in range(6)]  # header + 5 rows

# ── Data ──────────────────────────────────────────────────────────────────────
rows = [
    {
        "name": "Asana",
        "color": "#E74C3C",
        "ai_pos": '"Work management\nplatform with AI built in"\n(AI Studio / Smart Workflows)\nLang: "Agent operating system"',
        "pricing": "AI bundled into\nAdvanced & Enterprise\ntiers at no extra cost.\nNo consumption pricing.",
        "flagship": "Nov 2025: AI Studio +\nSmart Workflows bundled\ninto paid tiers — direct\nprice shot at add-on models",
        "option": "OPTION B",
        "option_col": OPTB_COL,
        "option_txt": RED,
        "diff": "Meridian has deep\nenterprise governance\n(FedRAMP, HIPAA);\nAsana does not.",
    },
    {
        "name": "Monday.com",
        "color": "#E67E22",
        "ai_pos": '"Work OS,\nsupercharged with AI"\n(monday AI Agents)\nLang: "AI layer across\nevery part of the OS"',
        "pricing": "AI Agents bundled\ninto Pro tier+.\nNo consumption pricing.\n'Consumption = friction'",
        "flagship": "Jan 2026: monday AI\nAgents GA — customer-\nbuildable agents in\nnatural language, Pro+",
        "option": "OPTION A/B\n(hybrid — breadth\nover depth)",
        "option_col": "#FDF2E9",
        "option_txt": ORANGE,
        "diff": "Meridian wins on\nregulated verticals;\nMonday has no\nFedRAMP/HIPAA.",
    },
    {
        "name": "Smartsheet",
        "color": "#27AE60",
        "ai_pos": '"Enterprise work platform\nyou can trust with AI"\n(Smartsheet AI)\nLang: "AI-augmented,"\nnot "agentic"',
        "pricing": "Smartsheet AI bundled\nin Business/Enterprise.\nAI Compliance Pack:\npremium add-on ~$15/seat.",
        "flagship": "Dec 2025: AI Compliance\nPack — agent audit logs,\nmodel selection, data\nresidency. Enterprise only.",
        "option": "OPTION A\n(closest peer)",
        "option_col": OPTA_COL,
        "option_txt": GREEN,
        "diff": "Meridian is more\nagentic; Smartsheet\nexplicitly rejected\n'agentic' label.",
    },
    {
        "name": "Atlassian",
        "color": BLUE,
        "ai_pos": '"Agentic enterprise\nplatform for software\n& IT teams" (Rovo)\nLang: "Agent company\nthat ships software"',
        "pricing": "Rovo: per-seat +\nper-action consumption.\n~$20/seat base.\nOnly competitor with\nconsumption pricing.",
        "flagship": "Jan 2026: Rovo Studio\nGA — developer agent\nbuilder on Jira/Confluence\ninfra. Separate paid SKU.",
        "option": "OPTION B\n(closest peer)",
        "option_col": OPTB_COL,
        "option_txt": BLUE,
        "diff": "Meridian serves\npharma/banking;\nAtlassian is dev/IT\nshaped. Meridian\nhas broader PM depth.",
    },
    {
        "name": "MERIDIAN\n(for reference)",
        "color": MERIDIAN,
        "ai_pos": '[Declaring at\nInvestor Day]\nCopilot GA Sep 2025;\n710 paying seats;\n$3.5M ARR',
        "pricing": "Today: $40/seat\nadd-on (Copilot).\nOption B commits to\nhybrid consumption\nmodel in H2 2026.",
        "flagship": "Nov 2025: Helio Labs\nacquisition ($78M);\nAgent framework +\n28 AI engineers.\nFedRAMP + HIPAA in hand.",
        "option": "DECLARING\nOPTION B\n(recommended)",
        "option_col": "#EAF4FB",
        "option_txt": MERIDIAN,
        "diff": "Only player with\nFedRAMP + HIPAA +\nagent framework +\nregulated-industry\nvertical depth.",
    },
]

# ── Draw header row ───────────────────────────────────────────────────────────
for i, (hdr, cx, cw) in enumerate(zip(HEADERS, COL_X, COL_W)):
    rect = FancyBboxPatch((cx - 0.05, ROW_Y[0] - 0.32), cw, 0.62,
                          boxstyle="round,pad=0.04", linewidth=0,
                          facecolor=NAVY, zorder=2)
    ax.add_patch(rect)
    ax.text(cx + cw/2 - 0.05, ROW_Y[0], hdr,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=WHITE, zorder=3)

# ── Draw data rows ────────────────────────────────────────────────────────────
cells = ["ai_pos", "pricing", "flagship", "option", "diff"]

for r_idx, row in enumerate(rows):
    y_top = ROW_Y[r_idx + 1] + ROW_H * 0.48
    y_bot = ROW_Y[r_idx + 1] - ROW_H * 0.52
    row_bg = WHITE if r_idx % 2 == 0 else LGRAY

    # full-row background
    rect = FancyBboxPatch((COL_X[0] - 0.05, y_bot),
                          COL_X[-1] + COL_W[-1] - COL_X[0],
                          y_top - y_bot,
                          boxstyle="round,pad=0.03", linewidth=0.5,
                          edgecolor=MGRAY, facecolor=row_bg, zorder=1)
    ax.add_patch(rect)

    # competitor name cell
    name_rect = FancyBboxPatch((COL_X[0] - 0.05, y_bot),
                               COL_W[0], y_top - y_bot,
                               boxstyle="round,pad=0.03", linewidth=0,
                               facecolor=row["color"], zorder=2)
    ax.add_patch(name_rect)
    ax.text(COL_X[0] + COL_W[0]/2 - 0.05, ROW_Y[r_idx + 1],
            row["name"], ha="center", va="center",
            fontsize=10, fontweight="bold", color=WHITE, zorder=3)

    # option cell (colored background)
    opt_rect = FancyBboxPatch((COL_X[4] - 0.05, y_bot),
                              COL_W[4], y_top - y_bot,
                              boxstyle="round,pad=0.03", linewidth=0.8,
                              edgecolor=row["option_txt"], facecolor=row["option_col"], zorder=2)
    ax.add_patch(opt_rect)
    ax.text(COL_X[4] + COL_W[4]/2 - 0.05, ROW_Y[r_idx + 1],
            row["option"], ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=row["option_txt"], zorder=3)

    # text cells
    for c_idx, key in enumerate(cells):
        if key == "option":
            continue   # already drawn
        cx = COL_X[c_idx + 1]
        cw = COL_W[c_idx + 1]
        ax.text(cx + 0.08, ROW_Y[r_idx + 1], row[key],
                ha="left", va="center",
                fontsize=7.8, color=NAVY, zorder=3,
                linespacing=1.4)

# ── Divider lines between rows ────────────────────────────────────────────────
for r_idx in range(len(rows)):
    y_line = ROW_Y[r_idx + 1] - ROW_H * 0.52
    ax.plot([COL_X[0] - 0.05, COL_X[-1] + COL_W[-1] - 0.1],
            [y_line, y_line], color=MGRAY, linewidth=0.5, zorder=4)

# ── Legend ────────────────────────────────────────────────────────────────────
leg_y = 0.38
ax.add_patch(FancyBboxPatch((0.2, leg_y - 0.18), 3.4, 0.42,
             boxstyle="round,pad=0.05", facecolor=OPTB_COL,
             edgecolor=BLUE, linewidth=1))
ax.text(1.9, leg_y, "Closer to Option B — Agentic Platform",
        ha="center", va="center", fontsize=8.5, color=BLUE, fontweight="bold")

ax.add_patch(FancyBboxPatch((3.9, leg_y - 0.18), 3.0, 0.42,
             boxstyle="round,pad=0.05", facecolor=OPTA_COL,
             edgecolor=GREEN, linewidth=1))
ax.text(5.4, leg_y, "Closer to Option A — PM+AI",
        ha="center", va="center", fontsize=8.5, color=GREEN, fontweight="bold")

ax.text(9, leg_y, "Option A = PM platform with AI features  |  Option B = Agentic work platform (Meridian's recommended path)",
        ha="center", va="center", fontsize=8, color="#666666")

ax.text(9, 0.1, "Source: Meridian internal data + competitor cached snapshots ~Feb 2026  |  Prepared for Investor Day positioning, March 11 2026",
        ha="center", va="center", fontsize=7.5, color="#999999")

out = "/home/user/Claude-session/competitive_landscape.png"
plt.tight_layout(pad=0)
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
