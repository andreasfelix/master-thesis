import itertools

import matplotlib.pyplot as plt
import numpy as np

import apace as ap
import apace.plot as aplot


def make_mba(n_bends=2, n_cells=16, drift_length=5, bend_length=3, quad_length=2):
    angle = 2 * np.pi / (n_bends * n_cells)
    angle_2 = 0.5 * angle
    d1 = ap.Drift("d1", drift_length / (8 + 2 * (n_bends - 2)))
    q1 = ap.Quadrupole("q1", length=quad_length / 2 / (2 + n_bends - 1), k1=2.0)
    q2 = ap.Quadrupole("q2", length=quad_length / 2 / 2, k1=-2.0)
    b1 = ap.Dipole("b1", bend_length / n_bends, angle=angle, e1=angle_2, e2=angle_2)
    left = [d1, q1, d1, q2, d1]
    right = reversed(left)
    cell = ap.Lattice("cell", [*left, b1, *([d1, q1, d1, b1] * (n_bends - 1)), *right])
    return ap.Lattice(f"{n_bends}-ba", n_cells * [cell])


n_bends_range = range(2, 9)
fig, axs = plt.subplots(figsize=(9, 16), nrows=len(range(2, 9)))
for n_bends, ax in zip(n_bends_range, axs):
    mba = make_mba(n_bends)
    cell = mba["cell"]
    plt.sca(ax)
    ax.set_xlim(0, cell.length)
    twiss = ap.Twiss(mba)
    q1 = mba["q1"]
    q2 = mba["q2"]
    for q1.k1, q2.k1 in itertools.product(np.linspace(0, 3), np.linspace(0, -3)):
        if twiss.stable:
            aplot.plot_twiss(twiss)
            print(mba.name, q1.k1, q2.k1)
            break
    aplot.draw_lattice(cell, ax=ax, draw_sub_lattices=False)

axs[0].legend(
    loc="lower left",
    bbox_to_anchor=(0.0, 1.05),
    ncol=10,
    borderaxespad=1,
    frameon=False,
)
fig.tight_layout()
fig.savefig("plots/mba.pdf")
