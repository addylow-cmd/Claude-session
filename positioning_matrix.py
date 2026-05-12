import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 10))
fig.patch.set_facecolor("#F7F9FC")
ax.set_facecolor("#F7F9FC")

# ── Axis ranges ───────────────────────────────────────────────────────────────
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

# ── Quadrant shading ──────────────────────────────────────────────────────────
ax.fill_between([-1, 0], [-1, -1], [0, 0],  color="#FEF9E7", alpha=0.7, zorder=0)  # BL: PM + bundled
ax.fill_between([0, 1],  [-1, -1], [0, 0],  color="#EAF4FB", alpha=0.7, zorder=0)  # BR: agentic + bundled
ax.fill_between([-1, 0], [0, 0],   [1, 1],  color="#FDF2E9", alpha=0.5, zorder=0)  # TL: PM + premium
ax.fill_between([0, 1],  [0, 0],   [1, 1],  color="#EBF5EB", alpha=0.5, zorder=0)  # TR: agentic + premium

# Quadrant labels
quad_kw = dict(fontsize=9, color="#AAAAAA", fontstyle="italic", zorder=1)
ax.text(-0.95,  0.92, "Traditional PM\n(premium / add-on)",    va="top",    ha="left",  **quad_kw)
ax.text( 0.95,  0.92, "Agentic Platform\n(premium / add-on)",  va="top",    ha="right", **quad_kw)
ax.text(-0.95, -0.92, "Traditional PM\n(bundled / low-cost)",  va="bottom", ha="left",  **quad_kw)
ax.text( 0.95, -0.92, "Agentic Platform\n(bundled / low-cost)",va="bottom", ha="right", **quad_kw)

# ── Axes ──────────────────────────────────────────────────────────────────────
ax.axhline(0, color="#CCCCCC", linewidth=1.2, zorder=1)
ax.axvline(0, color="#CCCCCC", linewidth=1.2, zorder=1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Axis arrows
arrow_kw = dict(transform=ax.transData, color="#888888",
                arrowstyle="-|>", mutation_scale=14, linewidth=1.2, zorder=2)
ax.annotate("", xy=(1.02, 0),  xytext=(-1.02, 0),  arrowprops=dict(**arrow_kw))
ax.annotate("", xy=(0, 1.02),  xytext=(0, -1.02),  arrowprops=dict(**arrow_kw))

# Axis labels
ax.text( 1.03,  0,     "Agentic-platform\ncentric →",  va="center", ha="left",  fontsize=10, fontweight="bold", color="#555555")
ax.text(-1.03,  0,     "← PM-\ncentric",               va="center", ha="right", fontsize=10, fontweight="bold", color="#555555")
ax.text( 0,     1.04,  "Premium /\nadd-on pricing ↑",  va="bottom", ha="center",fontsize=10, fontweight="bold", color="#555555")
ax.text( 0,    -1.04,  "↓ Bundled /\nlow-cost pricing", va="top",   ha="center",fontsize=10, fontweight="bold", color="#555555")

# ── Competitor data ───────────────────────────────────────────────────────────
# (x = PM→Agentic  -1..+1,  y = bundled→premium  -1..+1)
players = [
    dict(name="Asana",       x= 0.55, y=-0.55, color="#E74C3C", size=220,
         note="Bundled into\nAdvanced+ tiers;\n'agent OS' language"),
    dict(name="Monday.com",  x= 0.20, y=-0.75, color="#E67E22", size=220,
         note="Agents bundled\nPro+; cheapest\nagentic option"),
    dict(name="Smartsheet",  x=-0.60, y= 0.40, color="#27AE60", size=220,
         note="AI Compliance Pack\nas premium add-on;\nexplicitly not agentic"),
    dict(name="Atlassian",   x= 0.72, y= 0.65, color="#1F77B4", size=220,
         note="Rovo: per-seat +\nconsumption; most\ncommitted agentic bet"),
    dict(name="Meridian\n(Option B\nrecommended)", x=0.50, y=0.55,
         color="#1A3A5C", size=320,
         note="FedRAMP+HIPAA+\nagent framework;\nhybrid consumption\nH2 2026"),
]

# nudge label positions to avoid overlap
label_offsets = {
    "Asana":       (-0.10, -0.14),
    "Monday.com":  ( 0.08, -0.13),
    "Smartsheet":  (-0.08, -0.14),
    "Atlassian":   ( 0.08,  0.10),
    "Meridian\n(Option B\nrecommended)": (-0.22,  0.10),
}

for p in players:
    is_meridian = "Meridian" in p["name"]

    # shadow
    ax.scatter(p["x"] + 0.012, p["y"] - 0.012, s=p["size"] * 1.15,
               color="#AAAAAA", alpha=0.25, zorder=3)
    # dot
    ax.scatter(p["x"], p["y"], s=p["size"],
               color=p["color"], edgecolors=("gold" if is_meridian else "white"),
               linewidths=(2.5 if is_meridian else 1.5),
               zorder=4)

    # name label
    short = p["name"].split("\n")[0] + ("\n(Option B rec.)" if is_meridian else "")
    dx, dy = label_offsets[p["name"]]
    ax.text(p["x"] + dx, p["y"] + dy, short,
            ha="center", va="top",
            fontsize=9.5, fontweight="bold", color=p["color"],
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=p["color"], linewidth=0.8, alpha=0.88),
            zorder=5)

    # annotation note
    note_dx = 0.18 if p["x"] < 0 else -0.18
    note_align = "left" if p["x"] < 0 else "right"
    note_x = p["x"] + (0.22 if p["x"] > 0 else -0.22)
    note_y = p["y"] + (0.10 if p["y"] > 0 else -0.10)
    ax.text(note_x, note_y, p["note"],
            ha=note_align, va="center",
            fontsize=7.5, color="#666666", linespacing=1.35,
            zorder=5)

# ── "White space" callout ─────────────────────────────────────────────────────
# Top-right quadrant: agentic + premium — Atlassian + Meridian zone
ax.annotate("White space:\nEnterprise-grade,\nmodel-neutral\nagentic platform\n(Meridian's claim)",
            xy=(0.50, 0.55), xytext=(0.05, 0.78),
            fontsize=8, color="#1A3A5C", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#1A3A5C", lw=1.2),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EAF4FB",
                      edgecolor="#1A3A5C", linewidth=1),
            zorder=6)

# ── Title & footer ────────────────────────────────────────────────────────────
ax.set_title("AI Positioning Matrix — Work Management Category\n"
             "X: PM-centric → Agentic platform   |   Y: Bundled/low-cost → Premium/add-on",
             fontsize=13, fontweight="bold", color="#1A1A2E", pad=18)

ax.text(0, -1.13,
        "Source: Meridian internal data + competitor cached snapshots ~Feb 2026  |  Investor Day prep, March 11 2026",
        ha="center", va="center", fontsize=7.5, color="#AAAAAA", transform=ax.transData)

out = "/home/user/Claude-session/positioning_matrix.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
