import math

import apace as ap
import numpy as np
import pandas as pd
from apace.plot import draw_elements, plot_twiss, plt
from fodo import make_fodo

from master_thesis import figure_path

config = dict(drift_length=4, bend_length=3, quad_length=1, k1=0.8)
fig, axs = plt.subplots(2, figsize=(6.4, 6.4))
angles = 0, math.pi / 8
twiss_list = [ap.Twiss(make_fodo(angle=angle, **config)) for angle in angles]

for ax, twiss in zip(axs, twiss_list):
    lattice = twiss.lattice
    plot_twiss(ax, twiss)
    ax.set(xlim=(0, lattice.length), ylim=(-1, 20))
    ax.legend(bbox_to_anchor=[0.5, 0.825], loc="center", ncol=3)
    draw_elements(ax, lattice)

plot_twiss(axs[1], twiss_list[0], line_style="dashed", alpha=0.5, line_width=3)

fig.tight_layout()
fig.savefig(figure_path / "fodo-twiss.svg")

fig, (ax0, ax1, ax2) = plt.subplots(3, figsize=(6.4, 6.4))
twiss = twiss_list[1]
lattice = twiss.lattice

RED = "#EF4444"
BLUE = "#3B82F6"

ax0.plot(twiss.s, twiss.beta_x, color=RED, label=r"$\beta_\mathrm{x}$ / m")
ax0.plot(twiss.s, twiss.beta_y, color=BLUE, label=r"$\beta_\mathrm{y}$ / m")
ax0.set(xlim=(0, lattice.length), ylabel=r"$\beta_u$ / m")
draw_elements(ax0, lattice)

ax1.plot(twiss.s, twiss.alpha_x, color=RED, label=r"$\alpha_\mathrm{x}$ / m")
ax1.plot(twiss.s, twiss.alpha_y, color=BLUE, label=r"$\alpha_\mathrm{y}$ / m")
ax1.set(xlim=(0, lattice.length), ylabel=r"$\alpha_u$ / m")
draw_elements(ax1, lattice)

ax2.plot(twiss.s, twiss.psi_x, color=RED, label=r"$\psi_\mathrm{x}$ / m")
ax2.plot(twiss.s, twiss.psi_y, color=BLUE, label=r"$\psi_\mathrm{y}$ / m")
ax2.set(
    xlim=(0, lattice.length), xlabel="orbit position $s$ / m", ylabel=r"$\psi_u$ / m"
)
draw_elements(ax2, lattice)

handles, labels = [], []
for h, l in (ax.get_legend_handles_labels() for ax in (ax0, ax1, ax2)):
    handles += h
    labels += l

fig.legend(handles, labels, "upper left", ncol=10, frameon=False)
plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.savefig(figure_path / "fodo-twiss-2.svg")

print(
    pd.DataFrame(
        {
            name: [
                twiss.lattice.length,
                angle,
                config["k1"],
                twiss.tune_x,
                twiss.tune_y,
                np.max(twiss.beta_x),
                np.max(twiss.beta_y),
                np.max(twiss.eta_x),
            ]
            for name, angle, twiss in zip(
                ["without dipoles", "with dipoles"], angles, twiss_list
            )
        },
        index=[
            r"Cell length $L$ / m",
            r"Bending angle $\varphi$",
            r"Quadrupole strength $k$ / m$^{-2}$",
            r"Horizontal tune $Q_\mathrm{x}$",
            r"Vertical tune $Q_\mathrm{y}$",
            r"Max. horizontal beta $\beta_\mathrm{x,max}$ / m",
            r"Max. vertical beta $\beta_\mathrm{y,max}$ / m",
            r"Max. dispersion $\eta_\mathrm{x,max}$ / m",
        ],
    ).to_markdown(floatfmt=".2f")
)
