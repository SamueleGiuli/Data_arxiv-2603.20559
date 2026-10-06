"""Figure 6: zero-temperature large-B behavior of the gRISB sum rules.

Paramagnetic single-band Hubbard model on the infinite-coordination Bethe
lattice at T = 0, U/D = 2, half-bandwidth D = 1.  Left column n = 1.00, right
column n = 0.85.

Rows 1-4 are the published quantities entering Eqs. (191) and (200)-(202).
Row 5 is the new embedding-hybridization sum rule

    [D^T D*]_{sigma sigma} = sum_a |[D]_{a sigma}|^2  ->  D^2 / 4 ,

i.e. the sum over ghost/bath levels a of the squared embedding coupling, for a
fixed physical spin-orbital sigma.  This is the zeroth moment -- the 1/w
coefficient -- of the embedding hybridization function

    Delta_emb,{sigma sigma'}(w) = sum_a [D]_{a sigma}* [D]_{a sigma'} / (w - lambda_a) .

The Bethe-lattice DMFT self-consistency Delta(w) = (D^2/4) G(w), together with
G(w) -> 1/w at large w, pins that moment at D^2/4 independently of U and of the
filling.  With D = 1 the reference value is 0.25.  Only the converged coupling
matrices are needed -- no dynamical quantities.

Data
----
All plotted quantities are read from fig6_sumrules_data.csv (one row per
filling n, interaction U and number of ghost levels B).

Usage
-----
    python plot.py

writes Figure6.pdf and Figure6.png next to this script and prints the
deviation of the embedding-hybridization sum rule from D^2/4.
"""
import csv
import os

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

# Times for all text.  Liberation/Nimbus Roman are metric-compatible Times
# clones and are what Linux boxes usually have; STIX is the Times-matched math
# face bundled with matplotlib, so the equations match the labels either way.
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'Liberation Serif',
                              'Nimbus Roman', 'Nimbus Roman No9 L',
                              'FreeSerif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# One type size for every piece of text in the figure.
