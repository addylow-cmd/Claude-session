import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────────
financials = pd.DataFrame({
    "quarter": [
        "2022Q1","2022Q2","2022Q3","2022Q4",
        "2023Q1","2023Q2","2023Q3","2023Q4",
        "2024Q1","2024Q2","2024Q3","2024Q4",
        "2025Q1","2025Q2","2025Q3","2025Q4",
    ],
    "revenue":          [60.4,64.1,67.3,68.6,73.0,76.2,79.4,82.0,86.4,89.1,91.0,93.7,96.4,98.8,101.5,103.2],
    "arr":              [251.6,266.8,279.9,275.4,302.5,316.1,329.8,328.0,357.5,367.6,374.1,374.8,398.9,408.5,419.6,412.8],
    "op_margin":        [4.0,4.6,5.4,6.2,6.9,7.4,7.9,8.5,9.4,9.8,10.1,10.5,11.1,11.6,12.0,12.4],
    "fcf_margin":       [7.5,9.1,11.2,13.8,12.5,13.6,14.2,15.4,14.8,15.7,16.2,16.8,15.9,16.5,17.2,17.8],
})

kpis = pd.DataFrame({
    "quarter": ["2024Q1","2024Q2","2024Q3","2024Q4",
                "2025Q1","2025Q2","2025Q3","2025Q4"],
    "nrr":     [114,113,112,111,110,110,109,109],
    "magic":   [1.20,1.16,1.10,1.05,1.02,0.98,0.95,0.92],
})

# ARR YoY growth — quarterly (compare to same Q prior year)
arr = financials.set_index("quarter")["arr"]
yoy_arr = []
labels_arr = []
for i, q in enumerate(financials["quarter"]):
    year = int(q[:4]); qnum = q[4:]
    prior = f"{year-1}{qnum}"
    if prior in arr.index:
        growth = (arr[q] - arr[prior]) / arr[prior] * 100
        yoy_arr.append(growth)
        labels_arr.append(q)

# ── Layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor="#FAFAFA")
fig.suptitle(
    "Meridian Technologies — The Core Strategic Tension",
    fontsize=18, fontweight="bold", y=0.98, color="#1A1A2E"
)
fig.text(0.5, 0.945,
    "Profitability improving steadily — but growth is decelerating and GTM efficiency is eroding",
    ha="center", fontsize=11, color="#555555"
)

gs = fig.add_gridspec(2, 2, hspace=0.45, wspace=0.35,
                      left=0.07, right=0.96, top=0.90, bottom=0.08)

BLUE   = "#1F77B4"
GREEN  = "#2CA02C"
ORANGE = "#FF7F0E"
RED    = "#D62728"
GRAY   = "#AAAAAA"
ACCENT = "#E8F4FD"

quarters_fin = financials["quarter"].tolist()
x_fin = np.arange(len(quarters_fin))
tick_labels_fin = [q[2:] for q in quarters_fin]   # "22Q1" etc.

quarters_kpi = kpis["quarter"].tolist()
x_kpi = np.arange(len(quarters_kpi))
tick_labels_kpi = [q[2:] for q in quarters_kpi]

x_arr = np.arange(len(labels_arr))
tick_labels_arr = [q[2:] for q in labels_arr]

# ── Chart 1: ARR YoY growth ───────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.bar(x_arr, yoy_arr, color=[BLUE if v > 12 else ORANGE for v in yoy_arr],
               width=0.6, zorder=3)
ax1.axhline(12, color=GRAY, linestyle="--", linewidth=1, zorder=2)
ax1.text(len(x_arr)-0.5, 12.5, "12%", fontsize=8, color=GRAY)
ax1.set_title("ARR Growth (YoY)", fontsize=12, fontweight="bold", color="#1A1A2E", pad=8)
ax1.set_xticks(x_arr); ax1.set_xticklabels(tick_labels_arr, fontsize=7, rotation=45)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax1.set_facecolor(ACCENT); ax1.grid(axis="y", alpha=0.4, zorder=0)
ax1.spines[["top","right"]].set_visible(False)
for bar, val in zip(bars, yoy_arr):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{val:.0f}%", ha="center", va="bottom", fontsize=7, fontweight="bold")
# annotation
ax1.annotate("28% → 10%\nin 3 years", xy=(x_arr[-1], yoy_arr[-1]),
             xytext=(x_arr[-3], yoy_arr[-1]+6),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
             fontsize=8, color=RED, fontweight="bold")

