import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py


from matplotlib.lines import Line2D
from matplotlib.patches import Patch


with h5py.File('Data_gem.h5','r') as F:
    T_gem=F['T_list'][()]
    Bs_gem=F['B_list'][()]
    docc_gem=F['docc'][()]
    ekin_gem=F['ekin'][()]
    etot_gem=F['etot'][()]
    
with h5py.File('Data_edipack.h5','r') as F:
    T_edp=F['T_list'][()]
    Bs_edp=F['B_list'][()]
    docc_edp=F['docc'][()]
    ekin_edp=F['ekin'][()]
    etot_edp=F['etot'][()]
    
with h5py.File('Data_NRGLjubljana.h5','r') as F:
    T_nrg=F['T_list'][()]
    docc_nrg=F['docc'][()]
    ekin_nrg=F['ekin'][()]
    etot_nrg=F['etot'][()]

if(np.any(T_nrg!=T_edp) or np.any(T_nrg!=T_gem) ):
    raise ValueError('Temperature lists are not matching!')

T_list_nrg = T_nrg
T_list = T_gem

# ============================================================
# plotting style
# ============================================================

main_label_fs = 15
main_tick_fs = 12
legend_fs = 12
legend_title_fs = 15

eddmft_mark='.'
edgem_mark='.'

colors = cm.viridis(np.linspace(0.10, 0.90, len(Bs_gem)))
color_of_B = dict(zip(Bs_gem, colors))

legend_kw = dict(
    frameon=True,
    fancybox=True,
    framealpha=0.95,
    facecolor="white",
    edgecolor="0.75",
    borderpad=0.28,
    labelspacing=0.22,
    handlelength=2.0,
    handletextpad=0.45,
    fontsize=legend_fs,
    title_fontsize=legend_title_fs,
)

method_handles = [
    Line2D(
        [0], [0], color="black", ls="None", marker="^",
        mec="black", mew=0.9, ms=7.5, label="NRG-DMFT"
    ),
    Line2D(
        [0], [0], color="black", ls=":", marker=eddmft_mark,
        lw=1.8, mew=1.5, ms=6.5, label="ED-DMFT"
    ),
    Line2D(
        [0], [0], color="black", ls="-", marker=edgem_mark,
        lw=1.8, mew=1.5, ms=7, label="ghost-GA"
    ),
]

B_handles = [
    Line2D(
        [0], [0], color=color_of_B[B], lw=2.4,
        label=rf"$B={B}$"
    )
    for B in Bs_gem
]


# ============================================================
# double occupancy
# ============================================================

fig, (ax_d, ax_diff) = plt.subplots(
    2, 1, figsize=(6, 6), sharex=True,
    gridspec_kw={'height_ratios':[1.5,1]} 
)

for ax in (ax_d, ax_diff):
    ax.tick_params(direction="in", labelsize=main_tick_fs)

# upper panel
ax_d.scatter(
    T_list_nrg, docc_nrg,
    color="black",
    marker="^",
    s=56,
    edgecolor="black",
    linewidth=0.9,
    zorder=3
)

for iB, B in enumerate(Bs_gem):
    c = color_of_B[B]

    ax_d.plot(
        T_list,
        docc_gem[:, iB],
        color=c,
        ls="-",
        marker=edgem_mark,
        lw=1.8,
        ms=7,
        mew=1.5
    )

    ax_d.plot(
        T_list,
        docc_edp[:, iB],
        color=c,
        ls=":",
        marker=eddmft_mark,
        lw=1.8,
        ms=6.5,
        mew=1.5
    )

ax_d.set_ylabel(
    r"$\langle \hat{n}_{i \uparrow}\hat{n}_{i \downarrow}\rangle$",
    fontsize=main_label_fs
)
ax_d.set_ylim(-0.01, 0.11)

# legends
leg1 = ax_d.legend(
    handles=method_handles,
    loc="upper center",
    title="Method",
    bbox_to_anchor=(0.6, 0.35),
    **legend_kw
)
leg1.get_frame().set_linewidth(0.8) #0.8
ax_d.add_artist(leg1)

