import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


# ============================================================
# Load extracted HDF5 data
# ============================================================

data_dir = "."

Bs = [1, 3]
Uplot = [1.0, 2.0, 3.2]

D, K, V, E, F, S = {}, {}, {}, {}, {}, {}

for B in Bs:
    with h5py.File(f"{data_dir}/ghost_ga_B{B}.h5", "r") as f:
        Ts = f["T"][:]
        Us = f["U"][:]

        D[B] = f["docc"][:]
        K[B] = f["ekin"][:]
        V[B] = f["epot"][:]
        E[B] = f["etot"][:]
        F[B] = f["free_energy"][:]
        S[B] = f["entropy"][:]


# ============================================================
# Load DMFT data
# ============================================================

Dm, Em = {}, {}

with h5py.File(f"{data_dir}/dmft.h5", "r") as f:
    Td = f["T"][:]

    for U in Uplot:
        group = f[f"U_{U:.3f}"]
        Dm[U] = group["docc"][:]
        Em[U] = group["energy"][:]

# DMFT-NRG entropy
Tn, Sn = {}, {}

with h5py.File(f"{data_dir}/DMFTNRG_S.h5", "r") as f:
    for U in Uplot:
        group = f[f"U{U:.2f}"]
        Tn[U] = np.array([float(k[1:]) for k in group])
        Sn[U] = np.array([group[k]["entropy"][()] for k in group])


# ============================================================
# Plotting styles
# ============================================================

colors = cm.viridis(np.linspace(0.10, 0.90, len(Uplot)))
color = dict(zip(Uplot, colors))

style = {
    1: dict(ls="--", marker="", lw=1.8, ms=4),
    3: dict(ls="-", marker="", lw=1.8, ms=4),
}

uix = {
    round(float(U), 3): i
    for i, U in enumerate(Us)
}


# ============================================================
# Main figure
# ============================================================

fig, (ax_d, ax_e) = plt.subplots(
    2,
    1,
    figsize=(6, 7),
    sharex=True,
)

energy = []

for U in Uplot:
    j = uix[round(U, 3)]
    c = color[U]

    # Ghost-GA
    for B in Bs:
        md = np.isfinite(D[B][:, j])
        me = np.isfinite(E[B][:, j])

        ax_d.plot(
            Ts[md],
            D[B][md, j],
            color=c,
            **style[B],
        )

        ax_e.plot(
            Ts[me],
            E[B][me, j],
            color=c,
            **style[B],
        )

        if np.any(me):
            energy.append(E[B][me, j])

    # DMFT double occupancy
    md = np.isfinite(Td) & np.isfinite(Dm[U])

    ax_d.plot(
        Td[md],
        Dm[U][md],
        color=c,
        mec="black",
        ls="None",
        marker="^",
        ms=7.5,
        mew=0.9,
    )

    # DMFT energy
    me = np.isfinite(Td) & np.isfinite(Em[U])

    ax_e.plot(
        Td[me],
        Em[U][me],
        color=c,
        mec="black",
        ls="None",
        marker="^",
        ms=7.5,
        mew=0.9,
    )

    if np.any(me):
        energy.append(Em[U][me])


# ============================================================
# Main-axis formatting
# ============================================================

for ax in (ax_d, ax_e):
    ax.set_xscale("log")
    ax.set_xlim(3e-2, 10)
    ax.tick_params(direction="in", labelsize=12)

ax_d.set_ylabel(
    r"$\langle \hat{n}_{i\uparrow}\hat{n}_{i\downarrow}\rangle$",
    fontsize=15,
)

ax_e.set_ylabel(
    r"$(\mathcal{E}-\mu N)/N$",
    fontsize=15,
)

ax_e.set_xlabel(
    r"$T/D$",
    fontsize=15,
)

ax_d.set_ylim(0, 0.25)