# ── Chart 2: Operating margin + FCF margin ───────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.fill_between(x_fin, financials["fcf_margin"], alpha=0.15, color=GREEN)
ax2.plot(x_fin, financials["op_margin"],  color=BLUE,  linewidth=2.5, marker="o", ms=4, label="Operating margin")
ax2.plot(x_fin, financials["fcf_margin"], color=GREEN, linewidth=2.5, marker="s", ms=4, label="FCF margin")
ax2.set_title("Margin Expansion", fontsize=12, fontweight="bold", color="#1A1A2E", pad=8)
ax2.set_xticks(x_fin); ax2.set_xticklabels(tick_labels_fin, fontsize=7, rotation=45)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax2.legend(fontsize=8, framealpha=0.6)
ax2.set_facecolor(ACCENT); ax2.grid(axis="y", alpha=0.4)
ax2.spines[["top","right"]].set_visible(False)
# label endpoints
ax2.text(x_fin[-1]+0.1, financials["op_margin"].iloc[-1], "12.4%", fontsize=8, color=BLUE, va="center")
ax2.text(x_fin[-1]+0.1, financials["fcf_margin"].iloc[-1], "17.8%", fontsize=8, color=GREEN, va="center")

# ── Chart 3: NRR by segment (from segments doc — spot values) ─────────────────
ax3 = fig.add_subplot(gs[1, 0])
seg_labels = ["Enterprise\n(40% ARR)", "Mid-Market\n(47% ARR)", "SMB\n(13% ARR)"]
nrr_2022   = [127, 115, 115]   # approximate from segments doc
nrr_2025q4 = [125, 102,  84]
x_seg = np.arange(len(seg_labels))
w = 0.35
bars_22 = ax3.bar(x_seg - w/2, nrr_2022,   width=w, label="2022", color=BLUE,   alpha=0.85, zorder=3)
bars_25 = ax3.bar(x_seg + w/2, nrr_2025q4, width=w, label="Q4 2025", color=ORANGE, alpha=0.85, zorder=3)
ax3.axhline(100, color=RED, linestyle="--", linewidth=1.2, zorder=2)
ax3.text(-0.5, 100.8, "100% = no net churn", fontsize=7.5, color=RED)
ax3.set_title("Net Revenue Retention by Segment", fontsize=12, fontweight="bold", color="#1A1A2E", pad=8)
ax3.set_xticks(x_seg); ax3.set_xticklabels(seg_labels, fontsize=9)
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax3.legend(fontsize=9, framealpha=0.6)
ax3.set_ylim(75, 140)
ax3.set_facecolor(ACCENT); ax3.grid(axis="y", alpha=0.4, zorder=0)
ax3.spines[["top","right"]].set_visible(False)
for b, v in zip(bars_22, nrr_2022):
    ax3.text(b.get_x()+b.get_width()/2, v+0.5, f"{v}%", ha="center", va="bottom", fontsize=8)
for b, v in zip(bars_25, nrr_2025q4):
    color = RED if v < 100 else "#1A1A2E"
    ax3.text(b.get_x()+b.get_width()/2, v+0.5, f"{v}%", ha="center", va="bottom", fontsize=8, color=color, fontweight="bold")

# ── Chart 4: Magic number + CAC payback ──────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4b = ax4.twinx()
ax4.plot(x_kpi, kpis["magic"], color=BLUE,   linewidth=2.5, marker="o", ms=5, label="Magic number (L)")
ax4b.plot(x_kpi, kpis["magic"].apply(lambda _: None),  alpha=0)   # dummy for legend spacing

cac = [18.2,18.9,19.5,20.4,21.1,21.6,22.0,22.4]
ax4b.plot(x_kpi, cac, color=RED, linewidth=2.5, marker="s", ms=5, linestyle="--", label="CAC payback months (R)")

ax4.axhline(1.0, color=ORANGE, linestyle="--", linewidth=1.2)
ax4.text(0, 1.01, "Magic number = 1.0 (efficiency threshold)", fontsize=7.5, color=ORANGE)
ax4.set_title("GTM Efficiency Deteriorating", fontsize=12, fontweight="bold", color="#1A1A2E", pad=8)
ax4.set_xticks(x_kpi); ax4.set_xticklabels(tick_labels_kpi, fontsize=8, rotation=45)
ax4.set_ylabel("Magic number", fontsize=9, color=BLUE)
ax4b.set_ylabel("CAC payback (months)", fontsize=9, color=RED)
ax4.tick_params(axis="y", labelcolor=BLUE)
ax4b.tick_params(axis="y", labelcolor=RED)
ax4.set_ylim(0.7, 1.4)
ax4b.set_ylim(14, 26)
ax4.set_facecolor(ACCENT); ax4.grid(axis="y", alpha=0.3)
ax4.spines[["top"]].set_visible(False)

lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax4b.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=8, framealpha=0.6, loc="upper right")

# label the cross below 1.0
ax4.annotate("Below 1.0\n(Aug 2025)", xy=(5, 0.98), xytext=(3.5, 0.80),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
             fontsize=8, color=RED, fontweight="bold")

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.01,
    "Source: Meridian internal financials & KPI data, 2022Q1–2025Q4  |  Prepared for Board Strategic Review",
    ha="center", fontsize=8, color=GRAY
)

out = "/home/user/Claude-session/meridian/board_chart.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved to {out}")
