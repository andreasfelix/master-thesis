import math

import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt
import numpy as np

"""
contstraints:
10m cell

3m dipole
1m quadrupole
6m drift
"""

n_cells = 30
angle = math.pi / n_cells
angle_2 = 0.5 * angle

# # FODO
# q1 = ap.Quadrupole("q1", length=0.5, k1=0.3)
# q2 = ap.Quadrupole("q2", length=0.25, k1=-0.3)
# d1 = ap.Drift("d1", 1.5)
# b1 = ap.Dipole("b1", 1.5, angle=angle, e1=angle_2, e2=angle_2)
# fodo = ap.Lattice(
#     "fodo", n_cells * [ap.Lattice("cell", [q2, d1, b1, d1, q1, d1, b1, d1, q2,])],
# )

# DBA
d1 = ap.Drift("d1", 0.75)
q1 = ap.Quadrupole("q1", length=0.125, k1=1.0)
q2 = ap.Quadrupole("q2", length=0.25, k1=-1.0)
b1 = ap.Dipole("b1", 1.5, angle=angle, e1=angle_2, e2=angle_2)
cell = ap.Lattice(
    "cell", [d1, q1, d1, q2, d1, b1, d1, q1, q1, d1, b1, d1, q2, d1, q1, d1,],
)
dba = ap.Lattice("dba", n_cells * [cell])

# TBA
d1 = ap.Drift("d1", 0.6)
q1 = ap.Quadrupole("q1", length=0.125, k1=1.0)
q2 = ap.Quadrupole("q2", length=0.25, k1=-1.0)
b1 = ap.Dipole("b1", 1.0, angle=angle, e1=angle_2, e2=angle_2)
cell = ap.Lattice(
    "cell",
    [d1, q1, d1, q2, d1, b1, d1, q1, d1, b1, d1, q1, d1, b1, d1, q2, d1, q1, d1,],
)
tba = ap.Lattice("tba", n_cells * [cell])


# emittance
# energys = np.linspace(0, 2000, 2001)
# emittance = np.empty(energys.size)
# for i, energy in enumerate(energys):
#     print(energy)
#     twiss = ap.Twiss(fodo, energy=energy)
#     emittance[i] = twiss.emittance_x

# fig, ax = plt.subplots()
# ax.plot(energys, emittance)
# ax.set_xlabel("Energys / MeV")
# ax.set_ylabel("Emittance")
# fig.savefig("plots/emittance.pdf")

fig, axs = plt.subplots(3, figsize=(10, 10))
for i, lattice in enumerate((fodo, dba, tba)):
    twiss = ap.Twiss(lattice)
    aplot.plot_twiss(twiss, ax=axs[i])
    aplot.draw_lattice(lattice, ax=axs[i], x_max=10)
    axs[i].set_xlim(0, 10)

fig.tight_layout()
fig.legend()
fig.savefig(f"plots/lattice-design.pdf")
