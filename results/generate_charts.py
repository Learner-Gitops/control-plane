"""
IEEE-quality chart generation for:
"Designing a GitOps-Based Deployment Control Plane
 for Scalable Kubernetes Platforms"

Generates 6 publication-ready figures using matplotlib.
"""

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Load results ──────────────────────────────────────────
with open("results_data.json") as f:
    data = json.load(f)

os.makedirs("charts", exist_ok=True)

# ── IEEE style defaults ───────────────────────────────────
plt.rcParams.update({
    "font.family":      "serif",
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "legend.fontsize":  9,
    "figure.dpi":       150,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "axes.spines.top":  False,
    "axes.spines.right":False,
})

BLUE   = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN  = "#2ca02c"
RED    = "#d62728"


# ══════════════════════════════════════════════════════════
# Fig 1 — Deployment Consistency: Grouped Bar Chart
# ══════════════════════════════════════════════════════════
def fig1_consistency():
    d    = data["deployment_consistency"]
    envs = d["environments"]
    x    = np.arange(len(envs))
    w    = 0.35

    fig, ax = plt.subplots(figsize=(6, 4))
    b1 = ax.bar(x - w/2, d["manual_pct"], w, label="Manual Deployment",
                color=ORANGE, edgecolor="black", linewidth=0.6)
    b2 = ax.bar(x + w/2, d["gitops_pct"], w, label="GitOps (Argo CD)",
                color=BLUE,   edgecolor="black", linewidth=0.6)

    for bar in b1:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=8)
    for bar in b2:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(envs)
    ax.set_ylabel("Configuration Consistency (%)")
    ax.set_title("Fig. 1 — Deployment Consistency Across Environments\n"
                 f"(GitOps avg: {d['avg_gitops']}% vs Manual avg: {d['avg_manual']}%)")
    ax.set_ylim(0, 110)
    ax.legend(loc="lower right")
    ax.axhline(y=d["avg_gitops"],  color=BLUE,   linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axhline(y=d["avg_manual"],  color=ORANGE, linestyle="--", linewidth=0.8, alpha=0.6)

    plt.tight_layout()
    plt.savefig("charts/fig1_deployment_consistency.png")
    plt.close()
    print("Saved: fig1_deployment_consistency.png")


# ══════════════════════════════════════════════════════════
# Fig 2 — Drift Detection & Reconciliation: Stacked Bar
# ══════════════════════════════════════════════════════════
def fig2_drift():
    d   = data["drift_reconciliation"]
    y   = np.arange(len(d["scenarios"]))
    det = d["detection_sec"]
    rec = d["reconcile_sec"]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(y, det, color=ORANGE, edgecolor="black", linewidth=0.6, label="Detection Time (s)")
    ax.barh(y, rec, left=det,     color=BLUE,   edgecolor="black", linewidth=0.6, label="Reconciliation Time (s)")

    for i, (d_val, r_val) in enumerate(zip(det, rec)):
        total = d_val + r_val
        ax.text(total + 0.5, i, f"{total:.1f}s", va="center", fontsize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(d["scenarios"])
    ax.set_xlabel("Time (seconds)")
    ax.set_title(f"Fig. 2 — Drift Detection & Auto-Reconciliation Time\n"
                 f"(Avg MTTR: {d['avg_total_mttr']}s | Auto-heal rate: {d['auto_heal_rate']}%)")
    ax.legend(loc="lower right")
    ax.set_xlim(0, 55)

    plt.tight_layout()
    plt.savefig("charts/fig2_drift_reconciliation.png")
    plt.close()
    print("Saved: fig2_drift_reconciliation.png")


# ══════════════════════════════════════════════════════════
# Fig 3 — Rollback Speed: Dual-axis Bar Chart
# ══════════════════════════════════════════════════════════
def fig3_rollback():
    d  = data["rollback_speed"]
    x  = np.arange(len(d["scenarios"]))
    w  = 0.35

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax2 = ax1.twinx()

    b1 = ax1.bar(x - w/2, d["manual_min"], w, color=ORANGE,
                 edgecolor="black", linewidth=0.6, label="Manual (minutes)")
    b2 = ax1.bar(x + w/2, [s/60 for s in d["gitops_sec"]], w, color=BLUE,
                 edgecolor="black", linewidth=0.6, label="GitOps (minutes)")
    ax2.plot(x, d["speedup_x"], "D-", color=RED, linewidth=1.5,
             markersize=6, label="Speedup (×)", zorder=5)

    ax1.set_xticks(x)
    ax1.set_xticklabels(d["scenarios"], rotation=15, ha="right")
    ax1.set_ylabel("Rollback Time (minutes)")
    ax2.set_ylabel("Speedup Factor (×)", color=RED)
    ax2.tick_params(axis="y", labelcolor=RED)
    ax1.set_title(f"Fig. 3 — Rollback Speed: Manual vs GitOps\n"
                  f"(Avg speedup: {d['avg_speedup']}× | GitOps avg: {d['avg_gitops_sec']}s)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig("charts/fig3_rollback_speed.png")
    plt.close()
    print("Saved: fig3_rollback_speed.png")


# ══════════════════════════════════════════════════════════
# Fig 4 — Auditability: Deployment Timeline
# ══════════════════════════════════════════════════════════
def fig4_auditability():
    d       = data["auditability"]
    log     = d["audit_log"]
    times   = [i for i in range(len(log))]
    authors = [e["author"] for e in log]
    envs    = [e["environment"] for e in log]
    msgs    = [e["message"][:38]+"…" if len(e["message"])>38 else e["message"] for e in log]

    color_map = {"platform-team": BLUE, "app-team-a": ORANGE, "app-team-b": GREEN}
    colors    = [color_map.get(a, RED) for a in authors]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(times, [1]*len(times), c=colors, s=120, zorder=5, edgecolors="black", linewidth=0.5)
    ax.plot(times, [1]*len(times), color="gray", linewidth=1, zorder=1, linestyle="--")

    for i, (msg, env) in enumerate(zip(msgs, envs)):
        offset = 0.06 if i % 2 == 0 else -0.06
        va     = "bottom" if i % 2 == 0 else "top"
        ax.text(i, 1 + offset, f"[{env}]\n{msg}", ha="center", va=va,
                fontsize=6.5, rotation=0,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))

    patches = [mpatches.Patch(color=c, label=a) for a, c in color_map.items()]
    ax.legend(handles=patches, loc="upper right", fontsize=8)
    ax.set_xlim(-0.5, len(times)-0.5)
    ax.set_ylim(0.7, 1.4)
    ax.set_xticks(times)
    ax.set_xticklabels([f"D{i+1}" for i in times])
    ax.set_yticks([])
    ax.set_xlabel("Deployment Event")
    ax.set_title(f"Fig. 4 — Deployment Audit Trail (Git History)\n"
                 f"({d['total_deployments']} deployments | {d['audit_coverage_pct']}% traceable | RBAC enforced)")
    ax.grid(False)

    plt.tight_layout()
    plt.savefig("charts/fig4_auditability_timeline.png")
    plt.close()
    print("Saved: fig4_auditability_timeline.png")


# ══════════════════════════════════════════════════════════
# Fig 5 — Scalability: Line Chart (teams vs lag & errors)
# ══════════════════════════════════════════════════════════
def fig5_scalability():
    d  = data["scalability"]
    tc = d["team_counts"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

    # Sync lag
    ax1.plot(tc, d["gitops_lag_min"], "o-", color=BLUE,   linewidth=2, markersize=5, label="GitOps")
    ax1.plot(tc, d["manual_lag_min"], "s-", color=ORANGE, linewidth=2, markersize=5, label="Manual")
    ax1.set_xlabel("Number of Teams / Clusters")
    ax1.set_ylabel("Avg Deployment Lag (min)")
    ax1.set_title("(a) Deployment Lag vs Scale")
    ax1.legend()
    ax1.set_xticks(tc)

    # Error rate
    ax2.plot(tc, d["gitops_err_pct"], "o-", color=BLUE,   linewidth=2, markersize=5, label="GitOps")
    ax2.plot(tc, d["manual_err_pct"], "s-", color=ORANGE, linewidth=2, markersize=5, label="Manual")
    ax2.set_xlabel("Number of Teams / Clusters")
    ax2.set_ylabel("Deployment Error Rate (%)")
    ax2.set_title("(b) Error Rate vs Scale")
    ax2.legend()
    ax2.set_xticks(tc)

    fig.suptitle("Fig. 5 — Scalability of GitOps Control Plane vs Manual Approach",
                 fontsize=11, y=1.01)
    plt.tight_layout()
    plt.savefig("charts/fig5_scalability.png", bbox_inches="tight")
    plt.close()
    print("Saved: fig5_scalability.png")


# ══════════════════════════════════════════════════════════
# Fig 6 — Operational Overhead: Horizontal Bar Comparison
# ══════════════════════════════════════════════════════════
def fig6_overhead():
    d  = data["operational_overhead"]
    y  = np.arange(len(d["tasks"]))
    w  = 0.35

    fig, ax = plt.subplots(figsize=(7, 4.5))
    b1 = ax.barh(y + w/2, d["manual_hrs"], w, color=ORANGE,
                 edgecolor="black", linewidth=0.6, label="Manual (hrs/week)")
    b2 = ax.barh(y - w/2, d["gitops_hrs"], w, color=BLUE,
                 edgecolor="black", linewidth=0.6, label="GitOps (hrs/week)")

    for bar in b1:
        ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                f"{bar.get_width():.1f}h", va="center", fontsize=8)
    for bar in b2:
        ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                f"{bar.get_width():.1f}h", va="center", fontsize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(d["tasks"])
    ax.set_xlabel("Hours per Week")
    ax.set_title(f"Fig. 6 — Operational Overhead: Manual vs GitOps\n"
                 f"(Total saved: {d['total_saving']}h/week | "
                 f"Manual: {d['total_manual']}h → GitOps: {d['total_gitops']}h)")
    ax.legend(loc="lower right")
    ax.set_xlim(0, 16)

    plt.tight_layout()
    plt.savefig("charts/fig6_operational_overhead.png")
    plt.close()
    print("Saved: fig6_operational_overhead.png")


# ── Run all ───────────────────────────────────────────────
if __name__ == "__main__":
    print("\nGenerating IEEE-quality charts...\n")
    fig1_consistency()
    fig2_drift()
    fig3_rollback()
    fig4_auditability()
    fig5_scalability()
    fig6_overhead()
    print("\nAll 6 charts saved to: gitops-control-plane/results/charts/")
