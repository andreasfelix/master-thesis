#%%
import json
from math import pi
import numpy as np
import apace as ap
import apace.plot as aplot

import matplotlib.pyplot as plt

energy = 1700  # mev
n_cells = 16
angle = 2 * pi / n_cells

q1 = ap.Quadrupole("Q1", 0.4, 1.0)
q2 = ap.Quadrupole("Q2", 0.4, -1.1)
ds = ap.Drift("DS", 1.0)
dq = ap.Drift("DQ", 0.2)
b1 = ap.Dipole("B1", 2.5, angle)

#%%
cell = ap.Lattice("Cell", [ds, q1, dq, b1, dq, q2, ds])
ring = ap.Lattice("Ring", n_cells * [cell])

twiss = ap.Twiss(ring, energy=energy)

steps = 50
emittance_array = np.empty((steps, steps))

fig, ax = plt.subplots()

for i, q1.k1 in enumerate(np.linspace(0.1, 3.0, steps)):
    for j, q2.k1 in enumerate(np.linspace(-0.1, -3.0, steps)):
        emittance_array[i, j] = twiss.emittance_x if twiss.stable_x else np.nan
        print(twiss.emittance_x)

heatmap = ax.imshow(emittance_array, cmap="RdBu", vmin=0.0, vmax=1e-4,)
fig.colorbar(heatmap, ax=ax)


# aplot.twiss_plot(twiss)

plt.savefig("paul-fodo-heat.pdf")
