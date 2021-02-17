import apace as ap
import numpy as np
from tqdm import tqdm

d1 = ap.Drift("d1", length=0.55)
b1 = ap.Dipole("b1", length=1.5, angle=0.392701, e1=0.1963505, e2=0.1963505)
q1 = ap.Quadrupole("q1", length=0.2, k1=1.2)
q2 = ap.Quadrupole("q2", length=0.4, k1=-1.2)
cell = ap.Lattice("FODO", [q1, d1, b1, d1, q2, d1, b1, d1, q1])
fodo = ap.Lattice("RING", [cell] * 8)

twiss = ap.Twiss(fodo, steps_per_element=4)

# Define parameters for necktie plot
samples = 30
extent = 0, 2
interval = np.linspace(*extent, samples)
results = np.empty((samples, samples))

for i, q1.k1 in enumerate(tqdm(interval)):
    for j, q2.k1 in enumerate(-interval):
        try:
            results[i, j] = np.mean([twiss.beta_x, twiss.beta_y])
        except ap.UnstableLatticeError:
            results[i, j] = np.nan

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
heatmap = ax.imshow(
    results, extent=[*extent, *extent], origin="lower", vmin=0, vmax=30, cmap="cool"
)
ax.set_xlabel("q1$_{{k1}}$ / m$^2$")
ax.set_ylabel("q2$_{{k1}}$ / m$^2$")
ax.set_title("necktie plot")
colorbar = fig.colorbar(heatmap, ax=ax)
colorbar.ax.set_title("$\\beta_{\\mathrm{mean}}$", fontsize=12, pad=10)
fig.tight_layout()
fig.savefig("necktie-plot-apace.svg")
