# Unification-gGA-DMFT-data

Repository containing the data and scripts for the article:

**“Unifying Variational and Dynamical Quantum Embedding: From Ghost Gutzwiller Approximation to Dynamical Mean-Field Theory”**  
[(arXiv:2603.20559)](https://doi.org/10.48550/arXiv.2603.20559)

---

## Overview

This repository provides all data and Python scripts required to reproduce the figures in the paper.

Each figure is organized in its own directory, containing:
- the relevant data files (HDF5, CSV or plain text)
- a standalone plotting script `plot.py`
- the resulting figure

| Directory | Figure | Content | Output |
|:--|:--|:--|:--|
| `Fig6_PlotSumRule/` | Fig. 6 | Zero-temperature large-*B* behavior of the sum rules (Bethe lattice, *U/D* = 2, *n* = 1.00 and 0.85) | `Figure6.pdf`, `Figure6.png` |
| `Fig7_PlotBethe/`   | Fig. 7 | Double occupancy, energy and entropy vs. temperature on the Bethe lattice: ghost-GA (*B* = 1, 3) vs. DMFT | `Figure7.pdf` |
| `Fig8_PlotSquare/`  | Fig. 8 | Magnetization phase diagram of the square-lattice Hubbard model, compared with Refs. [107, 108] | `Figure8.png` |
| `Fig9_10_PlotEDB/`  | Figs. 9, 10 | Double occupancy (Fig. 9) and kinetic energy (Fig. 10): ghost-GA vs. ED-DMFT (EDIpack) vs. NRG-DMFT | `Figure9.pdf`, `Figure10.pdf` |
| `Fig11_PlotFTG/`    | Fig. 11 | Finite-temperature double occupancy, energy and entropy at *U/D* = 1.95, compared with Refs. [142, 145] | `Figure11.pdf` |
| `Fig12_PlotV2O3/`   | Fig. 12 | Quasiparticle weight and orbital polarization for the V₂O₃ model, compared with Ref. [143] | `Figure12.pdf` |

---

## Requirements

All figures are generated using Python. The required packages are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The code has been tested in a clean environment with the following versions:

- Python: **3.11.11**
- NumPy: **2.4.6**
- Matplotlib: **3.11.2**
- h5py: **3.16.0**

---

## Usage

To reproduce a figure, navigate to the corresponding folder and run:

```bash
cd Fig7_PlotBethe
python plot.py
```

The scripts read their data files from the current directory, so they must be run from inside their folder.
The figure is saved in the same folder, overwriting the version provided in the repository.
