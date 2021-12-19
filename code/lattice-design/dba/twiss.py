import math

import apace as ap
import numpy as np
import pandas as pd
from apace.plot import draw_elements, plt
from dba import achromatic_condition, figure_path, make_dba

RED = "#EF4444"
GREEN = "#10B981"
BLUE = "#3B82F6"

lattice = make_dba()
lattice["q1"].k1 = 4
lattice["q2"].k1 = -6
lattice["q3"].k1 = 5

achromatic_condition(lattice)
twiss = ap.Twiss(lattice)

fig, axs = plt.subplots(3, figsize=(8, 9))
ax0, ax1, ax2 = axs

ax0.plot(twiss.s, twiss.beta_x, color=RED, label=r"$\beta_\mathrm{x}$ / m")
ax0.plot(twiss.s, twiss.beta_y, color=BLUE, label=r"$\beta_\mathrm{y}$ / m")
ax0.set(xlim=(0, lattice.length), ylim=(-1, 32))
ax0.set(xlabel="orbit position $s$ / m", ylabel=r"$\beta_u$ / m")
ax0.legend(bbox_to_anchor=[0.5, 0.8], loc="center", ncol=2)
draw_elements(ax0, lattice)

ax1.plot(twiss.s, twiss.eta_x, color=RED, label=r"$\eta_\mathrm{x}$ / m")
ax1.plot(twiss.s, twiss.eta_x_dds, color=GREEN, label=r"$\eta_\mathrm{x}$'")
ax1.set(xlim=(0, lattice.length), ylim=(-0.4, 0.4))
ax1.set(
    xlabel="orbit position $s$ / m", ylabel=r"$\eta_\mathrm{x}$ / m, $\eta_\mathrm{x}'$"
)
ax1.legend(bbox_to_anchor=[0.15, 0.8], loc="center", ncol=2)
draw_elements(ax1, lattice)

ax2.plot(twiss.s, twiss.psi_x, color=RED, label=r"$\psi_\mathrm{x}$")
ax2.plot(twiss.s, twiss.psi_y, color=BLUE, label=r"$\psi_\mathrm{y}$")
ax2.set(xlim=(0, lattice.length))
ax2.set(xlabel="orbit position $s$ / m", ylabel=r"$\psi_u$")
ax2.legend(bbox_to_anchor=[0.15, 0.8], loc="center", ncol=2)
dba_start = 1.9 + 0.75
dba_end = 6.1 - 0.75
psi_bend = np.interp((dba_start, dba_end), twiss.s, twiss.psi_x)
plt.hlines(psi_bend, dba_start, dba_end, colors="black", linestyles="dotted")
plt.axvline(dba_start, color="black", linestyle="dotted")
plt.axvline(dba_end, color="black", linestyle="dotted")
draw_elements(ax2, lattice)
phase_advance = psi_bend[1] - psi_bend[0]
plt.annotate(
    text="",
    xy=(4, psi_bend[0]),
    xytext=(4, psi_bend[1]),
    arrowprops=dict(arrowstyle="<->"),
    zorder=10,
)
plt.text(4.1, phase_advance / 2 + 0.4, f"{phase_advance/math.pi:.2f} $\pi$")

handles, labels = [], []
for h, l in (ax.get_legend_handles_labels() for ax in axs):
    handles += h
    labels += l

plt.tight_layout()
plt.savefig(figure_path / "dba-twiss.svg")

print(
    pd.DataFrame(
        {
            "DBA": [
                twiss.lattice.length,
                lattice["b1"].angle,
                lattice["q1"].k1,
                lattice["q2"].k1,
                lattice["q3"].k1,
                twiss.tune_x,
                twiss.tune_y,
                np.max(twiss.beta_x),
                np.max(twiss.beta_y),
                np.max(twiss.eta_x),
            ]
        },
        index=[
            r"Cell length $L$ / m",
            r"Bending angle $\varphi$",
            r"Quadrupole strength $k_\mathrm{Q1}$ / m$^{-2}$",
            r"Quadrupole strength $k_\mathrm{Q2}$ / m$^{-2}$",
            r"Quadrupole strength $k_\mathrm{Q3}$ / m$^{-2}$",
            r"Horizontal tune $Q_\mathrm{x}$",
            r"Vertical tune $Q_\mathrm{y}$",
            r"Maximum horizontal beta $\beta_\mathrm{x,max}$ / m",
            r"Maximum vertical beta $\beta_\mathrm{y,max}$ / m",
            r"Maximum dispersion $\eta_\mathrm{x,max}$ / m",
        ],
    ).to_markdown(floatfmt=".2f")
)

# without dipole edges
# |                                         |   DBA |
# |:----------------------------------------|------:|
# | Cell length $L$                         |  8.00 |
# | Bending angle $\varphi$                 |  0.39 |
# | Quadrupole strength Q1 $k_1$            |  3.60 |
# | Quadrupole strength Q2 $k_1$            | -4.16 |
# | Quadrupole strength Q3 $k_1$            |  7.73 |
# | Horizontal tune $Q_x$                   |  0.76 |
# | Vertical tune $Q_y$                     |  0.30 |
# | Maximum horizontal beta $\beta_{x,max}$ | 19.62 |
# | Maximum vertical beta $\beta_{y,max}$   | 16.58 |
# | Maximum dispersion $\eta_{x,max}$       |  0.50 |