FONTSIZE = 15
plt.rcParams.update({
    'font.size': FONTSIZE,
    'axes.titlesize': FONTSIZE,
    'axes.labelsize': FONTSIZE,
    'xtick.labelsize': FONTSIZE,
    'ytick.labelsize': FONTSIZE,
    'legend.fontsize': FONTSIZE,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, 'fig6_sumrules_data.csv')

BS = [3, 5, 7, 9, 11, 13]
HALF_BANDWIDTH = 1.0
SUM_RULE = HALF_BANDWIDTH**2 / 4.

CASES = [
    ('(a)', 2.00, 1.00),
    ('(b)', 2.00, 0.85),
]

FIELDS = ['nqp', 'nphys', 'siglin', 'sig0', 'sig0an', 'sig1', 'sig1an',
          'DdD', 'mu']

def read_csv():
    rows = list(csv.DictReader(open(CSV_PATH)))
    data = []
    for tag, U, nfill in CASES:
        sel = [r for r in rows
               if abs(float(r['n']) - nfill) < 1e-9
               and abs(float(r['U']) - U) < 1e-9]
        sel.sort(key=lambda r: int(r['B']))
        d = {'B': np.array([int(r['B']) for r in sel])}
        d.update({k: np.array([float(r[k]) for r in sel]) for k in FIELDS})
        data.append((tag, U, nfill, d))
    return data


def set_ylim(ax, blue, black, pad=0.12):
    """Frame the curve and its reference; avoid zooming into round-off noise."""
    lo = min(np.min(blue), np.min(black))
    hi = max(np.max(blue), np.max(black))
    scale = max(abs(lo), abs(hi), 1.0)
    if hi - lo < 1e-3 * scale:
        mid = 0.5 * (lo + hi)
        ax.set_ylim(mid - 0.05 * scale, mid + 0.05 * scale)
    else:
        ax.set_ylim(lo - pad * (hi - lo), hi + pad * (hi - lo))
    ax.ticklabel_format(axis='y', useOffset=False)


data = read_csv()
print('replotted from %s' % CSV_PATH)

def row_specs(d):
    """(blue curve, black reference, blue label, black label) for each row."""
    B = d['B']
    return [
        (d['nqp'], d['nphys'],
         r'$\langle\Phi^0_i|\tilde{c}^\dagger_{i\uparrow}\tilde{c}_{i\uparrow}|\Phi^0_i\rangle$',
         r'$\langle\Phi_i|c^\dagger_{i\uparrow}c_{i\uparrow}|\Phi_i\rangle$'),
        (d['siglin'], np.zeros_like(B, dtype=float),
         r'$\Sigma^{\rm lin}_i$', r'$0$'),
        (d['sig0'], d['sig0an'],
         r'$\Sigma^{(0)}_i$', r'$\Sigma^{(0)}_{i,\rm emb}$'),
        (d['sig1'], d['sig1an'],
         r'$\Sigma^{(1)}_i$', r'$\Sigma^{(1)}_{i,\rm emb}$'),
        (d['DdD'], np.full_like(B, SUM_RULE, dtype=float),
         r'$[\mathcal{D}^{T}\mathcal{D}^{*}]_{\sigma\sigma}$', r'$D^2/4$'),
    ]


# Fixed per row so the boxes sit in each panel's empty corner rather than
# wherever 'best' happens to land after a data change.
LEGEND_LOC = ['lower left', 'lower right', 'center left', 'lower right',
              'lower right']

# Drawn oversized so 15 pt text has room, then scaled to REVTeX \columnwidth by
#   \includegraphics[width=\columnwidth]{Figure6.pdf}
# which brings the effective type size to 15 * 3.375/7.0 ~ 7.2 pt.
fig, axes = plt.subplots(5, 2, figsize=(7.0, 7.4),
                         sharex=True, sharey='row')

specs = [row_specs(d) for _tag, _U, _n, d in data]

for col, (tag, U, nfill, d) in enumerate(data):
    axes[0, col].set_title(r'%s $U/D=2$, $n=%.2f$' % (tag, nfill), pad=4)

    for row, (blue, black, lab_blue, lab_black) in enumerate(specs[col]):
        ax = axes[row, col]
        ax.plot(d['B'], blue, 'o-', color='blue', ms=4.5, lw=1.3,
                label=lab_blue)
        ax.plot(d['B'], black, 'k--', lw=1.2, label=lab_black)
        if col == 0:  # legends in the left column only, as in the published Fig. 6
            ax.legend(loc=LEGEND_LOC[row], framealpha=0.9, handlelength=1.6,
                      borderpad=0.25, labelspacing=0.2, handletextpad=0.5,
                      borderaxespad=0.3)

    axes[-1, col].set_xlabel(r'$B$', labelpad=1)
    axes[-1, col].set_xticks(BS)

# y-axis is shared across each row, so the limits must frame both columns.
for row in range(5):
    blues = [specs[c][row][0] for c in range(2)]
    blacks = [specs[c][row][1] for c in range(2)]
    set_ylim(axes[row, 0], np.concatenate(blues), np.concatenate(blacks))

plt.tight_layout(pad=0.3, h_pad=0.4, w_pad=0.3)
for ext in ('png', 'pdf'):
    fig.savefig(os.path.join(HERE, 'Figure6.%s' % ext), dpi=200)
print('wrote Figure6.png / .pdf')

print('\nNew bottom row -- embedding hybridization sum rule')
print('%-8s %3s  %-14s %-12s' % ('case', 'B', 'sum_a|D_{a,up}|^2', 'dev from D^2/4'))
for tag, U, nfill, d in data:
    for B, v in zip(d['B'], d['DdD']):
        print('n=%.2f  %3d  %-14.8f %-12.2e' % (nfill, B, v, v - SUM_RULE))