leg2 = ax_d.legend(
    handles=B_handles,
    loc="upper center",
    bbox_to_anchor=(0.85, 0.35),
    **legend_kw
)
leg2.get_frame().set_linewidth(0.8) #0.8

# lower panel: difference
for iB, B in enumerate(Bs_gem):
    c = color_of_B[B]

    ax_diff.plot(
        T_list_nrg,
        docc_nrg - docc_gem[:, iB],
        color=c,
        marker=edgem_mark,
        lw=1.8,
        ms=7,
        mew=1.5
    )

    ax_diff.plot(
        T_list_nrg,
        docc_nrg - docc_edp[:, iB],
        color=c,
        ls=":",
        marker=eddmft_mark,
        lw=1.8,
        ms=6.5,
        mew=1.5
    )

ax_diff.axhline(0, color="0.5", lw=1.0, zorder=0)
ax_diff.set_ylim(-0.075, 0.075)

ax_diff.set_xlabel(r"$T/D$", fontsize=main_label_fs)
ax_diff.set_ylabel(
    r"$\Delta\langle \hat{n}_{i \uparrow}\hat{n}_{i \downarrow}\rangle$",
    fontsize=main_label_fs
)

ax_diff.set_xticks(T_list)

plt.tight_layout()
plt.savefig('Figure9.pdf', bbox_inches="tight")
plt.show()


# ============================================================
# kinetic energy
# ============================================================

fig, (ax_e, ax_diff) = plt.subplots(
    2, 1, figsize=(6, 6), sharex=True,
    gridspec_kw={'height_ratios':[1.5,1]} 
)

for ax in (ax_e, ax_diff):
    ax.tick_params(direction="in", labelsize=main_tick_fs)

# upper panel
ax_e.scatter(
    T_list_nrg, ekin_nrg,
    color="black",
    marker="^",
    s=56,
    edgecolor="black",
    linewidth=0.9,
    zorder=3
)

for iB, B in enumerate(Bs_gem):
    c = color_of_B[B]

    ax_e.plot(
        T_list,
        ekin_gem[:, iB],
        color=c,
        ls="-",
        marker=edgem_mark,
        lw=1.8,
        ms=7,
        mew=1.5
    )

    ax_e.plot(
        T_list,
        ekin_edp[:, iB],
        color=c,
        ls=":",
        marker=eddmft_mark,
        lw=1.8,
        ms=6.5,
        mew=1.5
    )

ax_e.set_ylabel(r"$e_{\rm kin}$", fontsize=main_label_fs)
ax_e.set_ylim(-0.31, -0.10)
ax_e.set_yticks([-0.30, -0.25, -0.20, -0.15, -0.10])

leg1 = ax_e.legend(
    handles=method_handles,
    loc="upper center",
    title="Method",
    bbox_to_anchor=(0.6, 0.95),
    **legend_kw
)
leg1.get_frame().set_linewidth(0.8)
ax_e.add_artist(leg1)

leg2 = ax_e.legend(
    handles=B_handles,
    loc="upper center",
    bbox_to_anchor=(0.85, 0.95),
    **legend_kw
)
leg2.get_frame().set_linewidth(0.8)

# lower panel: difference
for iB, B in enumerate(Bs_gem):
    c = color_of_B[B]

    ax_diff.plot(
        T_list_nrg,
        ekin_nrg - ekin_gem[:, iB],
        color=c,
        marker=edgem_mark,
        lw=1.8,
        ms=7,
        mew=1.5
    )

    ax_diff.plot(
        T_list_nrg,
        ekin_nrg - ekin_edp[:, iB],
        color=c,
        ls=":",
        marker=eddmft_mark,
        lw=1.8,
        ms=6.5,
        mew=1.5
    )

ax_diff.axhline(0, color="0.5", lw=1.0, zorder=0)
ax_diff.set_ylim(-0.075, 0.075)

ax_diff.set_xlabel(r"$T/D$", fontsize=main_label_fs)
ax_diff.set_ylabel(
    r"$\Delta e_{\rm kin}$",
    fontsize=main_label_fs
)

ax_diff.set_xticks(T_list)

plt.tight_layout()
plt.savefig('Figure10.pdf', bbox_inches="tight")
plt.show()