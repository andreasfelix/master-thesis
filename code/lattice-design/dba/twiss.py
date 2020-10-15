import math

import apace as ap
import numpy as np
import pandas as pd
from apace.plot import draw_lattice, plot_twiss, plt

from dba import make_dba, figure_path, achromatic_condition

# TODO: smaller angle
config = dict(angle=math.pi / 4, drift_length=4, bend_length=3, quad_length=1, k1=0.8)
lattice = make_dba(**config)
achromatic_condition(lattice)
twiss = ap.Twiss(lattice)

fig, axs = plt.subplots(3, figsize=(8, 9))
ax0, ax1, ax2 = axs

plt.sca(ax=ax0)
plot_twiss(twiss, twiss_functions=["beta_x", "beta_y"])
draw_lattice(lattice)
plt.xlim(0, lattice.length)
plt.xticks(rotation=45)

plt.sca(ax=ax1)
plot_twiss(twiss, twiss_functions=["eta_x", "eta_x_dds"])
draw_lattice(lattice)
plt.xlim(0, lattice.length)
plt.xticks(rotation=45)

plt.sca(ax=ax2)
plot_twiss(twiss, twiss_functions=["psi_x", "psi_y"])
psi_bend = np.interp((1.9, 6.1), twiss.s, twiss.psi_x)
plt.hlines(psi_bend, 0, lattice.length, colors="black", linestyles="dotted")
draw_lattice(lattice)
plt.xlim(0, lattice.length)
plt.xticks(rotation=45)
phase_advance = psi_bend[1] - psi_bend[0]
plt.annotate(
    text="",
    xy=(4, psi_bend[0]),
    xytext=(4, psi_bend[1]),
    arrowprops=dict(arrowstyle="<->"),
)
plt.text(3.45, phase_advance / 2 + 0.4, f"{phase_advance/math.pi:.2f} $\pi$")

handles, labels = [], []
for h, l in (ax.get_legend_handles_labels() for ax in axs):
    handles += h
    labels += l

fig.legend(handles, labels, "upper left", ncol=10, frameon=False)
plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.savefig(figure_path / "dba-twiss.svg")

print(
    pd.DataFrame(
        {
            "DBA": [
                twiss.lattice.length,
                config["angle"],
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
            "Cell length $L$",
            r"Bending angle $\varphi$",
            "Quadrupole strength Q1 $k_1$",
            "Quadrupole strength Q2 $k_1$",
            "Quadrupole strength Q3 $k_1$",
            "Horizontal tune $Q_x$",
            "Vertical tune $Q_y$",
            r"Maximum horizontal beta $\beta_{x,max}$",
            r"Maximum vertical beta $\beta_{y,max}$",
            r"Maximum dispersion $\eta_{x,max}$",
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
