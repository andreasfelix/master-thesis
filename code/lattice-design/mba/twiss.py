import itertools
import numpy as np
import matplotlib.pyplot as plt
import apace as ap
from apace.plot import draw_lattice, plot_twiss
from mba import make_mba, achromatic_condition, figure_path

n_bends_range = range(2, 7)
fig, axs = plt.subplots(figsize=(6.4, 8), nrows=len(n_bends_range))
for n_bends, ax in zip(n_bends_range, axs):
    mba = make_mba(n_bends, k1=1.0)
    achromatic_condition(mba)
    twiss = ap.Twiss(mba)
    if twiss.stable:
        plot_twiss(twiss)
    plt.sca(ax)
    ax.set_xlim(0, mba.length)
    ax.set_ylim(0, 30)
    draw_lattice(mba, draw_sub_lattices=False)

axs[0].legend(
    loc="lower left",
    bbox_to_anchor=(0.0, 1.05),
    ncol=10,
    borderaxespad=1,
    frameon=False,
)
fig.tight_layout()
fig.savefig(figure_path / "mba-twiss.svg")
