import apace as ap
import matplotlib.pyplot as plt
import numpy as np
from apace.plot import draw_elements, plot_twiss
from mba import achromatic_condition, figure_path, make_mba2

n_bends_range = range(2, 5)
fig, axs = plt.subplots(figsize=(6.4, 8), nrows=len(n_bends_range))
energy = 1000
for n_bends, ax in zip(n_bends_range, axs):
    mba = make_mba2(n_bends, k1=1.7, drift_length=10.0)
    quads = list(filter(lambda x: isinstance(x, ap.Quadrupole), mba.elements))
    achromatic_condition(mba, quads, energy)
    twiss = ap.Twiss(mba, energy=energy)
    if twiss.stable:
        plot_twiss(ax, twiss)
        ax.text(
            0.5,
            0.8,
            f"emittance {twiss.emittance_x:.2e}",
            ha="center",
            va="top",
            transform=ax.transAxes,
        )
    ax.set_xlim(0, mba.length)
    ax.set_ylim(-1, 50)
    draw_elements(ax, mba)

axs[0].legend(
    loc="lower left",
    bbox_to_anchor=(0.0, 1.05),
    ncol=10,
    borderaxespad=1,
    frameon=False,
)
fig.tight_layout()
fig.savefig(figure_path / "mba-twiss.svg")
