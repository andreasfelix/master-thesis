import math

import apace as ap
import numpy as np
import pandas as pd
from apace.plot import draw_lattice, plot_twiss, plt

from fodo import create_fodo, figure_path

config = dict(drift_length=4, bend_length=3, quad_length=1, k1=0.8)
fig, axs = plt.subplots(2, figsize=(6.4, 6.4))
angles = 0, math.pi / 8
twiss_list = [ap.Twiss(create_fodo(angle=angle, **config)) for angle in angles]

for ax, twiss in zip(axs, twiss_list):
    lattice = twiss.lattice
    plt.sca(ax=ax)
    plot_twiss(twiss)
    plt.xlim(0, lattice.length)
    plt.ylim(-1, 20)
    draw_lattice(lattice)
    plt.xticks(rotation=45)

fig.legend(*axs[0].get_legend_handles_labels(), "upper left", ncol=10, frameon=False)
plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.savefig(figure_path / "fodo-twiss.svg")

fig, axs = plt.subplots(3, figsize=(6.4, 6.4))
twiss = twiss_list[1]
lattice = twiss.lattice

for ax, functions in zip(
    axs, (("beta_x", "beta_y"), ("alpha_x", "alpha_y"), ("psi_x", "psi_y"))
):
    plt.sca(ax)
    plot_twiss(twiss, functions)
    plt.xlim(0, lattice.length)
    draw_lattice(lattice)
    plt.xticks(rotation=45)


handles, labels = [], []
for h, l in (ax.get_legend_handles_labels() for ax in axs):
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
            "Cell length $L$",
            r"Bending angle $\varphi$",
            "Quadrupole strength $k_1$",
            "Horizontal tune $Q_x$",
            "Vertical tune $Q_y$",
            r"Maximum horizontal beta $\beta_{x,max}$",
            r"Maximum vertical beta $\beta_{y,max}$",
            r"Maximum dispersion $\eta_{x,max}$",
        ],
    ).to_markdown(floatfmt=".2f")
)