if energy:
    energy = np.concatenate(energy)

    emin = np.nanmin(energy)
    emax = np.nanmax(energy)
    espan = emax - emin

    ax_e.set_ylim(
        emin - 0.22 * espan,
        emax + 0.05 * espan,
    )


# ============================================================
# Legends
# ============================================================

interaction_handles = [
    Line2D(
        [0],
        [0],
        color=color[U],
        lw=2.4,
        label=rf"$U/D={U:.1f}$",
    )
    for U in Uplot
]

method_handles = [
    Line2D(
        [0],
        [0],
        color="black",
        ls="--",
        lw=2.2,
        label="Ghost-GA (B=1)",
    ),
    Line2D(
        [0],
        [0],
        color="black",
        ls="-",
        lw=2.2,
        label="Ghost-GA (B=3)",
    ),
    Line2D(
        [0],
        [0],
        color="black",
        ls="None",
        marker="^",
        mfc="gray",
        mec="black",
        mew=0.9,
        ms=7.5,
        label="DMFT",
    ),
    Line2D(
        [0],
        [0],
        color="black",
        ls="None",
        marker="o",
        mfc="white",
        mec="black",
        mew=0.9,
        ms=6,
        label="Entropy (B=3)",
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
    fontsize=10,
    title_fontsize=10,
)

legend = ax_d.legend(
    handles=interaction_handles,
    title="Interaction strength",
    loc="upper center",
    bbox_to_anchor=(0.37, 1),
    **legend_options,
)

legend.get_frame().set_linewidth(0.8)
ax_d.add_artist(legend)

legend = ax_d.legend(
    handles=method_handles,
    title="Method",
    loc="lower right",
    bbox_to_anchor=(0.985, 0.02),
    **legend_options,
)

legend.get_frame().set_linewidth(0.8)


# ============================================================
# Entropy inset
# ============================================================

axins = inset_axes(
    ax_e,
    width="42%",
    height="42%",
    loc="lower right",
    bbox_to_anchor=(0, 0.10, 1, 1),
    bbox_transform=ax_e.transAxes,
    borderpad=1,
)

entropy_values = []

for U in Uplot:
    j = uix[round(U, 3)]

    # DMFT-NRG (background)
    axins.plot(
        Tn[U],
        Sn[U] / np.log(2),
        color=color[U],
        mec="black",
        ls="None",
        marker="^",
        ms=7,
        mew=0.7,
        zorder=0,
    )

    entropy = S[3][:, j] / np.log(2)
    valid = np.isfinite(entropy)

    axins.plot(
        Ts[valid],
        entropy[valid],
        color=color[U],
        lw=1.8,
        zorder=0,
    )

    axins.scatter(
        Ts[valid][::4],
        entropy[valid][::4],
        facecolor="white",
        edgecolor=color[U],
        zorder=1,
        s=15,
    )

    if np.any(valid):
        entropy_values.append(entropy[valid])


# ============================================================
# Inset formatting
# ============================================================

axins.set_xscale("log")
axins.set_xlim(1e-2, 10)

axins.tick_params(
    direction="in",
    labelsize=9,
)

axins.set_xlabel(
    r"$T/D$",
    fontsize=10,
    labelpad=1,
)

axins.set_ylabel(
    r"$S/\ln 2$",
    fontsize=10,
    labelpad=2,
)

axins.yaxis.tick_left()
axins.yaxis.set_label_position("left")

if entropy_values:
    entropy_values = np.concatenate(entropy_values)

    smin = np.nanmin(entropy_values)
    smax = np.nanmax(entropy_values)
    sspan = smax - smin

    axins.set_ylim(
        smin - 0.08 * sspan,
        smax + 0.08 * sspan,
    )

for spine in axins.spines.values():
    spine.set_linewidth(0.8)

axins.set_facecolor("white")
axins.patch.set_alpha(0.96)


# ============================================================
# Save and display
# ============================================================

plt.tight_layout()
plt.savefig("Figure7.pdf", bbox_inches="tight")
plt.show()