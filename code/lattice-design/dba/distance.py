"Distance between bend and quad should "

from math import pi

import apace as ap
import apace.plot as aplot
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from master_thesis import figure_path

n_particles = 7
n_rows = 3
length = 8
bend_length, angle = 2.8, pi / 16
quad_length = 0.4
drift_length = length - bend_length - quad_length
d = ap.Drift("Drift", length=drift_length / (2 * n_rows + 2))
b = ap.Dipole("Bend", length=bend_length / 2, angle=angle, e1=angle / 2, e2=angle / 2)
q = ap.Quadrupole("Quad", length=quad_length, k1=2.55)

fig = plt.figure(figsize=(8, 8))

outer = gridspec.GridSpec(n_rows, 1, hspace=0.2)
cmap = plt.get_cmap("rainbow_r")

initial_distribution = ap.distribution(
    n_particles, delta_dist="uniform", delta_width=0.01
)


for i in range(n_rows):
    inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[i], hspace=0)
    ax1, ax2 = (plt.Subplot(fig, inner[j]) for j in range(2))
    d1 = (3 - i) * [d]
    d2 = (1 + i) * [d]
    lattice = ap.Lattice("DBA", [*d1, b, *d2, q, *d2, b, *d1])
    tracking = ap.TrackingMatrix(lattice, initial_distribution)
    twiss = ap.Twiss(lattice, initial=np.zeros(8))

    for i, particle in enumerate(tracking.x.T):
        ax1.plot(tracking.s, particle, color=cmap(i / (n_particles - 1)))

    ax1.set(xlim=(0, lattice.length), ylim=(-0.004, 0.004))
    ax1.set(ylabel="$x$ / m")
    ax1.set_xticklabels([])
    aplot.draw_elements(ax1, lattice)
    aplot.draw_sub_lattices(ax1, lattice)

    ax2.plot(twiss.s, twiss.eta_x, label=r"$\eta_\mathrm{x}$ / m")
    ax2.plot(twiss.s, twiss.eta_x_dds, label=r"$\eta_\mathrm{x}'$")
    ax2.set(xlim=(0, lattice.length), ylim=(-0.7, 0.7))
    ax2.set(ylabel=r"$\eta_\mathrm{x}$ / m, $\eta_\mathrm{x}'$")
    ax2.legend(loc="lower left", ncol=2)
    aplot.draw_sub_lattices(ax2, lattice)
    fig.add_subplot(ax1)
    fig.add_subplot(ax2, sharey=ax1)

ax2.set(xlabel="orbit position $s$ / m")

plt.subplots_adjust(left=0.125, right=0.98, top=0.94, bottom=0.05)
fig.savefig(figure_path / "dba-distance.svg")
