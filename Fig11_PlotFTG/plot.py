import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.lines import Line2D

U=1.95

B1S_gem=np.loadtxt('B1Slist.dat')
B1E_gem=np.loadtxt('B1Elist.dat')
B1D_gem=np.loadtxt('B1docclist.dat',dtype=np.complex128).real
B1T_gem=np.loadtxt('B1Tlist.dat')

B3S_gem=np.loadtxt('B3Slist.dat')
B3E_gem=np.loadtxt('B3Elist.dat')
B3D_gem=np.loadtxt('B3docclist.dat',dtype=np.complex128).real
B3T_gem=np.loadtxt('B3Tlist.dat')

Ts_nl, S_nl=np.loadtxt('S_NL_U1.95.dat',skiprows=1,unpack=True)
Te_nl, E_nl=np.loadtxt('E_NL_U1.95.dat',skiprows=1,unpack=True)
Td_nl, D_nl=np.loadtxt('D_NL_U1.95.dat',skiprows=1,unpack=True)

Td_w , D_w =np.loadtxt('D_W_U1.95.dat',skiprows=1,unpack=True, delimiter=',')
Ts_w , S_w =np.loadtxt('S_W_U1.95.dat',skiprows=1,unpack=True, delimiter=',')

cnl='tomato'
cw='gold'



main_label_fs = 15
main_tick_fs = 12
legend_fs = 12
legend_title_fs = 15

fig, (ax_d, ax_e) = plt.subplots(
    2, 1,
    figsize=(6, 7),
    sharex=False
)

# ----------------------------
# Top panel: double occupancy
# ----------------------------
ax_d.plot(
    B1T_gem, B1D_gem,
    color="navy",
    linestyle="--",
    linewidth=1.8,
    label="This work ($B=1$)"
)

ax_d.plot(
    B3T_gem, B3D_gem,
    color="navy",
    linestyle="-",
    linewidth=1.8,
    label="This work ($B=3$)"
)

ax_d.scatter(
    Td_nl, D_nl,
    color=cnl,
    marker="s",
    s=30,
    edgecolor="black",
    linewidth=0.6,
    label="Ref. [145]",
    zorder=3
)

ax_d.scatter(
    Td_w, D_w,
    color=cw,
    marker="o",
    s=30,
    edgecolor="black",
    linewidth=0.6,
    label="Ref. [142]",
    zorder=3
)


ax_d.set_xlim(0, 1)
ax_d.set_ylim(0, 0.2)
ax_d.set_ylabel(
    r"$\langle \hat{n}_{i \uparrow} \hat{n}_{i \downarrow}\rangle$",
    fontsize=main_label_fs
)

# ----------------------------
# Bottom panel: energy
# ----------------------------
ax_e.plot(
    B1T_gem, B1E_gem + 0.5 * U,
    color="navy",
    linestyle="--",
    linewidth=1.8,
    label="This work ($B=1$)"
)

ax_e.plot(
    B3T_gem, B3E_gem + 0.5 * U,
    color="navy",
    linestyle="-",
    linewidth=1.8,
    label="This work ($B=3$)"
)

ax_e.scatter(
    Te_nl, E_nl,
    color=cnl,
    marker="s",
    s=30,
    edgecolor="black",
    linewidth=0.6,
    label="Ref. [114]",
    zorder=3
)

ax_e.set_xlim(0, 1)
ax_e.set_ylim(-0.11, 0.3)
ax_e.set_xlabel(r"$T/D$", fontsize=main_label_fs)
ax_e.set_ylabel(r"$\mathcal{E}/N$", fontsize=main_label_fs)

# ----------------------------
# Shared styling
# ----------------------------
for ax in (ax_d, ax_e):
    ax.tick_params(direction="in", labelsize=main_tick_fs)

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

ax_d.legend(loc="lower right",
    title="Method",
#    bbox_to_anchor=(0.85, 0.95),
    **legend_kw)

# ----------------------------
# Inset: entropy inside E panel
# ----------------------------
axins = inset_axes(
    ax_e,
    width="42%",
    height="42%",
    loc="upper left",
    bbox_to_anchor=(0.05, 0.0, 1.0, 1.0),
    bbox_transform=ax_e.transAxes,
    borderpad=1.0
)

axins.plot(
    B1T_gem, B1S_gem / np.log(2),
    color="navy",
    linestyle="--",
    linewidth=1.8
)

axins.plot(
    B3T_gem, B3S_gem / np.log(2),
    color="navy",
    linestyle="-",
    linewidth=1.8
)

axins.scatter(
    Ts_nl, S_nl / np.log(2),
    color=cnl,
    marker="s",
    s=15,
    edgecolor="black",
    linewidth=0.5,
    zorder=3
)

axins.scatter(
    Ts_w, S_w ,
    color=cw,
    marker="o",
    s=15,
    edgecolor="black",
    linewidth=0.5,
    zorder=3
)

axins.axhline(0.0, color="black", alpha=0.5, linestyle="-", linewidth=0.8)
axins.axhline(1.0, color="black", alpha=0.25, linestyle=":", linewidth=0.8)
axins.axhline(2.0, color="black", alpha=0.25, linestyle=":", linewidth=0.8)

axins.set_xscale("log")
axins.set_xlim(1e-3, 10)

axins.set_xlabel(r"$T/D$", fontsize=10, labelpad=1)
axins.set_ylabel(r"$S/ \ln 2$", fontsize=10, labelpad=2)
axins.tick_params(direction="in", labelsize=9)

for spine in axins.spines.values():
    spine.set_linewidth(0.8)

axins.set_facecolor("white")
axins.patch.set_alpha(0.96)

plt.tight_layout()
plt.savefig("Figure11.pdf", bbox_inches="tight")
plt.show()