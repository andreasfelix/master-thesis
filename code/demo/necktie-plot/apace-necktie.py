#%% define fodo lattice
import apace as ap

d1 = ap.Drift("d1", length=0.55)
b1 = ap.Dipole("b1", length=1.5, angle=0.392701, e1=0.1963505, e2=0.1963505)
q1 = ap.Quadrupole("q1", length=0.2, k1=1.2)
q2 = ap.Quadrupole("q2", length=0.4, k1=-1.2)
cell = ap.Lattice("FODO", [q1, d1, b1, d1, q2, d1, b1, d1, q1])
fodo = ap.Lattice("RING", 8 * [cell])

twiss = ap.Twiss(fodo, steps_per_element=4)

#%% quadrupole scan
import numpy as np

samples = 100
start, end = 0, 2
results = np.empty((samples, samples))
interval = np.linspace(start, end, samples)
for i, q1.k1 in enumerate(interval):
    for j, q2.k1 in enumerate(-interval):
        try:
            results[i, j] = np.mean([twiss.beta_x, twiss.beta_y])
        except ap.UnstableLatticeError:
            results[i, j] = np.nan

#%% visualize necktie-plot
import matplotlib.pyplot as plt

from master_thesis import figure_path

fig, ax = plt.subplots()
extent = start, end, start, -end
image = ax.imshow(results.T, extent=extent, origin="lower", vmin=0, vmax=30)
ax.set(xlabel=r"$k_\mathrm{q1}$ / m$^{-2}$", ylabel=r"$k_\mathrm{q2}$ / m$^{-2}$")
fig.colorbar(image, ax=ax).ax.set_title(r"$\beta_\mathrm{mean}$")
fig.tight_layout()
fig.savefig(figure_path / "necktie-plot-apace.svg")

# # 3D surface
# fig = plt.figure()
# results[results > 10] = np.nan
# ax = fig.gca(projection="3d")
# ax.plot_surface(*np.meshgrid(interval, interval), results)
# ax.set_zlim(0, 15)
# fig.tight_layout()
# plt.show()
