import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from matplotlib.lines import Line2D


# ============================================================
# Load this-work data
# ============================================================

with h5py.File("V2O3_this_work.h5", "r") as f:
    Us = f["U"][:]
    Ts = f["T"][:]
    R1 = f["R1"][:]
    dn = f["dn"][:]


# ============================================================
# Load reference data
# ============================================================

ref = {}

with h5py.File("V2O3_reference.h5", "r") as f:
    U_list = f["U"][:]

    for U in U_list:
        U = float(U)
        group = f[f"U_{U:.2f}"]

        ref[U] = {
            "T_R1": group["T_R1"][:],
            "R1": group["R1"][:],
            "T_dn": group["T_dn"][:],
            "dn": group["dn"][:],
        }


def work_index(U):
    matches = np.flatnonzero(np.isclose(Us, U))
    return int(matches[0]) if matches.size else None


# ============================================================
# Styles
# ============================================================

markmf = "s"
markus = "o"
lsmf = ":"
lsus = "-"

colors = cm.viridis(np.linspace(0.10, 0.90, len(U_list)))
color = dict(zip(U_list, colors))

style = {
    "gem": dict(
        ls=lsus,
        marker=markus,
        lw=1.8,
        ms=4,
    ),
    "ref": dict(
        ls=lsmf,
        marker=markmf,
        ms=7.5,
        mew=0.9,
        mec="black",
    ),
}


# ============================================================
# Figure
# ============================================================

fig, (ax_r, ax_n) = plt.subplots(
    2,
    1,
    figsize=(6, 7),
    sharex=True,
)

for U in U_list:
    U = float(U)
    c = color[U]

    # --------------------------------------------------------
    # This work
    # --------------------------------------------------------

    j = work_index(U)

    if j is None:
        print(f"Warning: U={U:.2f} is not present in this-work data.")

    else:
        valid = np.isfinite(Ts) & np.isfinite(R1[j])

        ax_r.plot(
            Ts[valid]*2,
            R1[j][valid]**2,
            color=c,
            **style["gem"],
        )

        valid = np.isfinite(Ts) & np.isfinite(dn[j])

        ax_n.plot(
            Ts[valid]*2,
            dn[j][valid],
            color=c,
            **style["gem"],
        )

    # --------------------------------------------------------
    # Reference
    # --------------------------------------------------------

    TR = ref[U]["T_R1"]
    R_ref = ref[U]["R1"]

    valid = np.isfinite(TR) & np.isfinite(R_ref)

    ax_r.plot(
        TR[valid]*2,
        R_ref[valid]**2,
        color=c,
        **style["ref"],
    )

    TD = ref[U]["T_dn"]
    dn_ref = ref[U]["dn"]

    valid = np.isfinite(TD) & np.isfinite(dn_ref)

    ax_n.plot(
        TD[valid]*2,
        dn_ref[valid],
        color=c,
        **style["ref"],
    )


# ============================================================
# Axes
# ============================================================

for ax in (ax_r, ax_n):
    ax.set_xscale("log")
    ax.set_xlim(8e-3, 1)
    ax.set_ylim(0, 1)
    ax.tick_params(direction="in", labelsize=12)

ax_r.set_ylabel(r"$Z_1$", fontsize=15)
ax_n.set_ylabel(r"$n_1-n_2$", fontsize=15)
ax_n.set_xlabel(r"$T/D$", fontsize=15)


# ============================================================
# Legends
# ============================================================

interaction_handles = [
    Line2D(
        [0],
        [0],
        color=color[U],
        lw=2.4,
        label=rf"$U/D={U*2:.1f}$",
    )
    for U in U_list
]

method_handles = [
    Line2D(
        [0],
        [0],
        color="black",
        ls=lsus,
        marker=markus,
        lw=2.2,
        label="This work ($B=1$)",
    ),
    Line2D(
        [0],
        [0],
        color="black",
        ls=lsmf,
        marker=markmf,
        mfc="gray",
        mec="black",
        mew=0.9,
        ms=7.5,
        label="Ref. [143]",
    ),
]

legend_options = dict(
    frameon=True,
    fancybox=True,
    framealpha=0.95,
    facecolor="white",
    edgecolor="0.75",
    borderpad=0.28,
    labelspacing=0.22,
    handlelength=2,
    handletextpad=0.45,
    fontsize=12,
    title_fontsize=15,
)

legend = ax_n.legend(
    handles=interaction_handles,
    title="Interaction strength",
    loc="upper center",
    bbox_to_anchor=(0.75, 1),
    **legend_options,
)

legend.get_frame().set_linewidth(0.8)
ax_n.add_artist(legend)

legend = ax_n.legend(
    handles=method_handles,
    title="Method",
    loc="upper center",
    bbox_to_anchor=(0.725, 0.67),
    **legend_options,
)

legend.get_frame().set_linewidth(0.8)


# ============================================================
# Save and show
# ============================================================

plt.tight_layout()

plt.savefig("Figure12.pdf", bbox_inches="tight")

plt.show()